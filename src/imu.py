"""Standalone IMU reader — prints roll, pitch, yaw and gyroscope data at 2 Hz.

Usage:
    uv run src/imu.py
    make imu
"""

import math
import time

from bmi088 import BMI088
import bmi088.bmi088 as _bmi_module
from constants import IMU_I2C_BUS

# The library default gyro address is 0x69, on our board it's 0x68
_bmi_module.GYRO_ADDRESS = 0x68

imu = BMI088(i2c_bus=IMU_I2C_BUS)

print("IMU (BMI088) — Ctrl-C to stop.")

dt = 0.5
while True:
    w, x, y, z = imu.get_quat(dt)
    roll = math.degrees(math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y)))
    pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2 * (w * y - z * x)))))
    yaw = math.degrees(math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z)))
    gx, gy, gz = imu.read_gyroscope()
    ax, ay, az = imu.read_accelerometer()
    print("--------------------------------------------")
    print(f"IMU:  roll={roll:+.1f}°  pitch={pitch:+.1f}°  yaw={yaw:+.1f}°")
    print(f"Gyro: gx={gx:+.3f}  gy={gy:+.3f}  gz={gz:+.3f} rad/s")
    print(f"Acc:  ax={ax:+.3f}  ay={ay:+.3f}  az={az:+.3f} g")
    time.sleep(dt)
