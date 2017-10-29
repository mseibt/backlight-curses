#!/usr/bin/env python3

import sys

from ui import ui
from state import BrightnessState


if __name__ == "__main__":
    if len(sys.argv) > 1:
        brightness_state = BrightnessState(sys.argv[1])
    else:
        brightness_state = BrightnessState()
    ui(brightness_state)
