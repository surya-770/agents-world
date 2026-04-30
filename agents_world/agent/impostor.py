from agents_world.agent.agent import Agent
from agents_world.agent.role import Role

class Impostor(Agent):
    """Impostor specific extensions and predispositions."""
    def __init__(self, id: str, prompt_builder, executor, discussion_sys, voting_sys, suspicion_sys):
        super().__init__(id, Role.IMPOSTOR, prompt_builder, executor, discussion_sys, voting_sys, suspicion_sys)
        # Ensure deception is strictly augmented for Impostor strategy 
        self.personality.deception = max(self.personality.deception, 0.7)
