from agents_world.core.game_state import GameState
from agents_world.core.phase_manager import PhaseManager, Phase
from agents_world.core.clock import SimulationClock
from agents_world.utils.helpers import Config
from agents_world.utils.logger import logger
from agents_world.llm.prompt_builder import PromptBuilder
from agents_world.interface.action_executor import ActionExecutor
from agents_world.interface.game_interface import GameInterface
from agents_world.modules.discussion import DiscussionSystem
from agents_world.modules.voting import VotingSystem
from agents_world.modules.suspicion import SuspicionEngine
from agents_world.modules.communication import CommunicationSystem
from agents_world.agent.crewmate import Crewmate
from agents_world.agent.impostor import Impostor
import random

class SimulationOrchestrator:
    """Manages full lifecycle of the simulation process."""
    def __init__(self):
        self.config = Config()
        self.game_state = GameState()
        self.clock = SimulationClock()
        self.phase_manager = PhaseManager(self.config.get("game.discussion_duration_ticks", 5))
        
        self.prompt_builder = PromptBuilder()
        self.game_interface = GameInterface()
        self.executor = ActionExecutor(self.game_interface)
        self.discussion_sys = DiscussionSystem(self.prompt_builder)
        self.voting_sys = VotingSystem(self.prompt_builder)
        self.suspicion_sys = SuspicionEngine()
        self.communication_sys = CommunicationSystem()
        
        self.max_rounds = self.config.get("simulation.max_rounds", 5)
        self._spawn_agents()

    def _spawn_agents(self) -> None:
        num_agents = self.config.get("simulation.num_agents", 8)
        num_impostors = self.config.get("simulation.num_impostors", 2)
        
        roles = [True]*num_impostors + [False]*(num_agents - num_impostors)
        random.shuffle(roles)
        
        for i in range(num_agents):
            agent_id = f"Agent_{i+1}"
            if roles[i]:
                agent = Impostor(agent_id, self.prompt_builder, self.executor, self.discussion_sys, self.voting_sys, self.suspicion_sys)
            else:
                agent = Crewmate(agent_id, self.prompt_builder, self.executor, self.discussion_sys, self.voting_sys, self.suspicion_sys)
            
            self.game_state.agents[agent_id] = agent
            self.game_state.alive_agents.append(agent_id)
            self.game_state.agent_locations[agent_id] = "Cafeteria"
            
        logger.info(f"Initialized {num_agents} agents ({num_impostors} Impostors).")

    def run(self) -> None:
        logger.info("Simulation initialized. Starting main loop...")
        
        rounds = 0
        while self.phase_manager.current_phase != Phase.ENDED and rounds < self.max_rounds:
            logger.info(f"--- Tick {self.clock.current_tick} | Phase: {self.phase_manager.current_phase.name} ---")
            
            agents_order = list(self.game_state.alive_agents)
            random.shuffle(agents_order)
            
            for agent_id in agents_order:
                agent = self.game_state.agents[agent_id]
                agent.step(self.game_state)
                
            self.communication_sys.flush()
            
            for agent_id in self.game_state.alive_agents:
                self.suspicion_sys.decay(agent_id, self.game_state)

            if self.phase_manager.current_phase == Phase.VOTING:
                eliminated = self.voting_sys.tally(self.game_state)
                if eliminated:
                    logger.info(f"Agent {eliminated} was eliminated by vote.")
                    role = self.game_state.agents[eliminated].role.name
                    logger.info(f"{eliminated} was an {role}.")
                else:
                    logger.info("Voting tied or skipped. No one eliminated.")
                self.phase_manager.set_phase(Phase.TASK)
                rounds += 1
                logger.info(f"Round {rounds}/{self.max_rounds} concluded.")

            self._check_win_condition()
            
            self.phase_manager.advance()
            self.clock.advance()
            self.game_state.tick = self.clock.current_tick
            self.game_state.phase = self.phase_manager.current_phase

    def _check_win_condition(self) -> None:
        impostors = sum(1 for a in self.game_state.alive_agents if self.game_state.agents[a].role.name == "IMPOSTOR")
        crewmates = len(self.game_state.alive_agents) - impostors
        
        if impostors == 0:
            logger.info("Win Condition: CREWMATES WIN.")
            self.phase_manager.set_phase(Phase.ENDED)
        elif impostors >= crewmates:
            logger.info("Win Condition: IMPOSTORS WIN.")
            self.phase_manager.set_phase(Phase.ENDED)
