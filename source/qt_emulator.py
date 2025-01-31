"""
QT Architecture emulator
"""


from typing import Callable
from numpy import uint8, uint16, uint32, zeros, ndarray


class QTEmulator:
    """
    QT CPU Emulator
    """

    ADDRESS_BIT_WIDTH = 16

    def __init__(self):
        # program memory
        self.rom: list[uint32] = list()

        # array memory (cache)
        self.cache: ndarray[uint16] | None = None
        self.stack: ndarray[uint16] | None = None
        self.address_stack: ndarray[uint16] | None = None

        # register memory (registers)
        self.accumulator: uint16 = uint16(0)
        self.program_counter: uint16 = uint16(0)
        self.stack_counter: uint16 = uint16(0)
        self.address_stack_counter: uint16 = uint16(0)

        # instruction lookup table
        self._instruction_lookup: list[Callable] | None = None

    def _make_instruction_lookup(self):
        """
        Generate internal instruction lookup table
        """

        self._instruction_lookup = []

    def initialize_memory(self):
        """
        Initializes memory arrays
        """

        self.rom = zeros(2**self.ADDRESS_BIT_WIDTH, dtype=uint32)
        self.cache = zeros(2**self.ADDRESS_BIT_WIDTH, dtype=uint16)
        self.stack = zeros(2**self.ADDRESS_BIT_WIDTH, dtype=uint16)
        self.address_stack = zeros(2**self.ADDRESS_BIT_WIDTH, dtype=uint16)

    def import_code(self, instructions: list[tuple[int, int, int]]):
        """
        Imports instructions into ROM
        :param instructions: list of instruction tuples
        """

        for idx, instruction in enumerate(instructions):
            memory_flag = uint8((instruction[0]) & 1)
            value = uint16(instruction[1])
            opcode = uint8(instruction[2])

            # M VVVV`VVVV`VVVV`VVVV OOO`OOOO
            self.rom[idx] = uint32((memory_flag << 23) + (value << 7) + opcode)

    def run(self):
        """
        Executes imported code
        """

        while True:
            flag = self.rom[self.program_counter] >> 23
            value = (self.rom[self.program_counter] >> 7) & 65535
            opcode = self.rom[self.program_counter] & 127


