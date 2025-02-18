"""
Interrupt called modules for emulator
"""


import pygame as pg
from enum import IntEnum
from numpy import ndarray
from source.qt_emulator import QTEmulator


class ColorMode(IntEnum):
    BW = 1          # black and white
    BW8 = 8         # 8 bit grayscale
    RGB565 = 16     # 16 bit RGB565
    RGB888 = 24     # 24 bit RGB


class ModuleLinker:
    """
    Links emulator to modules
    """

    def __init__(self, emulator):
        self.emulator: QTEmulator = emulator

        self.screen_module: ScreenModule | None = None

    def process_syscall(self):
        """
        Processes CPU syscall interrupts
        """

        # [MODULE INDEX] - port 0
        # 1. screen
        match self.emulator.ports[0]:
            case 1:  # screen
                self._process_screen()
            case _:
                pass

    def exit(self):
        """
        Correctly stops modules
        """

        if self.screen_module:
            self.screen_module.stop()

    def _init_screen_module(self):
        """
        Initializes screen module
        """

        # [WIDTH | HEIGHT] - port 1
        width = self.emulator.ports[1] >> 8
        height = self.emulator.ports[1] & 0xFF

        # [MODE] - port 2
        # 1. BW
        # 8. BW8
        # 16. RGB565
        # 24. RGB888
        mode = self.emulator.ports[2]

        if mode == 1:
            mode = "BW"
        elif mode == 8:
            mode = "BW8"
        elif mode == 16:
            mode = "RGB565"
        elif mode == 24:
            mode = "RGB888"
        else:
            mode = "BW8"

        self.screen_module = ScreenModule(width, height, mode)
        self.screen_module.init()

    def _process_screen(self):
        """
        Processes any screen module related calls
        """

        # if screen module is not initializes -> initialize it and return
        if self.screen_module is None:
            self._init_screen_module()
            return

        # [START] - port 1
        # pointer to location in cache where screen data starts
        start = self.emulator.ports[1]

        self.screen_module.blit_array(self.emulator.cache, start)
        self.screen_module.update()


class ScreenModule:
    """
    Screen module
    """

    def __init__(self, width: int, height: int, color_mode: str):
        """
        :param width: screen width
        :param height: screen height
        :param color_mode: color mode (BW, BW8, RGB565, RGB888)
        """

        self.width: int = width
        self.height: int = height
        self.color_mode: ColorMode = getattr(ColorMode, color_mode)

        self.running: bool = False

        self._real_screen: pg.Surface | None = None
        self.fake_screen: pg.Surface | None = None

    def init(self):
        """
        init screen
        """

        pg.init()
        self._real_screen = pg.display.set_mode(
            (self.width, self.height),
            pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
        self.fake_screen = self._real_screen.copy()
        self.running = True

    def stop(self):
        """
        Stops the screen module
        """

        pg.quit()
        self.running = False

    def update(self):
        """
        Updates events
        """

        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.VIDEORESIZE:
                self._real_screen = pg.display.set_mode(
                    size=event.size,
                    flags=pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)

    def blit_array(self, array: ndarray, start: int):
        """
        Blits a slice of array to screen
        :param array: cache array
        :param start: slice start
        """

        self._real_screen.fill(0)  # clear display
        if self.color_mode is ColorMode.BW:         # black and white
            self._blit_bw(array, start)
        elif self.color_mode is ColorMode.BW8:      # grayscale
            self._blit_bw8(array, start)
        elif self.color_mode is ColorMode.RGB565:   # rgb565
            self._blit_rgb565(array, start)
        elif self.color_mode is ColorMode.RGB888:   # rgb888
            self._blit_rgb888(array, start)

    def _blit_bw(self, array: ndarray, start: int):
        """
        Blits a slice of array to screen in BW color mode
        """

        for y in range(self.height):
            for x in range(self.width):
                true_index = x + y * self.width
                index = true_index // 16
                value = array[start + index]

                if value & (1 << (true_index % 16)) > 0:
                    pg.draw.line(self._real_screen, (255, 255, 255), (x, y), (x, y))
                else:
                    pass

    def _blit_bw8(self, array: ndarray, start: int):
        """
        Blits a slice of array to screen in grayscale color mode
        """

        for y in range(self.height):
            for x in range(self.width):
                index = (x + y * self.width) // 2
                value = array[start + index]
                color = (value & (0xFF << (x % 2))) >> (x % 2)
                pg.draw.line(self._real_screen, (color, color, color), (x, y), (x, y))

    def _blit_rgb565(self, array: ndarray, start: int):
        """
        Blits a slice of array to screen in RGB565 color mode
        """

        for y in range(self.height):
            for x in range(self.width):
                index = x + y * self.width
                value = array[start + index]

                red = value >> 11
                green = (value >> 5) & 0b111111
                blue = value & 0b11111

                pg.draw.line(self._real_screen, (red, green, blue), (x, y), (x, y))

    def _blit_rgb888(self, array: ndarray, start: int):
        """
        Blits a slice of array to screen in RGB888 color mode
        """

        for y in range(self.height):
            for x in range(self.width):
                true_index = x + y * self.width
                index = true_index * 2

                if true_index % 2 == 0:
                    # [RED | GREEN] [BLUE | ...]
                    rg = array[start + index]
                    b = array[start + index + 1]

                    red = rg >> 8
                    green = rg & 0xFF
                    blue = b >> 8
                else:
                    # [... | RED] [GREEN | BLUE]
                    r = array[start + index - 1]
                    gb = array[start + index]

                    red = r & 0xFF
                    green = gb >> 8
                    blue = gb & 0xFF

                pg.draw.line(self._real_screen, (red, green, blue), (x, y), (x, y))
