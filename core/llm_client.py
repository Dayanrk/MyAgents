"""
Client LiteLLM centralisé pour tous les agents.
Gère les appels aux différents modèles LLM de manière unifiée.
"""

import litellm
from typing import Dict, List, Any, Optional, Union
import asyncio
import logging
from dataclasses import dataclass
from enum import Enum


class ModelProvider(Enum):
    """Fournisseurs de modèles supportés."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"


@dataclass
class LLMConfig:
    """Configuration pour un modèle LLM."""
    provider: ModelProvider
    model_name: str
    api_key: str
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = 30


class LLMClient:
    """
    Client centralisé pour les appels LLM via LiteLLM.
    Gère la configuration, la rotation des modèles et la gestion d'erreurs.
    """
    
    def __init__(self, configs: List[LLMConfig]):
        self.configs = {config.provider.value: config for config in configs}
        self.logger = logging.getLogger("llm_client")
        self.usage_stats = {}
        
        # Configuration LiteLLM
        self._setup_litellm()
    
    def _setup_litellm(self) -> None:
        """Configure LiteLLM avec les clés API."""
        for config in self.configs.values():
            if config.provider == ModelProvider.OPENAI:
                litellm.openai_key = config.api_key
            elif config.provider == ModelProvider.ANTHROPIC:
                litellm.anthropic_key = config.api_key
            elif config.provider == ModelProvider.GOOGLE:
                litellm.google_key = config.api_key
            elif config.provider == ModelProvider.COHERE:
                litellm.cohere_key = config.api_key
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        provider: ModelProvider,
        model_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Génère une réponse en utilisant le modèle spécifié.
        
        Args:
            messages: Liste des messages pour le chat
            provider: Fournisseur du modèle
            model_name: Nom du modèle (optionnel)
            **kwargs: Paramètres additionnels (temperature, max_tokens, etc.)
        
        Returns:
            Dict contenant la réponse et les métadonnées
        """
        config = self.configs.get(provider.value)
        if not config:
            raise ValueError(f"Configuration not found for provider: {provider.value}")
        
        # Utilise le nom de modèle spécifié ou celui de la config
        model = model_name or config.model_name
        
        # Fusionne les paramètres
        params = {
            "model": f"{provider.value}/{model}",
            "messages": messages,
            "temperature": kwargs.get("temperature", config.temperature),
            "max_tokens": kwargs.get("max_tokens", config.max_tokens),
            "timeout": kwargs.get("timeout", config.timeout)
        }
        
        try:
            self.logger.info(f"Generating response with {provider.value}/{model}")
            
            # Appel asynchrone à LiteLLM
            response = await litellm.acompletion(**params)
            
            # Enregistrement des statistiques
            self._update_usage_stats(provider.value, response)
            
            return {
                "content": response.choices[0].message.content,
                "model": model,
                "provider": provider.value,
                "usage": response.usage,
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            raise
    
    async def generate_with_retry(
        self,
        messages: List[Dict[str, str]],
        provider: ModelProvider,
        max_retries: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Génère une réponse avec retry automatique en cas d'erreur.
        """
        for attempt in range(max_retries):
            try:
                return await self.generate(messages, provider, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                self.logger.warning(f"Attempt {attempt + 1} failed, retrying: {str(e)}")
                await asyncio.sleep(2 ** attempt)  # Backoff exponentiel
    
    async def generate_with_fallback(
        self,
        messages: List[Dict[str, str]],
        primary_provider: ModelProvider,
        fallback_providers: List[ModelProvider],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Génère une réponse avec fallback automatique vers d'autres modèles.
        """
        providers_to_try = [primary_provider] + fallback_providers
        
        for provider in providers_to_try:
            try:
                return await self.generate(messages, provider, **kwargs)
            except Exception as e:
                self.logger.warning(f"Provider {provider.value} failed: {str(e)}")
                if provider == providers_to_try[-1]:
                    raise
                continue
    
    async def stream_generate(
        self,
        messages: List[Dict[str, str]],
        provider: ModelProvider,
        **kwargs
    ):
        """
        Génère une réponse en streaming.
        """
        config = self.configs.get(provider.value)
        if not config:
            raise ValueError(f"Configuration not found for provider: {provider.value}")
        
        model = kwargs.get("model_name", config.model_name)
        params = {
            "model": f"{provider.value}/{model}",
            "messages": messages,
            "stream": True,
            "temperature": kwargs.get("temperature", config.temperature),
            "max_tokens": kwargs.get("max_tokens", config.max_tokens)
        }
        
        try:
            async for chunk in litellm.astream(**params):
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            self.logger.error(f"Error in streaming: {str(e)}")
            raise
    
    def _update_usage_stats(self, provider: str, response) -> None:
        """Met à jour les statistiques d'utilisation."""
        if provider not in self.usage_stats:
            self.usage_stats[provider] = {
                "total_requests": 0,
                "total_tokens": 0,
                "total_cost": 0.0
            }
        
        stats = self.usage_stats[provider]
        stats["total_requests"] += 1
        if hasattr(response, 'usage'):
            stats["total_tokens"] += response.usage.total_tokens
            # Calcul du coût (à adapter selon les tarifs)
            stats["total_cost"] += self._calculate_cost(provider, response.usage)
    
    def _calculate_cost(self, provider: str, usage) -> float:
        """Calcule le coût approximatif de l'utilisation."""
        # Tarifs approximatifs (à mettre à jour selon les vrais tarifs)
        pricing = {
            "openai": {"input": 0.0015, "output": 0.002},
            "anthropic": {"input": 0.003, "output": 0.015},
            "google": {"input": 0.0005, "output": 0.0015}
        }
        
        if provider in pricing:
            cost = (usage.prompt_tokens * pricing[provider]["input"] + 
                   usage.completion_tokens * pricing[provider]["output"]) / 1000
            return cost
        
        return 0.0
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques d'utilisation."""
        return self.usage_stats.copy()
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Retourne la liste des modèles disponibles par fournisseur."""
        return {
            "openai": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
            "google": ["gemini-pro", "gemini-pro-vision"],
            "cohere": ["command", "command-light"]
        }
