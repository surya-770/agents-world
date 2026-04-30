class SimulationClock:
    """Manages the current tick of the simulation."""
    
    def __init__(self):
        self.tick: int = 0
        
    def advance(self) -> None:
        """Advances the clock by one tick."""
        self.tick += 1
        
    def reset(self) -> None:
        """Resets the clock to zero."""
        self.tick = 0
        
    @property
    def current_tick(self) -> int:
        """Returns the current tick."""
        return self.tick
