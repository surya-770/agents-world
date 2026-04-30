import pytest
from agents_world.modules.voting import VotingSystem
from agents_world.core.game_state import GameState

def test_voting_tally_majority():
    sys = VotingSystem(None)
    gs = GameState()
    gs.alive_agents = ["A1", "A2", "A3"]
    
    gs.record_vote("A1", "A3")
    gs.record_vote("A2", "A3")
    gs.record_vote("A3", "A1")
    
    eliminated = sys.tally(gs)
    assert eliminated == "A3"
    assert "A3" in gs.dead_agents
    assert "A3" not in gs.alive_agents

def test_voting_tally_tie():
    sys = VotingSystem(None)
    gs = GameState()
    gs.alive_agents = ["A1", "A2"]
    
    gs.record_vote("A1", "A2")
    gs.record_vote("A2", "A1")
    
    eliminated = sys.tally(gs)
    assert eliminated is None
    assert len(gs.dead_agents) == 0
