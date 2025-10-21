# Architecture du Système Multi-Agents Expérimental

## Vue d'ensemble

Ce projet est un laboratoire d'expérimentation pour différentes architectures d'agents. Chaque agent a la même mission mais utilise des approches architecturales différentes. L'objectif est de comparer et évaluer différentes stratégies d'implémentation.

## Architecture Modulaire

```
MyAgents/
├── agent_architectures/       # Différentes architectures d'agents
│   ├── rag_based/            # Agents basés sur RAG
│   │   ├── simple_rag_agent.py
│   │   ├── hierarchical_rag_agent.py
│   │   └── multi_retrieval_agent.py
│   ├── planning_based/       # Agents basés sur la planification
│   │   ├── goal_tree_agent.py
│   │   ├── hierarchical_planner_agent.py
│   │   └── reactive_planner_agent.py
│   ├── reasoning_based/      # Agents basés sur le raisonnement
│   │   ├── chain_of_thought_agent.py
│   │   ├── tree_of_thought_agent.py
│   │   └── graph_reasoning_agent.py
│   ├── hybrid/               # Architectures hybrides
│   │   ├── rag_planning_agent.py
│   │   ├── reasoning_rag_agent.py
│   │   └── multi_strategy_agent.py
│   └── experimental/         # Nouvelles approches expérimentales
│       ├── neuro_symbolic_agent.py
│       ├── meta_learning_agent.py
│       └── adaptive_agent.py
├── shared_components/        # Composants partagés
│   ├── base_agent.py         # Classe de base abstraite
│   ├── llm_client.py         # Client LiteLLM centralisé
│   ├── memory_manager.py     # Gestionnaire de mémoire
│   └── task_interface.py     # Interface commune des tâches
├── modules/                  # Modules réutilisables
│   ├── rag/                  # Système RAG
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   └── embeddings.py
│   ├── planning/             # Système de planification
│   │   ├── goal_decomposition.py
│   │   ├── action_planner.py
│   │   └── constraint_solver.py
│   ├── reasoning/            # Système de raisonnement
│   │   ├── chain_of_thought.py
│   │   ├── tree_of_thought.py
│   │   └── graph_reasoning.py
│   ├── memory/               # Système de mémoire
│   │   ├── short_term.py
│   │   ├── long_term.py
│   │   └── episodic.py
│   └── communication/        # Communication
│       ├── message_bus.py
│       └── protocol.py
├── actions/                  # Actions environnementales (ACT)
│   ├── web_actions.py       # Actions web (navigation, clics, etc.)
│   ├── file_actions.py      # Actions sur fichiers
│   ├── api_actions.py       # Actions API
│   ├── database_actions.py  # Actions base de données
│   └── system_actions.py    # Actions système
├── tools/                    # Outils et utilitaires
│   ├── web_search.py
│   ├── file_operations.py
│   └── data_processing.py
├── config/                   # Configuration
│   ├── agent_configs.py      # Configurations des agents
│   ├── model_configs.py      # Configurations des modèles
│   └── system_config.py      # Configuration système
├── utils/                    # Utilitaires
│   ├── logging.py            # Système de logs
│   ├── metrics.py            # Métriques et monitoring
│   └── validation.py         # Validation des données
├── tests/                    # Tests
│   ├── unit/                 # Tests unitaires
│   ├── integration/          # Tests d'intégration
│   └── agents/               # Tests spécifiques aux agents
├── examples/                 # Exemples d'utilisation
│   ├── simple_chat.py        # Chat simple
│   ├── complex_task.py       # Tâche complexe
│   └── multi_agent_demo.py   # Démonstration multi-agents
├── requirements.txt          # Dépendances
├── setup.py                  # Installation
└── README.md                 # Documentation principale
```

## Composants Principaux

### 1. Architectures d'Agents Expérimentales

Chaque dossier contient différentes implémentations pour la même mission :

#### **RAG-Based Agents** (`agent_architectures/rag_based/`)
- **Simple RAG Agent** : RAG basique avec récupération simple
- **Hierarchical RAG Agent** : RAG avec hiérarchie de documents
- **Multi-Retrieval Agent** : RAG avec plusieurs stratégies de récupération

#### **Planning-Based Agents** (`agent_architectures/planning_based/`)
- **Goal Tree Agent** : Planification par arbre d'objectifs
- **Hierarchical Planner** : Planification hiérarchique
- **Reactive Planner** : Planification réactive

#### **Reasoning-Based Agents** (`agent_architectures/reasoning_based/`)
- **Chain of Thought Agent** : Raisonnement séquentiel
- **Tree of Thought Agent** : Raisonnement arborescent
- **Graph Reasoning Agent** : Raisonnement sur graphe

#### **Hybrid Agents** (`agent_architectures/hybrid/`)
- **RAG + Planning** : Combine RAG et planification
- **Reasoning + RAG** : Combine raisonnement et RAG
- **Multi-Strategy** : Utilise plusieurs stratégies

#### **Experimental Agents** (`agent_architectures/experimental/`)
- **Neuro-Symbolic** : Approche neuro-symbolique
- **Meta-Learning** : Apprentissage méta
- **Adaptive** : Agent adaptatif

### 2. Système RAG

- **Vector Store** : Stockage et recherche vectorielle (ChromaDB/Pinecone)
- **Document Processor** : Traitement et indexation des documents
- **Retriever** : Récupération d'informations pertinentes
- **Embeddings** : Génération et gestion des embeddings

### 3. Système de Mémoire

- **Short Term** : Mémoire de travail pour la session actuelle
- **Long Term** : Stockage persistant des connaissances
- **Episodic** : Mémoire des événements et expériences
- **Semantic** : Mémoire des concepts et relations

### 4. Planification

- **Goal Decomposition** : Décomposition des objectifs en sous-tâches
- **Action Planner** : Planification des actions séquentielles
- **Constraint Solver** : Résolution des contraintes
- **Execution Monitor** : Surveillance de l'exécution

### 5. Communication Inter-Agents

- **Message Bus** : Système de messagerie asynchrone
- **Protocol** : Protocole de communication standardisé
- **Negotiation** : Système de négociation entre agents

## Flux de Travail

1. **Initialisation** : Chargement des agents et configuration
2. **Réception de Tâche** : Analyse et décomposition de la tâche
3. **Planification** : Création du plan d'exécution
4. **Coordination** : Distribution des sous-tâches aux agents
5. **Exécution** : Exécution parallèle ou séquentielle
6. **Synchronisation** : Coordination des résultats
7. **Synthèse** : Combinaison des résultats finaux

## Technologies Utilisées

- **LiteLLM** : Interface unifiée pour les modèles LLM
- **ChromaDB/Pinecone** : Base de données vectorielle
- **FastAPI** : API REST pour l'orchestration
- **Redis** : Cache et message broker
- **PostgreSQL** : Base de données relationnelle
- **Docker** : Containerisation

## Avantages de cette Architecture

1. **Modularité** : Chaque composant est indépendant
2. **Scalabilité** : Facile d'ajouter de nouveaux agents
3. **Flexibilité** : Différentes stratégies pour le même objectif
4. **Maintenabilité** : Code organisé et testable
5. **Extensibilité** : Facile d'intégrer de nouveaux outils

## Exemple d'Utilisation

```python
# Import des différentes architectures
from agent_architectures.rag_based.simple_rag_agent import SimpleRAGAgent
from agent_architectures.planning_based.goal_tree_agent import GoalTreeAgent
from agent_architectures.reasoning_based.chain_of_thought_agent import ChainOfThoughtAgent
from agent_architectures.hybrid.rag_planning_agent import RAGPlanningAgent

# Comparaison d'architectures pour la même tâche
task = "Analyser et résumer ce document complexe"

# Test avec RAG simple
rag_agent = SimpleRAGAgent()
rag_result = await rag_agent.execute(task)

# Test avec planification
planning_agent = GoalTreeAgent()
planning_result = await planning_agent.execute(task)

# Test avec raisonnement
reasoning_agent = ChainOfThoughtAgent()
reasoning_result = await reasoning_agent.execute(task)

# Test avec approche hybride
hybrid_agent = RAGPlanningAgent()
hybrid_result = await hybrid_agent.execute(task)

# Comparaison des résultats
comparison = compare_results([rag_result, planning_result, reasoning_result, hybrid_result])
```

## Avantages de cette Architecture Modulaire

1. **Expérimentation** : Facile de tester différentes approches
2. **Comparaison** : Évaluation objective des performances
3. **Réutilisabilité** : Modules partagés entre architectures
4. **Extensibilité** : Ajout facile de nouvelles architectures
5. **Isolation** : Chaque architecture est indépendante
6. **Prototypage** : Développement rapide de nouvelles idées

Cette architecture permet une approche expérimentale et modulaire pour développer et comparer différentes stratégies d'agents.
