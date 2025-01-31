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

    VALUE_BIT_WIDTH = ADDRESS_BIT_WIDTH
    OPCODE_BIT_WIDTH = 7

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

        # misc fields
        self.running: bool = False
        self.exit_code: int = 0

        # instruction lookup table
        self._instruction_lookup: list[Callable] | None = None
        self._make_instruction_lookup()

    def _make_instruction_lookup(self):
        """
        Generate internal instruction lookup table
        """

        self._instruction_lookup = [self._unknown_instruction_halt for _ in range(2**self.OPCODE_BIT_WIDTH)]
        for field in self.__dir__():
            attr = getattr(self, field)
            if not attr.__doc__:
                continue
            if attr.__doc__.find("INSTRUCTION CALL") > -1:
                self._instruction_lookup[int(field[2:5])] = attr

    def _unknown_instruction_halt(self):
        """
        Called on any unknown instruction that is called
        Exit code: 400
        """

        self.running = False
        self.exit_code = 400

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
            memory_flag = instruction[0]
            value = instruction[1]
            opcode = instruction[2]

            # M VVVV`VVVV`VVVV`VVVV OOO`OOOO
            self.rom[idx] = uint32((memory_flag << 23) + (value << 7) + opcode)

    def run(self):
        """
        Executes imported code
        """

        self.running = True
        while self.running:
            flag = uint8(self.rom[self.program_counter] >> 23)
            value = uint16((self.rom[self.program_counter] >> 7))
            opcode = uint8(self.rom[self.program_counter] & 127)

    def _i000_nop(self):
        """
        INSTRUCTION CALL
        NOP - No Operation
        """

        # Do nothing
        pass
