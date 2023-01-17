"""
BMP280 temperature, humidity and pressure sensor
"""

from typing import cast

from ...types import ConfigType, SensorValueType
from . import GenericSensor
from ...exceptions import RuntimeConfigError

REQUIREMENTS = ("adafruit-circuitpython-bmp280",)

class Sensor(GenericSensor):
    """
    Implementation of Sensor class for bmp280.
    """

    CONFIG_SCHEMA = {
        "sea_level_pressure": {"type": "float", "required": False, "default": 1021.2}
    }
    # pressure in hPa
    # temperature in degrees Celsius
    # altidue in meters
    SENSOR_SCHEMA = {
        "type": dict(
            type="string",
            required=False,
            empty=False,
            default="pressure",
            allowed=["pressure", "temperature", "altitude"],
        )
    }

    def setup_module(self) -> None:
        # pylint: disable=import-outside-toplevel,import-error
        import adafruit_bmp280  # type: ignore
        import board  # type: ignore
        import busio  # type: ignore

        # this is what was in the other file (aht20)
        #i2c = busio.I2C(board.SCL, board.SDA)
        # but this is what adafruit had... 
        i2c = board.I2C()        
        self.sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        self.sensor.sea_level_pressure = 1021.2 # how do I read this from the file?

    @property
    def _temperature(self) -> SensorValueType:
        return cast(SensorValueType, self.sensor.temperature)

    @property
    def _pressure(self) -> SensorValueType:
        return cast(SensorValueType, self.sensor.pressure)

    @property
    def _altitude(self) -> SensorValueType:
        return cast(SensorValueType, self.sensor.altitude)


    def get_value(self, sens_conf: ConfigType) -> SensorValueType:
        """
        Get the sensor value from the sensor
        """
        if sens_conf["type"] == "pressure":
            return self._pressure
        if sens_conf["type"] == "temperature":
            return self._temperature
        if sens_conf["type"] == "altitude":
            return self._altitude
        raise RuntimeConfigError(
            "bmp280 sensor '%s' was not configured to return 'pressure', 'temperature' or 'altitude'"
            % sens_conf["name"]
        )
