"""
Agent de planification par arbre d'objectifs.
Utilise une approche hiérarchique pour décomposer les tâches en sous-objectifs.
"""

from typing import Dict, List, Any, Optional, Tuple
import asyncio
import logging
from shared_components.base_agent import BaseAgent, Task, AgentResult
from modules.planning.goal_decomposition import GoalDecomposer
from modules.planning.action_planner import ActionPlanner


class GoalTreeAgent(BaseAgent):
    """
    Agent qui utilise un arbre d'objectifs pour planifier et exécuter des tâches.
    Décompose les tâches complexes en sous-objectifs hiérarchiques.
    """
    
    def __init__(
        self,
        agent_id: str = "goal_tree_agent",
        llm_client=None,
        max_depth: int = 5,
        **kwargs
    ):
        super().__init__(
            agent_id=agent_id,
            name="Goal Tree Agent",
            description="Agent utilisant la planification par arbre d'objectifs",
            architecture_type="planning_based",
            llm_client=llm_client,
            **kwargs
        )
        
        self.max_depth = max_depth
        self.goal_decomposer = GoalDecomposer(llm_client=llm_client)
        self.action_planner = ActionPlanner(llm_client=llm_client)
        
        self.logger = logging.getLogger(f"goal_tree_agent.{agent_id}")
    
    async def execute_task(self, task: Task) -> AgentResult:
        """
        Exécute une tâche en utilisant l'approche d'arbre d'objectifs.
        """
        try:
            # 1. Décomposition de la tâche en objectifs
            goal_tree = await self._decompose_task_to_goals(task)
            
            # 2. Planification des actions pour chaque objectif
            action_plan = await self._plan_actions_for_goals(goal_tree)
            
            # 3. Exécution séquentielle du plan
            execution_results = await self._execute_action_plan(action_plan)
            
            # 4. Synthèse des résultats
            final_result = await self._synthesize_results(task, execution_results)
            
            return AgentResult(
                agent_id=self.agent_id,
                task_id=task.id,
                success=True,
                output=final_result,
                reasoning=f"Goal tree approach: {len(goal_tree)} goals, {len(action_plan)} actions executed",
                execution_time=0.0,  # Sera mis à jour par run()
                metadata={
                    "goal_tree": goal_tree,
                    "action_plan": action_plan,
                    "execution_results": execution_results
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error in goal tree execution: {str(e)}")
            raise
    
    async def think(self, context: Dict[str, Any]) -> str:
        """
        Processus de réflexion spécifique à la planification par objectifs.
        """
        thinking_prompt = f"""
        En tant qu'agent de planification par arbre d'objectifs, je dois:
        1. Analyser la tâche complexe
        2. Identifier les objectifs principaux
        3. Décomposer chaque objectif en sous-objectifs
        4. Créer un plan d'actions séquentiel
        5. Exécuter le plan étape par étape
        
        Tâche: {context.get('task_description', 'N/A')}
        Contexte: {context.get('context', 'N/A')}
        
        Ma stratégie de planification:
        - Décomposition hiérarchique des objectifs
        - Planification d'actions pour chaque niveau
        - Exécution séquentielle avec vérification
        - Synthèse des résultats à chaque étape
        """
        
        if self.llm_client:
            response = await self.llm_client.generate(
                messages=[{"role": "user", "content": thinking_prompt}],
                provider="openai"
            )
            return response["content"]
        
        return "Goal tree thinking: Analyser → Décomposer → Planifier → Exécuter → Synthétiser"
    
    async def _decompose_task_to_goals(self, task: Task) -> Dict[str, Any]:
        """Décompose la tâche en arbre d'objectifs."""
        decomposition_prompt = f"""
        Décompose cette tâche complexe en arbre d'objectifs hiérarchique.
        Chaque objectif doit être:
        - Spécifique et mesurable
        - Réalisable
        - Pertinent pour la tâche principale
        
        Tâche: {task.description}
        Données d'entrée: {task.input_data}
        
        Crée un arbre d'objectifs avec:
        - Objectif principal (racine)
        - Objectifs secondaires (branches)
        - Sous-objectifs (feuilles)
        - Relations de dépendance
        """
        
        if self.llm_client:
            response = await self.llm_client.generate(
                messages=[{"role": "user", "content": decomposition_prompt}],
                provider="openai"
            )
            return self._parse_goal_tree(response["content"])
        
        # Structure par défaut
        return {
            "main_goal": task.description,
            "sub_goals": [
                {"id": "goal_1", "description": "Analyser les données d'entrée", "priority": 1},
                {"id": "goal_2", "description": "Traiter les informations", "priority": 2},
                {"id": "goal_3", "description": "Générer la réponse", "priority": 3}
            ],
            "dependencies": []
        }
    
    async def _plan_actions_for_goals(self, goal_tree: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Planifie les actions pour chaque objectif."""
        action_plan = []
        
        for goal in goal_tree.get("sub_goals", []):
            action_prompt = f"""
            Crée un plan d'actions spécifiques pour atteindre cet objectif:
            
            Objectif: {goal['description']}
            Priorité: {goal['priority']}
            
            Génère 2-4 actions concrètes et séquentielles.
            """
            
            if self.llm_client:
                response = await self.llm_client.generate(
                    messages=[{"role": "user", "content": action_prompt}],
                    provider="openai"
                )
                actions = self._parse_actions(response["content"], goal["id"])
            else:
                actions = [
                    {"id": f"action_1_{goal['id']}", "description": f"Action 1 pour {goal['description']}", "goal_id": goal["id"]},
                    {"id": f"action_2_{goal['id']}", "description": f"Action 2 pour {goal['description']}", "goal_id": goal["id"]}
                ]
            
            action_plan.extend(actions)
        
        return action_plan
    
    async def _execute_action_plan(self, action_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Exécute le plan d'actions séquentiellement."""
        results = []
        
        for action in action_plan:
            try:
                self.logger.info(f"Executing action: {action['description']}")
                
                # Simulation d'exécution d'action
                result = await self._execute_single_action(action)
                results.append({
                    "action_id": action["id"],
                    "success": True,
                    "result": result,
                    "timestamp": asyncio.get_event_loop().time()
                })
                
            except Exception as e:
                self.logger.error(f"Error executing action {action['id']}: {str(e)}")
                results.append({
                    "action_id": action["id"],
                    "success": False,
                    "error": str(e),
                    "timestamp": asyncio.get_event_loop().time()
                })
        
        return results
    
    async def _execute_single_action(self, action: Dict[str, Any]) -> str:
        """Exécute une action individuelle."""
        execution_prompt = f"""
        Exécute cette action spécifique:
        
        Action: {action['description']}
        
        Fournis un résultat concret et détaillé.
        """
        
        if self.llm_client:
            response = await self.llm_client.generate(
                messages=[{"role": "user", "content": execution_prompt}],
                provider="openai"
            )
            return response["content"]
        
        return f"Résultat de l'action: {action['description']}"
    
    async def _synthesize_results(self, task: Task, execution_results: List[Dict[str, Any]]) -> str:
        """Synthétise les résultats de l'exécution."""
        synthesis_prompt = f"""
        Synthétise les résultats de l'exécution pour répondre à la tâche originale:
        
        Tâche originale: {task.description}
        
        Résultats d'exécution:
        {self._format_execution_results(execution_results)}
        
        Crée une réponse finale cohérente et complète.
        """
        
        if self.llm_client:
            response = await self.llm_client.generate(
                messages=[{"role": "user", "content": synthesis_prompt}],
                provider="openai"
            )
            return response["content"]
        
        return "Synthèse des résultats d'exécution"
    
    def _parse_goal_tree(self, content: str) -> Dict[str, Any]:
        """Parse la réponse LLM en structure d'arbre d'objectifs."""
        # Implémentation simplifiée - à améliorer selon les besoins
        return {
            "main_goal": "Objectif principal",
            "sub_goals": [
                {"id": "goal_1", "description": "Sous-objectif 1", "priority": 1},
                {"id": "goal_2", "description": "Sous-objectif 2", "priority": 2}
            ],
            "dependencies": []
        }
    
    def _parse_actions(self, content: str, goal_id: str) -> List[Dict[str, Any]]:
        """Parse la réponse LLM en liste d'actions."""
        # Implémentation simplifiée - à améliorer selon les besoins
        return [
            {"id": f"action_1_{goal_id}", "description": "Action 1", "goal_id": goal_id},
            {"id": f"action_2_{goal_id}", "description": "Action 2", "goal_id": goal_id}
        ]
    
    def _format_execution_results(self, results: List[Dict[str, Any]]) -> str:
        """Formate les résultats d'exécution pour la synthèse."""
        formatted = []
        for i, result in enumerate(results, 1):
            status = "✓" if result["success"] else "✗"
            formatted.append(f"{status} Action {i}: {result.get('result', result.get('error', 'N/A'))}")
        return '\n'.join(formatted)
