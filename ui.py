import curses

from state import BrightnessState


def draw_menu(stdscr):
    """ inspired by https://gist.github.com/claymcleod/b670285f334acd56ad1c"""

    k = 0
    brightness_state = BrightnessState()

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k in [curses.KEY_DOWN, curses.KEY_LEFT]:
            brightness_state.lower_brightness()
        elif k in [curses.KEY_UP, curses.KEY_RIGHT]:
            brightness_state.higher_brightness()

        # Title
        title = "Brightness Level"

        # Value
        val = str(brightness_state.percentage) + "%"

        # Centering calculations
        start_x_title = width // 2 - len(title) // 2
        start_x_val = width // 2 - len(val) // 2
        start_y = height // 2

        # Rendering title
        stdscr.attron(curses.color_pair(1))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(start_y - 1, start_x_title, title)
        stdscr.attroff(curses.color_pair(1))
        stdscr.attroff(curses.A_BOLD)

        # Rendering value
        stdscr.addstr(start_y + 1, start_x_val, val)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()


def ui():
    curses.wrapper(draw_menu)
