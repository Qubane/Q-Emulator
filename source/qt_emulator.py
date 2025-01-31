"""
QT Architecture emulator
"""


from ctypes import c_uint8, c_uint16, c_uint32


class QTEmulator:
    """
    QT CPU Emulator
    """

    ADDRESS_BIT_WIDTH = 16

    def __init__(self):
        # program memory
        self.rom: list[c_uint32] = list()

        # array memory (cache)
        self.cache: list[c_uint16] = list()
        self.stack: list[c_uint16] = list()
        self.address_stack: list[c_uint16] = list()

        # register memory (registers)
        self.accumulator: c_uint16 = c_uint16(0)
        self.program_counter: c_uint16 = c_uint16(0)
        self.stack_counter: c_uint16 = c_uint16(0)
        self.address_stack_counter: c_uint16 = c_uint16(0)

    def initialize_memory(self):
        """
        Initializes memory arrays
        """

        self.rom = [c_uint16(0) for _ in range(2**self.ADDRESS_BIT_WIDTH)]
        self.cache = [c_uint16(0) for _ in range(2**self.ADDRESS_BIT_WIDTH)]
        self.stack = [c_uint16(0) for _ in range(2**self.ADDRESS_BIT_WIDTH)]
        self.address_stack = [c_uint16(0) for _ in range(2**self.ADDRESS_BIT_WIDTH)]

    def import_code(self, instructions: list[tuple[int, int, int]]):
        """
        Imports instructions into ROM
        :param instructions: list of instruction tuples
        """

        for idx, instruction in enumerate(instructions):
            memory_flag = c_uint8((instruction[0]) & 1)
            value = c_uint16(instruction[1])
            opcode = c_uint8(instruction[2])

            # M VVVV`VVVV`VVVV`VVVV OOO`OOOO
            self.rom[idx] = c_uint32((memory_flag.value << 23) + (value.value << 7) + opcode.value)
