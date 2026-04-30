import pytest
from agents_world.modules.suspicion import SuspicionEngine
from agents_world.core.game_state import GameState
from agents_world.agent.crewmate import Crewmate
from agents_world.modules.perception import GameEvent

class MockAgent:
    def __init__(self, id):
        self.id = id
        from agents_world.modules.memory import MemorySystem
        self.memory = MemorySystem(id)

def test_suspicion_witness_kill():
    engine = SuspicionEngine()
    gs = GameState()
    gs.agents["A1"] = MockAgent("A1")
    gs.alive_agents = ["A1", "A2"]
    
    ev = GameEvent("KILL_WITNESSED", "A2 killed A3", 1)
    engine.on_event("A1", ev, gs)
    
    assert gs.agents["A1"].memory.suspicion_scores["A2"] == 1.0

def test_suspicion_decay():
    engine = SuspicionEngine()
    engine.decay_rate = 0.1
    gs = GameState()
    gs.agents["A1"] = MockAgent("A1")
    gs.agents["A1"].memory.suspicion_scores["A2"] = 0.5
    
    engine.decay("A1", gs)
    
    assert gs.agents["A1"].memory.suspicion_scores["A2"] == 0.4
