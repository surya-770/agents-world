from dataclasses import dataclass
import random

@dataclass
class PersonalityProfile:
    """Defines agent baseline behavior metrics."""
    honesty: float
    aggression: float
    passivity: float
    deception: float
    forgetfulness: float
    bias: float

    @staticmethod
    def random() -> 'PersonalityProfile':
        """Generates a profile with values sampled from a Dirichlet distribution."""
        alphas = [1.0] * 6
        samples = [random.gammavariate(a, 1) for a in alphas]
        total = sum(samples)
        normalized = [s / total for s in samples]
        
        return PersonalityProfile(
            honesty=normalized[0],
            aggression=normalized[1],
            passivity=normalized[2],
            deception=normalized[3], # Deception matters mostly for impostors
            forgetfulness=normalized[4],
            bias=normalized[5]
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PersonalityProfile):
            return NotImplemented
        return (self.honesty == other.honesty and
                self.aggression == other.aggression and
                self.passivity == other.passivity and
                self.deception == other.deception and
                self.forgetfulness == other.forgetfulness and
                self.bias == other.bias)
