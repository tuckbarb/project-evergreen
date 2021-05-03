import time

import board
import busio
import digitalio
import storage
import sdioio
import random

import adafruit_sdcard
import adafruit_bmp280
import adafruit_lis3mdl

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Connect to the card and mount the filesystem.
sdcard = sdioio.SDCard(
    clock=board.SDIO_CLOCK,
    command=board.SDIO_COMMAND,
    data=board.SDIO_DATA,
    frequency=25000000)

vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Sensor
sensor_pressure = adafruit_bmp280.Adafruit_BMP280_I2C(board.I2C())
sensor_magnet = adafruit_lis3mdl.LIS3MDL(board.I2C())

# change this to match the location's pressure (hPa) at sea level
sensor_pressure.sea_level_pressure = 1013.25

start_time = time.monotonic_ns()
filename = "/sd/data_" + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(7)) + ".csv"
print("Logging data to sd card at " + filename + " ...")
# append to the file!

while True:
    # open file for append
    with open(filename, "a") as fi:
        ms_duration = round((time.monotonic_ns() - start_time) / 1e6, 1)
        led.value = True  # turn on LED to indicate we're writing to the file
        out_text = f'{ms_duration}, {sensor_pressure.temperature}, {sensor_pressure.pressure}, {sensor_pressure.altitude}\n'

        print(out_text)
        fi.write(out_text)
        led.value = False  # turn off LED to indicate we're done
    # file is saved
    time.sleep(1)
