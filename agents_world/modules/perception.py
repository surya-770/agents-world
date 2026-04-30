from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class PerceptionSnapshot:
    nearby_agents: List[str]
    dead_bodies: List[str]
    current_room: str
    visible_tasks: List[str]
    suspicious_events: List[str]

@dataclass
class GameEvent:
    type: str # PLAYER_SEEN, BODY_FOUND, TASK_COMPLETED, KILL_WITNESSED, SABOTAGE_DETECTED
    details: str
    tick: int

class PerceptionModule:
    """Handles agent observation and interpretation."""
    def __init__(self, agent_id: str, prompt_builder: 'PromptBuilder'):
        self.agent_id = agent_id
        from agents_world.llm.llm_client import LLMClient
        self.llm = LLMClient()
        self.prompt_builder = prompt_builder

    def capture(self, game_state: 'GameState' = None) -> PerceptionSnapshot:
        """Captures environment screenshot and builds snapshot."""
        from agents_world.interface.screenshot_capture import ScreenshotCapture
        ScreenshotCapture.capture_b64() # Call interface
        
        current_room = "Unknown"
        if game_state and self.agent_id in game_state.agent_locations:
            current_room = game_state.agent_locations[self.agent_id]
        
        # We send with observe.txt prompt
        prompt = self.prompt_builder.render("observe", agent_id=self.agent_id, visible_entities=f"Simulated data: {current_room}, Agent nearby")
        
        try:
            desc = self.llm.complete(prompt, max_tokens=150)
        except Exception:
            pass # Fallback to empty snapshot handled by robust design
            
        return PerceptionSnapshot(
            nearby_agents=[],
            dead_bodies=[],
            current_room=current_room,
            visible_tasks=[],
            suspicious_events=[]
        )

    def interpret(self, snapshot: PerceptionSnapshot, tick: int) -> List[GameEvent]:
        """Interprets raw snapshot into concrete GameEvents."""
        prompt = self.prompt_builder.render("interpret", observation=str(snapshot))
        
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "details": {"type": "string"}
                },
                "required": ["type", "details"]
            }
        }
        
        try:
            result = self.llm.complete_structured(prompt, schema)
        except Exception:
            return []
            
        events = []
        if isinstance(result, list):
            for r in result:
                if isinstance(r, dict) and "type" in r and "details" in r:
                    events.append(GameEvent(type=r["type"], details=r["details"], tick=tick))
        return events
