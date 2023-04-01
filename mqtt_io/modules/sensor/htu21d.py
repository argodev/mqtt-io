"""
HTU 21D humidity sensor
"""

from typing import cast

from ...types import ConfigType, SensorValueType
from . import GenericSensor
from ...exceptions import RuntimeConfigError

REQUIREMENTS = ("adafruit-circuitpython-htu21d",)


class Sensor(GenericSensor):
    """
    Implementation of Sensor class for htu21d.
    """

    # temperature in degrees Celsius
    # altidue in meters
    SENSOR_SCHEMA = {
        "type": dict(
            type="string",
            required=False,
            empty=False,
            default="humidity",
            allowed=["humidity", "temperature"],
        )
    }

    def setup_module(self) -> None:
        # pylint: disable=import-outside-toplevel,import-error
        import adafruit_htu21d  # type: ignore
        import board  # type: ignore
        import busio  # type: ignore

        # this is what was in the other file (aht20)
        # i2c = busio.I2C(board.SCL, board.SDA)
        # but this is what adafruit had...
        i2c = board.I2C()
        self.sensor = adafruit_htu21d.HTU21D(i2c)

    @property
    def _temperature(self) -> SensorValueType:
        return cast(SensorValueType, self.sensor.temperature)

    @property
    def _humidity(self) -> SensorValueType:
        return cast(SensorValueType, self.sensor.relative_humidity)


    def get_value(self, sens_conf: ConfigType) -> SensorValueType:
        """
        Get the sensor value from the sensor
        """
        if sens_conf["type"] == "humidity":
            return self._humidity
        if sens_conf["type"] == "temperature":
            return self._temperature
        raise RuntimeConfigError(
            "htu21d sensor '%s' was not configured to return 'humidity', or 'temperature'"
            % sens_conf["name"]
        )
