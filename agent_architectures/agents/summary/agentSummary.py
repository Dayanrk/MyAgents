"""
AgentSummary - Classe pour créer une mémoire à court terme pour chatbot
en résumant les blocs de messages de conversation.
"""

from typing import List, Dict, Any
from datetime import datetime
import json

# J'ai envie d'essayer quelque chose c'est de de donner au modèle toutes la conversation pour la mémoire à court terme, 
# Mais toutes la conversation on la mets dans une base de donnée vectoriel 
# Ensuite on dis à notre context manager de faire une requete sur la question de base, de chercher dans la base de donnée vectoriel les question et réponse le plus en lien. 
# Ils renvoient certains, vecteur de la conversation que on mettra dans l'ordre, puis on fais un summary sur ces conversation et on le donne en short-terme memory

class AgentSummary:
    """
    Classe responsable de créer et gérer une mémoire à court terme
    pour un chatbot en analysant et résumant les blocs de messages.
    """
    
    def __init__(self, max_memory_size: int = 100, summary_threshold: int = 10):
        """
        Initialise l'AgentSummary avec les paramètres de configuration.
        
        Args:
            max_memory_size: Taille maximale de la mémoire à court terme
            summary_threshold: Seuil de messages avant déclenchement du résumé
        """
        self.max_memory_size = max_memory_size
        # self.agent_summary = Créer notre agent qui va résumer 
    
    def summary_messages(self, message_content: str, id_conversation:str , query:str, connect: Any) -> List[Dict[str, Any]]:
        """
        Traite des bloc de messages et renvoie ce meme blocs de messages mais pour chaque 
        message, on ne garde que le message essentiel pour créer un short-terme memory
        
        Args:
            messages: Liste des messages à traiter (format: [{"role": "user/assistant", "content": "..."}])
            
        Returns:
            Liste des messages résumés avec seulement l'essentiel
        """
        # clean query = appelle à un agent pour reposer la question proprement, selon le besoin
        
        # chercher la question dans la base de donnée vectoriel weaviate dans la conversation id
        
        # Trier les messages dans l'ordre de conversation  grace aux métadonnée
        
        # Sur chaque bloc de message faire un summary. Mais la méthode question, c'est comment utilsié les ASYNC pour pouvoir renvoyer le message dans l'ordre 
        # Exemple on a 4 message dans l'ordre 
        # On traite les questions de manière parallèle mais des questions on finit plus tot alors que ils ont pas été traité en premier
        # Comment remettre les réponse finale dans l'ordre bref 
        
        # renvoyer les réponses dans l'ordre
        pass
    
    def _summarize_single_message(self, content: str, role: str) -> str:
        """
        Résume un message individuel en gardant seulement l'essentiel.
        
        Args:
            content: Contenu du message à résumer
            role: Rôle de l'expéditeur (user/assistant)
            
        Returns:
            Message résumé avec les points essentiels
        """
        pass
    
    def _summarize_user_message(self, content: str) -> str:
        """
        Résume un message utilisateur en extrayant l'intention et la demande.
        
        Args:
            content: Contenu du message utilisateur
            
        Returns:
            Résumé du message utilisateur
        """
        # Extrait les mots-clés et l'intention
        # Format: "Intention: [demande] - Contexte: [détails importants]"
        
        # Analyse simple pour extraire l'essentiel
        sentences = content.split('.')
        key_sentences = []
        
        # Garde les phrases qui contiennent des mots-clés importants
        important_keywords = ['demande', 'besoin', 'aide', 'comment', 'pourquoi', 'quand', 'où', 'qui', 'quoi']
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in important_keywords):
                key_sentences.append(sentence)
        
        # Si pas de mots-clés trouvés, prend les premières phrases
        if not key_sentences:
            key_sentences = sentences[:2]
        
        return " | ".join(key_sentences[:3])  # Max 3 points essentiels
    
    def _summarize_assistant_message(self, content: str) -> str:
        """
        Résume un message assistant en gardant les informations clés.
        
        Args:
            content: Contenu du message assistant
            
        Returns:
            Résumé du message assistant
        """
        # Extrait les informations importantes de la réponse
        # Format: "Action: [ce qui a été fait] - Info: [informations clés]"
        
        sentences = content.split('.')
        key_sentences = []
        
        # Garde les phrases qui contiennent des informations importantes
        important_keywords = ['solution', 'réponse', 'conseil', 'étape', 'méthode', 'exemple', 'résultat']
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in important_keywords):
                key_sentences.append(sentence)
        
        # Si pas de mots-clés trouvés, prend les premières phrases
        if not key_sentences:
            key_sentences = sentences[:2]
        
        return " | ".join(key_sentences[:3])  # Max 3 points essentiels
    
    def _create_summary(self) -> None:
        """
        Crée un résumé des blocs de messages récents.
        Analyse les patterns, extrait les points clés et génère un résumé concis.
        """
        # Analyse les blocs de messages pour identifier les thèmes principaux
        main_topics = self._extract_main_topics()
        
        # Identifie les actions et décisions importantes
        key_actions = self._identify_key_actions()
        
        # Génère le résumé structuré
        self.current_summary = {
            "timestamp": datetime.now().isoformat(),
            "summary_id": len(self.short_term_memory),
            "main_topics": main_topics,
            "key_actions": key_actions,
            "conversation_flow": self._analyze_conversation_flow(),
            "user_intent": self._extract_user_intent()
        }
    
    def _extract_main_topics(self) -> List[str]:
        """
        Extrait les thèmes principaux de la conversation.
        
        Returns:
            Liste des thèmes identifiés
        """
        # Analyse les messages pour identifier les sujets récurrents
        # Utilise des techniques de NLP pour extraire les mots-clés
        pass
    
    def _identify_key_actions(self) -> List[Dict[str, Any]]:
        """
        Identifie les actions et décisions importantes dans la conversation.
        
        Returns:
            Liste des actions clés avec leur contexte
        """
        # Analyse les messages pour détecter les actions, décisions, demandes
        # Identifie les changements d'état ou les nouvelles informations
        pass
    
    def _analyze_conversation_flow(self) -> Dict[str, Any]:
        """
        Analyse le flux de la conversation pour comprendre la progression.
        
        Returns:
            Dictionnaire décrivant le flux de conversation
        """
        # Analyse la structure temporelle des échanges
        # Identifie les transitions entre sujets
        # Détecte les patterns de communication
        pass
    
    def _extract_user_intent(self) -> Dict[str, Any]:
        """
        Extrait l'intention principale de l'utilisateur.
        
        Returns:
            Dictionnaire contenant l'intention et le contexte
        """
        # Analyse les messages utilisateur pour identifier l'intention
        # Catégorise le type de demande (information, action, clarification)
        pass
    
    def _update_short_term_memory(self) -> None:
        """
        Met à jour la mémoire à court terme avec le nouveau résumé.
        Gère la taille de la mémoire et archive les anciens résumés si nécessaire.
        """
        # Ajoute le nouveau résumé à la mémoire
        self.short_term_memory.append(self.current_summary)
        
        # Gère la taille de la mémoire (FIFO)
        if len(self.short_term_memory) > self.max_memory_size:
            self.short_term_memory.pop(0)
        
        # Réinitialise les blocs de messages traités
        self.message_blocks = []
    
    def get_short_term_memory(self) -> List[Dict[str, Any]]:
        """
        Récupère la mémoire à court terme actuelle.
        
        Returns:
            Liste des résumés en mémoire à court terme
        """
        return self.short_term_memory.copy()
    
    def get_context_summary(self, context_window: int = 5) -> str:
        """
        Génère un résumé contextuel des derniers échanges pour le chatbot.
        
        Args:
            context_window: Nombre de résumés récents à inclure
            
        Returns:
            Résumé contextuel formaté pour le chatbot
        """
        # Sélectionne les résumés les plus récents
        recent_summaries = self.short_term_memory[-context_window:]
        
        # Formate le résumé contextuel
        context_summary = {
            "conversation_context": recent_summaries,
            "current_topics": self._get_current_topics(),
            "user_preferences": self._extract_user_preferences()
        }
        
        return json.dumps(context_summary, ensure_ascii=False, indent=2)
    
    def _get_current_topics(self) -> List[str]:
        """
        Récupère les thèmes actuellement actifs dans la conversation.
        
        Returns:
            Liste des thèmes actuels
        """
        # Analyse les résumés récents pour identifier les thèmes en cours
        pass
    
    def _extract_user_preferences(self) -> Dict[str, Any]:
        """
        Extrait les préférences de l'utilisateur basées sur l'historique.
        
        Returns:
            Dictionnaire des préférences identifiées
        """
        # Analyse les patterns de communication de l'utilisateur
        # Identifie les préférences de style, de format, etc.
        pass
    
    def clear_memory(self) -> None:
        """
        Vide complètement la mémoire à court terme.
        Utile pour redémarrer une nouvelle session de conversation.
        """
        self.short_term_memory = []
        self.message_blocks = []
        self.current_summary = ""
    
    def export_memory(self, filepath: str) -> None:
        """
        Exporte la mémoire à court terme vers un fichier JSON.
        
        Args:
            filepath: Chemin du fichier de destination
        """
        memory_data = {
            "short_term_memory": self.short_term_memory,
            "message_blocks": self.message_blocks,
            "current_summary": self.current_summary,
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=2)
    
    def import_memory(self, filepath: str) -> None:
        """
        Importe une mémoire à court terme depuis un fichier JSON.
        
        Args:
            filepath: Chemin du fichier source
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            memory_data = json.load(f)
        
        self.short_term_memory = memory_data.get("short_term_memory", [])
        self.message_blocks = memory_data.get("message_blocks", [])
        self.current_summary = memory_data.get("current_summary", "")
