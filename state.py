import configparser
import os
import subprocess


class BrightnessState(object):
    DEFAULT_BACKLIGHT_PATH = "/sys/class/backlight/intel_backlight"
    DEFAULT_ACTUAL_BRIGHTNESS_FILE = "actual_brightness"
    DEFAULT_ACTUAL_BRIGHTNESS = 755
    DEFAULT_MAX_BRIGHTNESS_FILE = "max_brightness"
    DEFAULT_MAX_BRIGHTNESS = 755
    DEFAULT_BRIGHTNESS_FILE = "brightness"
    DEFAULT_INCREMENT = 5

    def __init__(self, config_path=None):
        self.backlight_path = BrightnessState.DEFAULT_BACKLIGHT_PATH
        self.actual_brightness_file = BrightnessState.DEFAULT_ACTUAL_BRIGHTNESS_FILE
        self.max_brightness_file = BrightnessState.DEFAULT_MAX_BRIGHTNESS_FILE
        self.brightness_file = BrightnessState.DEFAULT_BRIGHTNESS_FILE
        self.increment = BrightnessState.DEFAULT_INCREMENT

        # load config if a config path is provided
        if config_path:
            self.load_config(config_path)

        # get current values
        self.actual_brightness = self.read_actual_brightness()
        self.max_brightness = self.read_max_brightness()

        # Calculate the percentage for the current actual_brightness
        self._percentage = int(100 * (self.actual_brightness / self.max_brightness))

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, percentage):
        """ validates the percentage value and sets it """
        assert type(percentage) is int, "The percentage is not an integer"
        if percentage > 100:
            self._percentage = 100
        elif percentage < 1:
            self._percentage = 1
        else:
            self._percentage = percentage

    def read_brightness_file(self, name):
        """ generic method to read brightness files """
        with open(os.path.join(self.backlight_path, name), 'r') as f:
            txt = f.read().strip()
        try:
            return float(txt)
        except ValueError:
            return None

    def read_actual_brightness(self):
        """ reads from base/actual_brightness """
        val = self.read_brightness_file(self.actual_brightness_file)
        if not val:
            return BrightnessState.DEFAULT_ACTUAL_BRIGHTNESS
        return val

    def read_max_brightness(self):
        """ reads from base/max_brightness """
        val = self.read_brightness_file(self.max_brightness_file)
        if not val:
            return BrightnessState.DEFAULT_MAX_BRIGHTNESS
        return val

    def lower_brightness(self):
        """ lowers the brightness percentage by increment """
        self.percentage -= self.increment
        self.set_brightness()

    def higher_brightness(self):
        """ highers the brightness percentage by increment """
        self.percentage += self.increment
        self.set_brightness()

    def absolute_brightness(self, percentage):
        """ sets the brightness percentage directly """
        self.percentage = percentage
        self.set_brightness()

    def set_brightness(self):
        """ sets the brightness to the current percentage """
        val = str(int((self.percentage / 100.) * self.max_brightness))
        command = "echo '{val}' | tee {path}".format(
            val=val,
            path=os.path.join(self.backlight_path, self.brightness_file)
        )
        subprocess.call(command, shell=True)

    def load_config(self, config_path):
        # TODO: load config
        # - check file existence
        # - read
        # - validate values

        # current_path = os.path.dirname(os.path.realpath(__file__))
        # config_path = os.path.join(current_path, 'config.ini')

        config = configparser.ConfigParser()
        config.read(config_path)
        if 'Brightness' in config.sections():
            pass
            # if base_increment <= 0 \
            #    or base_increment >= 100 \
            #    or not isinstance(base_increment, float):
            #     raise ValueError('base_increment is a float between 0. and 100.')
            # self.base_increment = base_increment

            # self.actual_brightness = self.read_actual_brightness()
            # self.max_brightness = self.read_max_brightness()
