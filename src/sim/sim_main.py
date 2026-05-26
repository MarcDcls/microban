"""Local simulation entry point — never deployed to the robot.

Usage:
    uv run --group sim src/sim/sim_main.py --mjcf path/to/robot.xml
    make sim                          # uses default model/scene.xml
    make sim MJCF=path/to/robot.xml
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
    parser.add_argument("--mjcf", metavar="PATH", required=True, help="Path to the MJCF scene file")
    parser.add_argument("--hz", type=float, default=50.0, metavar="FREQ", help="Scheduler frequency in Hz (default: 50)")
    args = parser.parse_args()

    input_source = MuJoCoInputSource(move_keys={"h": "head", "w": "walk"})
    controller = MuJoCoController(
        args.mjcf,
        key_callback=input_source.key_callback,
        reset_source=input_source,
    )

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
