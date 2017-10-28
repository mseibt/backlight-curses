import os
import subprocess


class State(object):
    def __init__(self, base_increment=3.0, base_path="/sys/class/backlight/intel_backlight/"):
        # read value in
        self.base = base_path

        if base_increment <= 0 \
           or base_increment >= 100 \
           or not isinstance(base_increment, float):
            raise ValueError('base_increment is a float between 0. and 100.')
        self.base_increment = base_increment

        self.actual_brightness = self.read_actual_brightness()
        self.max_brightness = self.read_max_brightness()
        self.percentage = self.actual_brightness / self.max_brightness

    def read_brightness_file(self, name):
        with open(os.path.join(self.base, name), 'r') as f:
            txt = f.read().strip()
        try:
            return float(txt)
        except ValueError:
            return None

    def read_actual_brightness(self):
        """ reads from base/actual_brightness """
        val = self.read_brightness_file('actual_brightness')
        if not val:
            val = 100.
        return val

    def read_max_brightness(self):
        """ reads from base/max_brightness """
        val = self.read_brightness_file('max_brightness')
        if not val:
            val = 100.
        return val

    def lower_brightness(self):
        """ lowers the brightness percentage by base_increment """
        if self.percentage - self.base_increment >= 0:
            self.percentage -= self.base_increment
        else:
            self.percentage = 1.
        self.set_brightness()

    def higher_brightness(self):
        """ highers the brightness percentage by base_increment """
        if self.percentage + self.base_increment <= 100:
            self.percentage += self.base_increment
        else:
            self.percentage = 100.
        self.set_brightness()

    def absolute_brightness(self, percentage):
        """ sets the brightness percentage directly """
        if percentage > 100.:
            self.percentage = 100.
        elif percentage < 1.:
            self.percentage = 1.
        else:
            self.percentage = percentage
        self.set_brightness()

    def set_brightness(self):
        """ sets the brightness to the current percentage """
        val = str(int((self.percentage / 100.) * self.max_brightness))
        command = "echo '{val}' | tee {path}".format(
            val=val,
            path=os.path.join(self.base, 'brightness')
        )
        # print(command)
        subprocess.call(command, shell=True)
