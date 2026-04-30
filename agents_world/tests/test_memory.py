import pytest
from agents_world.modules.memory import MemorySystem
from agents_world.modules.perception import GameEvent

def test_memory_store_and_retrieve():
    mem = MemorySystem("Agent_Test")
    events = [GameEvent("BODY_FOUND", "Found near electrical", 1)]
    mem.store(events, forgetfulness_rate=0.0)
    assert len(mem.events) == 1
    
    summary = mem.get_context_summary(max_tokens=300)
    assert "BODY_FOUND" in summary

def test_memory_forgetfulness():
    mem = MemorySystem("Agent_Test")
    events = [GameEvent("BODY_FOUND", "Found near electrical", 1)]
    mem.store(events, forgetfulness_rate=1.0) # guaranteed drop
    assert len(mem.events) == 0

def test_suspicion_update():
    mem = MemorySystem("Agent_Test")
    mem.update_suspicion("Target", 0.5, "test")
    assert mem.suspicion_scores["Target"] == 0.5
    mem.update_suspicion("Target", 0.6, "test")
    assert mem.suspicion_scores["Target"] == 1.0 # Clamps to max 1.0
