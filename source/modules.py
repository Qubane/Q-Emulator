"""
Interrupt called modules for emulator
"""


class ScreenModule:
    """
    Screen module
    """

    def __init__(self, width: int, height: int, color_depth: int):
        self.width: int = width
        self.height: int = height
        self.color_depth: int = color_depth
