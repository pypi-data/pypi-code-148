from BirdBrain import Hummingbird
import math, time

class HummingbirdJoystick:
    DEFAULT_ROTATION = 0
    ROTATION_CCW_0 = DEFAULT_ROTATION
    ROTATION_CCW_1 = 1
    ROTATION_CCW_2 = 2
    ROTATION_CCW_3 = 3
    SLICE_COUNT = 8
    SPEED_CALIBRATION_BASE = 1.30
    SPEED_CALIBRATION_BIAS = 0.10
    SPEED_MINIMUM = 20.0
    SPEED_MAXIMUM = 100.0
    SPEED_MAXIMUM_BIAS = 10.0
    BUTTON_NOISE = 0.1

    def __init__(self, device = None, rotation = None):
        self.device = device
        self.rotation = rotation
        self.calibrate_max_speed = HummingbirdJoystick.SPEED_CALIBRATION_BASE
        self.calibrate_x = [ -HummingbirdJoystick.SPEED_CALIBRATION_BASE, HummingbirdJoystick.SPEED_CALIBRATION_BASE ]
        self.calibrate_y = [ -HummingbirdJoystick.SPEED_CALIBRATION_BASE, HummingbirdJoystick.SPEED_CALIBRATION_BASE ]

        self.button_base = 0.0
        self.x_base = 0.0
        self.y_base = 0.0

        if self.rotation is None: self.rotation = HummingbirdJoystick.DEFAULT_ROTATION

        try:
            self.joy_stick = Hummingbird(device)

            self.calibrate()
        except ConnectionRefusedError:
            print("Joystick device not available")
            raise

    def calibrate(self):
        self.button_base = self.joy_stick.getVoltage(1)
        self.x_base = self.joy_stick.getVoltage(2)
        self.y_base = self.joy_stick.getVoltage(3)

    def calibrate_xy(self, x, y):
        if x < self.calibrate_x[0]: self.calibrate_x[0] = x
        if x > self.calibrate_x[1]: self.calibrate_x[1] = x
        if y < self.calibrate_y[0]: self.calibrate_y[0] = y
        if y > self.calibrate_y[1]: self.calibrate_y[1] = y

    def raw_values(self):
        x = self.joy_stick.getVoltage(2) - self.x_base
        y = self.joy_stick.getVoltage(3) - self.y_base
        button = max(0.0, self.joy_stick.getVoltage(1) - self.x_base - HummingbirdJoystick.BUTTON_NOISE)
        return [ self.clean_value(-x), self.clean_value(y), self.clean_value(button) ]

    def values(self, speed_mimimum = SPEED_MINIMUM):
        x, y, button = self.raw_values()

        if self.rotation == HummingbirdJoystick.ROTATION_CCW_1:
            x, y = -y, x
        elif self.rotation == HummingbirdJoystick.ROTATION_CCW_2:
            x, y = -x, -y
        elif self.rotation == HummingbirdJoystick.ROTATION_CCW_3:
            x, y = y, -x

        x = self.clean_value(x)
        y = self.clean_value(y)

        is_button_selected = True if button > 1.0 else False

        angle = math.atan2(x, y) / math.pi * 180
        if angle < 0.0: angle = 360 + angle

        raw_speed = max(abs(x), abs(y))
        if (raw_speed > self.calibrate_max_speed): self.calibrate_max_speed = raw_speed - HummingbirdJoystick.SPEED_CALIBRATION_BIAS

        speed = HummingbirdJoystick.SPEED_MAXIMUM - ((self.calibrate_max_speed - raw_speed) * HummingbirdJoystick.SPEED_MAXIMUM)
        speed = speed + HummingbirdJoystick.SPEED_MAXIMUM_BIAS
        if speed < speed_mimimum: speed = 0.0
        if speed > HummingbirdJoystick.SPEED_MAXIMUM: speed = HummingbirdJoystick.SPEED_MAXIMUM

        return(x, y, is_button_selected, self.clean_value(angle), self.clean_value(speed))

    def direction(self, slice_size = SLICE_COUNT):
        x, y, is_button_selected, angle, speed = self.values()

        slice_size = 360.0 / slice_size
        half_slice_size = slice_size / 2.0

        angle_for_calculation = angle
        if (angle + half_slice_size) > 360.00: angle_for_calculation = 0

        direction = int((angle_for_calculation + half_slice_size) / slice_size)

        return(direction, speed, is_button_selected)

    def normalize(self, xy, calibrate_xy):
        if xy <= 0.0:
            return(self.clean_value(-(xy / calibrate_xy[0]) * 100))
        else:
            return(self.clean_value((xy / calibrate_xy[1]) * 100))

    def normalized_xy(self):
        x, y, button = self.raw_values()

        is_button_selected = True if button > 1.0 else False

        self.calibrate_xy(x, y)

        normalized_x = self.normalize(x, self.calibrate_x)
        normalized_y = self.normalize(y, self.calibrate_y)

        return(normalized_x, normalized_y, is_button_selected)

    def clean_value(self, x_or_y):
        return(x_or_y + 0.0)
