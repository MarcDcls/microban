"""Local simulation entry point — never deployed to the robot.

Usage:
    uv run --group sim src/sim/sim_main.py --hz 50
    make sim 
"""

import argparse

from scheduler import Scheduler
from sim.mujoco_input import MuJoCoInputSource
from sim.mujoco_controller import MuJoCoController
from moves.rotate_head import RotateHeadMove
from moves.squat import SquatMove
from moves.walk import WalkMove


def main() -> None:
    parser = argparse.ArgumentParser(description="Run microban scheduler in MuJoCo simulation.")
    parser.add_argument("--hz", type=float, default=50.0, metavar="FREQ", help="Scheduler frequency in Hz (default: 50)")
    parser.add_argument("--delay-motor", type=int, default=0, metavar="TICKS", help="Motor position/velocity read delay in ticks (default: 1 tick = 20 ms at 50 Hz)")
    parser.add_argument("--delay-imu", type=int, default=0, metavar="TICKS", help="IMU gyro/quat read delay in ticks (default: 1 tick= 20 ms at 50 Hz)")
    args = parser.parse_args()

    input_source = MuJoCoInputSource(move_keys={"h": "head", "s": "squat", "v": "walk"})
    controller = MuJoCoController(
        mjcf_path="src/model/mjcf/scene.xml",
        key_callback=input_source.key_callback,
        reset_source=input_source,
        delay_motor_ticks=args.delay_motor,
        delay_imu_ticks=args.delay_imu,
    )
    input_source.set_viewer_opt(controller.viewer_opt)

    scheduler = Scheduler(
        frequency_hz=args.hz,
        controller=controller,
        input_source=input_source,
        moves={
            "head": RotateHeadMove(),
            "squat": SquatMove(),
            "walk": WalkMove(controller=controller),
        },
    )
    scheduler.run()


if __name__ == "__main__":
    main()
