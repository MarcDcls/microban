import onnxruntime as ort

from observer import Observation
from moves.move import MotorCommand, Move


class WalkMove(Move):
    """Walk using a RL policy trained in simulation."""

    def __init__(self) -> None:
        super().__init__()

    def step(self, obs: Observation, command: MotorCommand) -> None:
        pass