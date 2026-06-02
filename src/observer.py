from dataclasses import dataclass, field
import time

from controller import ControllerProtocol
from input.input_source import UserInput
from constants import MOTOR_TO_ID


@dataclass
class RobotState:
    """Hardware sensor readings for one scheduler iteration."""

    time_s: float = 0.0
    acc: list[float] = field(default_factory=list)
    gyro: list[float] = field(default_factory=list)
    quat: list[float] = field(default_factory=list)
    motor_angles: dict[str, float] = field(default_factory=dict)


@dataclass
class Observation:
    """Full observation passed through the move pipeline each tick."""

    robot_state: RobotState = field(default_factory=RobotState)
    user_input: UserInput = field(default_factory=UserInput)


class Observer:
    def __init__(self, controller: ControllerProtocol):
        self.controller = controller
        self._last_imu_warn_s: float = 0.0
        self._imu_warn_interval_s: float = 1.0

    def read_state(self, dt: float) -> RobotState:
        """Read current motor positions from the controller."""
        state = RobotState(time_s=time.perf_counter())

        motor_names = list(MOTOR_TO_ID.keys())
        motor_ids = list(MOTOR_TO_ID.values())
        angles = self.controller.sync_read_present_position(motor_ids)
        state.motor_angles = dict(zip(motor_names, angles))

        try:
            state.acc = list(self.controller.read_acc())
            state.gyro = list(self.controller.read_gyro())
            state.quat = list(self.controller.read_quat(dt))
        except Exception as exc:
            now = time.perf_counter()
            if (now - self._last_imu_warn_s) >= self._imu_warn_interval_s:
                print(f"Warning: observer IMU read failed: {exc}", end="\r\n", flush=True)
                self._last_imu_warn_s = now

        return state

