from enum import Enum, auto

class Phase(Enum):
    TASK = auto()
    DISCUSSION = auto()
    VOTING = auto()
    ENDED = auto()

class PhaseManager:
    """Manages game phase transitions."""
    
    def __init__(self, discussion_duration: int = 5):
        self.current_phase: Phase = Phase.TASK
        self.discussion_duration: int = discussion_duration
        self.phase_ticks: int = 0

    def set_phase(self, new_phase: Phase) -> None:
        """Transitions to a new phase and resets phase tick counter."""
        self.current_phase = new_phase
        self.phase_ticks = 0

    def advance(self) -> None:
        """Advances phase state. Called every tick by orchestrator."""
        self.phase_ticks += 1
        # Auto-transition from discussion to voting
        if self.current_phase == Phase.DISCUSSION and self.phase_ticks >= self.discussion_duration:
            self.set_phase(Phase.VOTING)
            
    def is_ended(self) -> bool:
        """Returns true if the game phase is ENDED."""
        return self.current_phase == Phase.ENDED
