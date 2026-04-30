from dataclasses import dataclass
from agents_world.core.phase_manager import Phase

@dataclass
class Action:
    """Action to be executed by ActionExecutor."""
    type: str # IDLE, MOVE, USE, KILL, VOTE
    target: str = ""

class DecisionEngine:
    """Agent decision making logic during Task phase."""
    def __init__(self, prompt_builder: 'PromptBuilder'):
        from agents_world.llm.llm_client import LLMClient
        self.llm = LLMClient()
        self.prompt_builder = prompt_builder

    def decide(self, agent_id: str, memory: 'MemorySystem', personality: 'PersonalityProfile', phase: Phase, game_state: 'GameState' = None) -> Action:
        """Computes next action based on memory and personality."""
        summary = memory.get_context_summary(max_tokens=300)
        
        current_room = "Unknown"
        valid_rooms = ["Cafeteria", "MedBay", "Electrical", "Storage", "Navigation", "Shields", "O2", "Reactor"]
        if game_state and agent_id in game_state.agent_locations:
            current_room = game_state.agent_locations[agent_id]
        
        prompt = self.prompt_builder.render("decide", memory_summary=summary, phase=phase.name, current_room=current_room, valid_rooms=", ".join(valid_rooms))
        prompt = self.prompt_builder.apply_personality(prompt, personality)
        
        schema = {
            "type": "object",
            "properties": {
                "action_type": {"type": "string"},
                "target": {"type": "string"}
            },
            "required": ["action_type"]
        }
        
        try:
            result = self.llm.complete_structured(prompt, schema)
            act_type = result.get("action_type", "IDLE")
            target = result.get("target", "")
        except Exception:
            act_type = "IDLE"
            target = ""
        
        return Action(type=act_type.upper(), target=target)
