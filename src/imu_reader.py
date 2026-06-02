import threading
import time
from dataclasses import dataclass

from bmi088 import BMI088
import bmi088.bmi088 as _bmi_module


# Python defaults: ACC=0x18, GYRO=0x69
# Our board according to the rust driver: ACC=0x19, GYRO=0x68
_bmi_module.ACC_ADDRESS = 0x19
_bmi_module.GYRO_ADDRESS = 0x68


@dataclass(frozen=True)
class IMUSnapshot:
    timestamp_s: float
    quat: tuple[float, float, float, float]
    gyro: tuple[float, float, float]
    acc: tuple[float, float, float]
    valid: bool
    error_count: int


class ThreadedIMUReader:
    """Reads BMI088 on a dedicated thread and exposes the latest sample snapshot."""

    def __init__(self, i2c_bus: int, frequency_hz: float = 200.0, warn_interval_s: float = 1.0) -> None:
        if frequency_hz <= 0:
            raise ValueError("frequency_hz must be > 0")

        self._imu = BMI088(i2c_bus=i2c_bus)
        self._period_s = 1.0 / frequency_hz
        self._warn_interval_s = warn_interval_s

        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run_loop, name="imu-reader", daemon=True)

        now = time.perf_counter()
        self._snapshot = IMUSnapshot(
            timestamp_s=now,
            quat=(1.0, 0.0, 0.0, 0.0),
            gyro=(0.0, 0.0, 0.0),
            acc=(0.0, 0.0, 0.0),
            valid=False,
            error_count=0,
        )

        self._error_count = 0
        self._last_warn_s = 0.0

    def start(self) -> None:
        if not self._thread.is_alive():
            self._thread.start()

    def stop(self, timeout_s: float = 1.0) -> None:
        self._stop_event.set()
        if self._thread.is_alive():
            self._thread.join(timeout=timeout_s)

    def get_latest(self) -> IMUSnapshot:
        with self._lock:
            return self._snapshot

    def get_status(self) -> dict[str, float | int | bool]:
        snap = self.get_latest()
        now = time.perf_counter()
        return {
            "valid": snap.valid,
            "age_s": max(0.0, now - snap.timestamp_s),
            "error_count": snap.error_count,
            "target_frequency_hz": 1.0 / self._period_s,
        }

    def _run_loop(self) -> None:
        next_tick = time.perf_counter()
        last_tick = next_tick

        while not self._stop_event.is_set():
            now = time.perf_counter()
            dt = max(1e-4, now - last_tick)
            last_tick = now

            try:
                w, x, y, z = self._imu.get_quat(dt)
                gx, gy, gz = self._imu.read_gyroscope()
                ax, ay, az = self._imu.read_accelerometer()
                with self._lock:
                    self._snapshot = IMUSnapshot(
                        timestamp_s=now,
                        quat=(float(w), float(x), float(y), float(z)),
                        gyro=(float(gx), float(gy), float(gz)),
                        acc=(float(ax), float(ay), float(az)),
                        valid=True,
                        error_count=self._error_count,
                    )
            except Exception as exc:
                self._error_count += 1
                if (now - self._last_warn_s) >= self._warn_interval_s:
                    print(f"Warning: IMU read failed ({self._error_count}): {exc}", end="\r\n", flush=True)
                    self._last_warn_s = now
                with self._lock:
                    prev = self._snapshot
                    self._snapshot = IMUSnapshot(
                        timestamp_s=prev.timestamp_s,
                        quat=prev.quat,
                        gyro=prev.gyro,
                        acc=prev.acc,
                        valid=prev.valid,
                        error_count=self._error_count,
                    )

            next_tick += self._period_s
            sleep_s = next_tick - time.perf_counter()
            if sleep_s > 0:
                time.sleep(sleep_s)
            else:
                # Reset cadence anchor when late to avoid accumulating drift.
                next_tick = time.perf_counter()