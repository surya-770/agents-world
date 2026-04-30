import argparse
from agents_world.core.orchestrator import SimulationOrchestrator
from agents_world.utils.helpers import Config

def merge_args_to_config(args):
    """Syncs CLI overrides to singleton config."""
    config = Config()
    if args.agents:
        config.settings.setdefault("simulation", {})["num_agents"] = args.agents
    if args.impostors:
        config.settings.setdefault("simulation", {})["num_impostors"] = args.impostors
    if args.rounds:
        config.settings.setdefault("simulation", {})["max_rounds"] = args.rounds

def main():
    """Main execution point for standard entry."""
    parser = argparse.ArgumentParser(description="Agents World Simulation")
    parser.add_argument("--agents", type=int, help="Number of agents")
    parser.add_argument("--impostors", type=int, help="Number of impostors")
    parser.add_argument("--rounds", type=int, help="Maximum rounds")
    args = parser.parse_args()

    merge_args_to_config(args)
    
    orchestrator = SimulationOrchestrator()
    orchestrator.run()
    
    # Summary requirement format block
    print("\n" + "="*40)
    print("SIMULATION SUMMARY")
    print("="*40)
    print(f"Total Ticks: {orchestrator.clock.current_tick}")
    print(f"Surviving Agents: {len(orchestrator.game_state.alive_agents)}")
    print(f"Dead Agents: {len(orchestrator.game_state.dead_agents)}")
    
    impostors = sum(1 for a in orchestrator.game_state.alive_agents if orchestrator.game_state.agents[a].role.name == "IMPOSTOR")
    if impostors == 0:
        print("WINNER: CREWMATES")
    elif impostors >= (len(orchestrator.game_state.alive_agents) - impostors):
        print("WINNER: IMPOSTORS")
    else:
        print("WINNER: DRAW / ROUND LIMIT REACHED")

if __name__ == "__main__":
    main()
