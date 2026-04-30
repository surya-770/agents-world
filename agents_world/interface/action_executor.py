from agents_world.modules.decision import Action
from agents_world.interface.game_interface import GameInterface

class ActionExecutor:
    """Translates Action signals from DecisionEngine into interface events."""
    def __init__(self, interface: GameInterface):
        self.interface = interface
        
    def execute(self, action: Action, agent_id: str = None, game_state: 'GameState' = None) -> None:
        """Fires mapped functions relative to intent type."""
        if action.type == "MOVE":
            self.interface.move_to(action.target, agent_id, game_state)
        elif action.type == "USE":
            self.interface.interact_with_task(action.target, agent_id, game_state)
        elif action.type == "KILL":
            self.interface.kill_target(action.target)
        elif action.type in ["IDLE", "VOTE", "SKIP"]:
            pass # Abstracted to discrete subphases or ignored
