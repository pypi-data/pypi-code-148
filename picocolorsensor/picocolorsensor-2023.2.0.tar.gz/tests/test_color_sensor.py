import picocolorsensor


def test_ctor():
    color_sensor = picocolorsensor.PicoColorSensor()
    assert color_sensor
