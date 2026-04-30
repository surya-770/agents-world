from abc import ABC, abstractmethod
from agents_world.core.game_state import GameState
from agents_world.core.phase_manager import Phase
from agents_world.agent.role import Role
from agents_world.agent.personality import PersonalityProfile
from agents_world.modules.perception import PerceptionModule
from agents_world.modules.memory import MemorySystem
from agents_world.modules.decision import DecisionEngine
from agents_world.modules.discussion import DiscussionSystem
from agents_world.modules.voting import VotingSystem
from agents_world.modules.suspicion import SuspicionEngine
from agents_world.interface.action_executor import ActionExecutor
from agents_world.llm.prompt_builder import PromptBuilder
from agents_world.utils.logger import logger

class Agent(ABC):
    """Abstract base definition handling sequence orchestration per turn."""
    def __init__(self, id: str, role: Role, prompt_builder: PromptBuilder, executor: ActionExecutor, 
                 discussion_sys: DiscussionSystem, voting_sys: VotingSystem, suspicion_sys: SuspicionEngine):
        self.id = id
        self.role = role
        self.personality = PersonalityProfile.random()
        self.perception = PerceptionModule(self.id, prompt_builder)
        self.memory = MemorySystem(self.id)
        self.decision = DecisionEngine(prompt_builder)
        self.action_executor = executor
        self.discussion_sys = discussion_sys
        self.voting_sys = voting_sys
        self.suspicion_sys = suspicion_sys

    def step(self, game_state: GameState) -> None:
        """Executes full lifecycle for tick loop."""
        if self.id in game_state.dead_agents:
            return
            
        try:
            # 1. OBSERVE
            snapshot = self.perception.capture(game_state)
            # 2. INTERPRET
            events = self.perception.interpret(snapshot, game_state.tick)
            # 3. UPDATE MEMORY
            self.memory.store(events, self.personality.forgetfulness)
            for ev in events:
                self.suspicion_sys.on_event(self.id, ev, game_state)
            
            # 4. DECIDE
            action = self.decision.decide(self.id, self.memory, self.personality, game_state.phase, game_state)
            
            if action.type == "IDLE" or not action.type:
                import random
                rooms = ["Cafeteria", "MedBay", "Electrical", "Storage", "Navigation", "Shields", "O2", "Reactor"]
                # Create a new Action object directly instead of modifying the existing one
                from agents_world.modules.decision import Action
                action = Action(type="MOVE", target=random.choice(rooms))

            # 5. ACT
            self.action_executor.execute(action, self.id, game_state)
            
            if game_state.phase == Phase.DISCUSSION:
                msg = self.discussion_sys.contribute(self.id, self.memory, self.personality, game_state)
                # System automatically logged it via contribute? Or do it directly
                # contribute logic doesn't explicitly guarantee log if caller should. We log directly.
                # Actually earlier discussion_sys did, but we make sure:
                game_state.log_chat(msg.author_id, msg.content)
                
            elif game_state.phase == Phase.VOTING:
                vote_target = self.voting_sys.vote(self.id, self.memory, self.suspicion_sys, self.personality, game_state)
                game_state.record_vote(self.id, vote_target.target)
                
        except Exception as e:
            logger.error(f"Agent {self.id} error during step: {e}")
            if game_state.phase == Phase.VOTING:
                game_state.record_vote(self.id, "SKIP")
