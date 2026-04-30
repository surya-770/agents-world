import pytest
from agents_world.core.orchestrator import SimulationOrchestrator

def test_orchestrator_spawns_agents():
    orch = SimulationOrchestrator()
    assert len(orch.game_state.agents) == orch.config.get("simulation.num_agents")
    
    impostors = [a for a in orch.game_state.agents.values() if a.role.name == "IMPOSTOR"]
    assert len(impostors) == orch.config.get("simulation.num_impostors")

def test_agent_loop_runs_without_crashing():
    orch = SimulationOrchestrator()
    orch.max_rounds = 1 # Force fast limit
    # Just ensure we can crank the main loop safely over one phase check
    orch.run()
    assert orch.clock.current_tick > 0
