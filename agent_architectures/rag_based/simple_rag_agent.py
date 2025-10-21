"""
Agent RAG simple - Architecture basique avec récupération d'informations.
Utilise un système RAG standard pour récupérer des informations pertinentes.
"""

from typing import Dict, List, Any, Optional
import asyncio
import logging
from shared_components.base_agent import BaseAgent, Task, AgentResult
from modules.rag.retriever import RAGRetriever
from modules.rag.embeddings import EmbeddingGenerator


class SimpleRAGAgent(BaseAgent):
    """
    Agent RAG simple qui utilise la récupération d'informations
    pour répondre aux questions et accomplir des tâches.
    """
    
    def __init__(
        self,
        agent_id: str = "simple_rag_agent",
        llm_client=None,
        vector_store=None,
        **kwargs
    ):
        super().__init__(
            agent_id=agent_id,
            name="Simple RAG Agent",
            description="Agent utilisant RAG basique pour récupérer et synthétiser des informations",
            architecture_type="rag_based",
            llm_client=llm_client,
            **kwargs
        )
        
        # Composants RAG
        self.vector_store = vector_store
        self.retriever = RAGRetriever(vector_store=vector_store)
        self.embedding_generator = EmbeddingGenerator()
        
        self.logger = logging.getLogger(f"rag_agent.{agent_id}")
    
    async def execute_task(self, task: Task) -> AgentResult:
        """
        Exécute une tâche en utilisant l'approche RAG.
        """
        try:
            # 1. Analyse de la tâche
            task_analysis = await self._analyze_task(task)
            
            # 2. Génération de requêtes de recherche
            search_queries = await self._generate_search_queries(task_analysis)
            
            # 3. Récupération d'informations
            retrieved_docs = await self._retrieve_information(search_queries)
            
            # 4. Synthèse des informations
            synthesis = await self._synthesize_information(task, retrieved_docs)
            
            # 5. Génération de la réponse finale
            final_response = await self._generate_final_response(task, synthesis)
            
            return AgentResult(
                agent_id=self.agent_id,
                task_id=task.id,
                success=True,
                output=final_response,
                reasoning=f"RAG approach: Retrieved {len(retrieved_docs)} documents, synthesized information",
                execution_time=0.0,  # Sera mis à jour par run()
                metadata={
                    "retrieved_docs_count": len(retrieved_docs),
                    "search_queries": search_queries,
                    "synthesis": synthesis
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error in RAG execution: {str(e)}")
            raise
    
    async def think(self, context: Dict[str, Any]) -> str:
        """
        Processus de réflexion spécifique à RAG.
        """
        thinking_prompt = f"""
        En tant qu'agent RAG, je dois analyser cette tâche et déterminer:
        1. Quelles informations dois-je récupérer?
        2. Comment structurer ma recherche?
        3. Comment synthétiser les résultats?
        
        Tâche: {context.get('task_description', 'N/A')}
        Contexte: {context.get('context', 'N/A')}
        
        Ma stratégie RAG:
        - Analyser la tâche pour identifier les concepts clés
        - Générer des requêtes de recherche variées
        - Récupérer les documents les plus pertinents
        - Synthétiser les informations de manière cohérente
        """
        
        if self.llm_client:
            response = await self.llm_client.generate(
                messages=[{"role": "user", "content": thinking_prompt}],
                provider="openai"  # À adapter selon votre config
            )
            return response["content"]
        
        return "RAG thinking: Analyser → Rechercher → Récupérer → Synthétiser"
    
    async def _analyze_task(self, task: Task) -> Dict[str, Any]:
        """Analyse la tâche pour identifier les besoins d'information."""
        analysis_prompt = f"""
        Analyse cette tâche et identifie:
        1. Les concepts clés à rechercher
        2. Le type d'information nécessaire
        3. La structure de réponse attendue
        
        Tâche: {task.description}
        Données d'entrée: {task.input_data}
        """
        
        if self.llm_client:
            response = await self.llm_client.generate(
                messages=[{"role": "user", "content": analysis_prompt}],
                provider="openai"
            )
            return {"analysis": response["content"]}
        
        return {"analysis": "Analyse basique de la tâche"}
    
    async def _generate_search_queries(self, task_analysis: Dict[str, Any]) -> List[str]:
        """Génère des requêtes de recherche basées sur l'analyse de la tâche."""
        query_generation_prompt = f"""
        Basé sur cette analyse de tâche, génère 3-5 requêtes de recherche différentes
        qui permettront de récupérer les informations nécessaires.
        
        Analyse: {task_analysis.get('analysis', 'N/A')}
        
        Génère des requêtes variées et complémentaires.
        """
        
        if self.llm_client:
            response = await self.llm_client.generate(
                messages=[{"role": "user", "content": query_generation_prompt}],
                provider="openai"
            )
            # Parse les requêtes (simplifié)
            queries = response["content"].split('\n')
            return [q.strip() for q in queries if q.strip()]
        
        return ["requête par défaut"]
    
    async def _retrieve_information(self, search_queries: List[str]) -> List[Dict[str, Any]]:
        """Récupère les informations pertinentes."""
        all_docs = []
        
        for query in search_queries:
            try:
                docs = await self.retriever.retrieve(query, top_k=3)
                all_docs.extend(docs)
            except Exception as e:
                self.logger.warning(f"Error retrieving for query '{query}': {str(e)}")
        
        # Déduplication et tri par score
        unique_docs = self._deduplicate_documents(all_docs)
        return sorted(unique_docs, key=lambda x: x.get('score', 0), reverse=True)[:10]
    
    async def _synthesize_information(self, task: Task, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Synthétise les informations récupérées."""
        if not retrieved_docs:
            return "Aucune information pertinente trouvée."
        
        synthesis_prompt = f"""
        Synthétise ces informations pour répondre à la tâche:
        
        Tâche: {task.description}
        
        Documents récupérés:
        {self._format_documents_for_synthesis(retrieved_docs)}
        
        Crée une synthèse cohérente et structurée.
        """
        
        if self.llm_client:
            response = await self.llm_client.generate(
                messages=[{"role": "user", "content": synthesis_prompt}],
                provider="openai"
            )
            return response["content"]
        
        return "Synthèse basique des informations récupérées."
    
    async def _generate_final_response(self, task: Task, synthesis: str) -> str:
        """Génère la réponse finale."""
        final_prompt = f"""
        Basé sur cette synthèse, génère une réponse finale pour la tâche:
        
        Tâche: {task.description}
        Synthèse: {synthesis}
        
        Réponse finale structurée et complète.
        """
        
        if self.llm_client:
            response = await self.llm_client.generate(
                messages=[{"role": "user", "content": final_prompt}],
                provider="openai"
            )
            return response["content"]
        
        return synthesis
    
    def _deduplicate_documents(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Supprime les doublons des documents."""
        seen = set()
        unique_docs = []
        
        for doc in docs:
            doc_id = doc.get('id', doc.get('content', ''))
            if doc_id not in seen:
                seen.add(doc_id)
                unique_docs.append(doc)
        
        return unique_docs
    
    def _format_documents_for_synthesis(self, docs: List[Dict[str, Any]]) -> str:
        """Formate les documents pour la synthèse."""
        formatted = []
        for i, doc in enumerate(docs, 1):
            content = doc.get('content', '')
            score = doc.get('score', 0)
            formatted.append(f"Document {i} (score: {score:.2f}):\n{content}\n")
        return '\n'.join(formatted)
