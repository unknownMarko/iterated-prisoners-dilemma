from enum import Enum
import random


class Action(Enum):
    COOPERATE = "C"
    DEFECT = "D"


C = Action.COOPERATE
D = Action.DEFECT


class Strategy:
    name = "Base Strategy"

    def __init__(self):
        self.reset()

    def reset(self):
        self.my_history = []
        self.opponent_history = []

    def choose(self):
        raise NotImplementedError

    def record_round(self, my_action, opponent_action):
        self.my_history.append(my_action)
        self.opponent_history.append(opponent_action)

    def __repr__(self):
        return self.name


# --- Known strategies ---

class AlwaysCooperate(Strategy):
    name = "Always Cooperate"

    def choose(self):
        return C


class AlwaysDefect(Strategy):
    name = "Always Defect"

    def choose(self):
        return D


class TitForTat(Strategy):
    name = "Tit For Tat"

    def choose(self):
        if not self.opponent_history:
            return C
        return self.opponent_history[-1]


class Random(Strategy):
    name = "Random"

    def choose(self):
        return random.choice([C, D])


class PeriodicDDC(Strategy):
    name = "Periodic DDC"

    def choose(self):
        pattern = [D, D, C]
        return pattern[len(self.my_history) % len(pattern)]


class PeriodicCCD(Strategy):
    name = "Periodic CCD"

    def choose(self):
        pattern = [C, C, D]
        return pattern[len(self.my_history) % len(pattern)]


class Grudger(Strategy):
    """Cooperates until the opponent defects once, then always defects."""
    name = "Grudger"

    def reset(self):
        super().reset()
        self.angry = False

    def choose(self):
        if self.angry:
            return D
        return C

    def record_round(self, my_action, opponent_action):
        super().record_round(my_action, opponent_action)
        if opponent_action == D:
            self.angry = True


class SuspiciousTitForTat(Strategy):
    """Like Tit For Tat, but defects on the first move."""
    name = "Suspicious Tit For Tat"

    def choose(self):
        if not self.opponent_history:
            return D
        return self.opponent_history[-1]


class Pavlov(Strategy):
    """Win-Stay, Lose-Shift. Cooperates on the first move.
    If the previous round payoff was good (CC or DC), repeats the action.
    If it was bad (CD or DD), switches."""
    name = "Pavlov"

    def choose(self):
        if not self.my_history:
            return C
        last_mine = self.my_history[-1]
        last_theirs = self.opponent_history[-1]
        # "Win" = both cooperated or I defected and they cooperated
        if last_mine == last_theirs:
            return C
        return D


# --- Custom strategy ---

class ForgivingTitForTat(Strategy):
    """Custom strategy: like Tit For Tat, but only retaliates if the opponent
    defected in BOTH of the last 2 rounds. This forgives single defections
    and breaks out of defection spirals more easily."""
    name = "Forgiving TFT (custom)"

    def choose(self):
        if len(self.opponent_history) < 2:
            return C
        if self.opponent_history[-1] == D and self.opponent_history[-2] == D:
            return D
        return C


ALL_STRATEGIES = [
    TitForTat,
    AlwaysCooperate,
    AlwaysDefect,
    Random,
    PeriodicDDC,
    PeriodicCCD,
    Grudger,
    SuspiciousTitForTat,
    Pavlov,
    ForgivingTitForTat,
]
