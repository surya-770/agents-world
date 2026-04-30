from agents_world.core.game_state import GameState
from agents_world.modules.perception import GameEvent
from agents_world.utils.helpers import Config
from typing import Dict

class SuspicionEngine:
    """Updates and decays suspicion metrics across game events."""
    def __init__(self):
        self.decay_rate = Config().get("game.suspicion_decay_rate", 0.05)
        
    def on_event(self, observer_id: str, event: GameEvent, game_state: GameState) -> None:
        """Process event and update suspicion matrix."""
        observer = game_state.agents.get(observer_id)
        if not observer:
            return
            
        target = self._extract_target(event.details, game_state.alive_agents)
        if not target:
            return

        delta = 0.0
        reason = event.type
        
        if event.type == "KILL_WITNESSED":
            delta = 1.0 # Immediately to 1.0 logic in agent memory handler or here
            observer.memory.update_suspicion(target, 1.0, reason)
            return
        elif event.type == "BODY_FOUND":
            delta = 0.3
        elif event.type == "PLAYER_SEEN_ALONE_IN_RESTRICTED":
            delta = 0.15
        elif event.type == "ALIBI_CONFIRMED":
            delta = -0.2
            
        if delta != 0.0:
            observer.memory.update_suspicion(target, delta, reason)

    def _extract_target(self, details: str, valid_agents: list[str]) -> str:
        for a in valid_agents:
            if a in details:
                return a
        return ""

    def decay(self, agent_id: str, game_state: 'GameState') -> None:
        """Applies suspicion decay rate per tick."""
        agent = game_state.agents.get(agent_id)
        if not agent:
            return
            
        for target, score in list(agent.memory.suspicion_scores.items()):
            if score > 0:
                agent.memory.update_suspicion(target, -self.decay_rate, "tick_decay")

    def get_top_suspect(self, agent_id: str, game_state: 'GameState', exclude_self: bool = True) -> str:
        """Retrieves top suspect from memory."""
        agent = game_state.agents.get(agent_id)
        if not agent:
            return ""
            
        best_target = ""
        highest_score = -1.0
        for target, score in agent.memory.suspicion_scores.items():
            if exclude_self and target == agent_id:
                continue
            if score > highest_score:
                highest_score = score
                best_target = target
        return best_target
