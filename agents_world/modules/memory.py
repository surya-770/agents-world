from collections import deque
from typing import List, Dict
from agents_world.modules.perception import PerceptionSnapshot, GameEvent
from agents_world.core.game_state import ChatMessage, VoteRecord
from agents_world.utils.logger import logger
from agents_world.utils.helpers import Config
import random

class MemorySystem:
    """Manages an agent's memory and knowledge base."""
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        config = Config()
        max_obs = config.get("game.memory_max_observations", 50)
        self.observations: deque = deque(maxlen=max_obs)
        self.events: List[GameEvent] = []
        self.suspicion_scores: Dict[str, float] = {}
        self.chat_history: List[ChatMessage] = []
        self.voting_history: List[VoteRecord] = []
        self.inferred_beliefs: Dict[str, str] = {}
        self.forgetfulness = 0.0

    def store(self, events: List[GameEvent], forgetfulness_rate: float = 0.0) -> None:
        """Stores new events, subject to forgetfulness probability."""
        self.forgetfulness = forgetfulness_rate
        for ev in events:
            if random.random() < forgetfulness_rate:
                logger.debug(f"[{self.agent_id}] forgot event {ev.type}")
                continue
                
            self.events.append(ev)
            if ev.type in ["KILL_WITNESSED", "BODY_FOUND"]:
                # Simplistic belief update
                pass 
                
    def update_suspicion(self, target_id: str, delta: float, reason: str) -> None:
        """Modifies suspicion score for another agent."""
        if target_id not in self.suspicion_scores:
            self.suspicion_scores[target_id] = 0.0
        old_score = self.suspicion_scores[target_id]
        new_score = max(0.0, min(1.0, old_score + delta))
        self.suspicion_scores[target_id] = new_score
        logger.debug(f"[{self.agent_id}] Updated suspicion of {target_id}: {old_score:.2f} -> {new_score:.2f} ({reason})")

    def get_context_summary(self, max_tokens: int) -> str:
        """Generates ranked summary of memory."""
        recent = self.events[-10:]
        summary = "Recent events:\n"
        for ev in recent:
            summary += f"- [Tick {ev.tick}] {ev.type}: {ev.details}\n"
        return summary[:int(max_tokens * 4)] # Approx chars per token
