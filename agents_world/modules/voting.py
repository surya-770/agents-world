from agents_world.core.game_state import GameState, VoteRecord
from typing import Optional
from agents_world.utils.logger import logger

class VoteTarget:
    """Wrapper for vote target result."""
    def __init__(self, target: str):
        self.target = target # can be 'SKIP'

class VotingSystem:
    """Handles parsing vote formats and aggregating consensus."""
    def __init__(self, prompt_builder: 'PromptBuilder'):
        from agents_world.llm.llm_client import LLMClient
        self.llm = LLMClient()
        self.prompt_builder = prompt_builder

    def vote(self, agent_id: str, memory: 'MemorySystem', suspicion_engine: 'SuspicionEngine', personality: 'PersonalityProfile', game_state: GameState) -> VoteTarget:
        """Uses LLM to decide on a vote target based on suspicion scores."""
        top_suspect = suspicion_engine.get_top_suspect(agent_id, game_state, exclude_self=True)
        # Convert map to string
        suspects_str = ", ".join([f"{k}: {v:.2f}" for k, v in memory.suspicion_scores.items() if v > 0.1])
        
        prompt = self.prompt_builder.render("vote", suspects=suspects_str, reasoning_history="None")
        prompt = self.prompt_builder.apply_personality(prompt, personality)
        
        schema = {
            "type": "object",
            "properties": {
                "vote": {"type": "string"},
                "reason": {"type": "string"}
            },
            "required": ["vote", "reason"]
        }
        
        try:
            result = self.llm.complete_structured(prompt, schema)
            target = result.get("vote", "SKIP")
        except Exception:
            target = "SKIP"
            
        if target not in game_state.alive_agents and target != "SKIP":
            target = "SKIP"
            
        return VoteTarget(target)

    def tally(self, game_state: GameState) -> Optional[str]:
        """Calculates majority vote for current tick, handles ties."""
        counts = {}
        target_tick = game_state.tick
        for r in game_state.vote_record:
            if r.tick == target_tick:
                counts[r.target_id] = counts.get(r.target_id, 0) + 1
        
        if not counts: return None
        
        highest_votes = max(counts.values())
        leaders = [k for k, v in counts.items() if v == highest_votes]
        
        logger.info(f"Vote Tally phase results: {counts}")
        
        if len(leaders) == 1 and leaders[0] != "SKIP":
            game_state.eliminate_agent(leaders[0])
            return leaders[0]
            
        return None
