from typing import Dict, List, Any
from dataclasses import dataclass
from agents_world.core.phase_manager import Phase

@dataclass
class BodyReport:
    reporter_id: str
    target_id: str
    tick: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BodyReport): return NotImplemented
        return self.reporter_id == other.reporter_id and self.target_id == other.target_id and self.tick == other.tick

@dataclass
class ChatMessage:
    author_id: str
    content: str
    tick: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChatMessage): return NotImplemented
        return self.author_id == other.author_id and self.content == other.content and self.tick == other.tick

@dataclass
class VoteRecord:
    voter_id: str
    target_id: str  # Can be empty string or 'SKIP'
    tick: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VoteRecord): return NotImplemented
        return self.voter_id == other.voter_id and self.target_id == other.target_id and self.tick == other.tick

class GameState:
    """Single source of truth for the simulation state."""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}  # Forward reference resolved at runtime
        self.alive_agents: List[str] = []
        self.dead_agents: List[str] = []
        self.phase: Phase = Phase.TASK
        self.tick: int = 0
        self.body_reports: List[BodyReport] = []
        self.task_progress: Dict[str, bool] = {}
        self.chat_log: List[ChatMessage] = []
        self.vote_record: List[VoteRecord] = []
        self.agent_locations: Dict[str, str] = {}

    def report_body(self, reporter_id: str, target_id: str) -> None:
        """Registers a body report."""
        self.body_reports.append(BodyReport(reporter_id, target_id, self.tick))

    def complete_task(self, task_id: str) -> None:
        """Marks a task as completed."""
        self.task_progress[task_id] = True

    def log_chat(self, author_id: str, content: str) -> None:
        """Appends a chat message to the log."""
        self.chat_log.append(ChatMessage(author_id, content, self.tick))

    def record_vote(self, voter_id: str, target_id: str) -> None:
        """Records a vote cast by an agent."""
        self.vote_record.append(VoteRecord(voter_id, target_id, self.tick))

    def eliminate_agent(self, agent_id: str) -> None:
        """Moves an agent from alive to dead list."""
        if agent_id in self.alive_agents:
            self.alive_agents.remove(agent_id)
            self.dead_agents.append(agent_id)

    def move_agent(self, agent_id: str, new_location: str) -> None:
        """Updates an agent's current room/location."""
        self.agent_locations[agent_id] = new_location
