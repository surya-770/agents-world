from agents_world.agent.agent import Agent
from agents_world.agent.role import Role

class Crewmate(Agent):
    """Crewmate specific extensions."""
    def __init__(self, id: str, prompt_builder, executor, discussion_sys, voting_sys, suspicion_sys):
        super().__init__(id, Role.CREWMATE, prompt_builder, executor, discussion_sys, voting_sys, suspicion_sys)
