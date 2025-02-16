"""
Interrupt called modules for emulator
"""


import pygame as pg
from numpy import ndarray, uint16


class ScreenModule:
    """
    Screen module
    """

    def __init__(self, width: int, height: int, color_depth: int):
        self.width: int = width
        self.height: int = height
        self.color_depth: int = color_depth

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
