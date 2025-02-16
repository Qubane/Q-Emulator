"""
Interrupt called modules for emulator
"""


import pygame as pg
from enum import IntEnum
from numpy import ndarray, uint16


class ColorMode(IntEnum):
    BW = 1          # black and white
    BW8 = 8         # 8 bit grayscale
    RGB565 = 16     # 16 bit RGB565
    RGB888 = 24     # 24 bit RGB


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

        self.screen: pg.Surface | None = None

    def init(self):
        """
        init screen
        """

        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))

    def update(self):
        """
        Updates events
        """

        for event in pg.event.get():
            pass

    def blit_array(self, array: ndarray[uint16], start: int):
        """
        Blits a slice of array to screen
        :param array: cache array
        :param start: slice start
        """

        if self.color_mode is ColorMode.BW:         # black and white
            self._blit_bw(array, start)
        elif self.color_mode is ColorMode.BW8:      # grayscale
            self._blit_bw8(array, start)
        elif self.color_mode is ColorMode.RGB565:   # rgb565
            self._blit_rgb565(array, start)
        elif self.color_mode is ColorMode.RGB888:   # rgb888
            self._blit_rgb888(array, start)

    def _blit_bw(self, array: ndarray[uint16], start: int):
        """
        Blits a slice of array to screen in BW color mode
        """

    def _blit_bw8(self, array: ndarray[uint16], start: int):
        """
        Blits a slice of array to screen in grayscale color mode
        """

    def _blit_rgb565(self, array: ndarray[uint16], start: int):
        """
        Blits a slice of array to screen in RGB565 color mode
        """

    def _blit_rgb888(self, array: ndarray[uint16], start: int):
        """
        Blits a slice of array to screen in RGB888 color mode
        """
