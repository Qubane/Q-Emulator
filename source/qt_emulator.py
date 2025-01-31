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

            self._instruction_lookup[opcode](flag, value)

            self.program_counter += 1

    def _unknown_instruction_halt(self, *args):
        """
        Called on any unknown instruction that is called
        Exit code: 400
        """

        self.running = False
        self.exit_code = 400

    def _i000_nop(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        nop - No Operation
        """

        # Do nothing
        pass

    def _i001_load(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        load - Load - Loads VAL into ACC
        """

    def _i002_store(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        store - Store - Stores ACC into address defined by VAL
        """

    def _i003_loadp(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        loadp - Load Pointer - Loads value from cache using ACC as address
        """

    def _i004_loadpr(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        loadpr - Load Pointer Register - Load VAL into PR
        """

    def _i005_storep(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        storep - Store Pointer - Store ACC into address defined by PR
        """

    def _i006_push(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        push - Push - Push ACC onto number stack
        """

    def _i007_pop(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        pop - Pop - Pop ACC from number stack
        """

    def _i008_call(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        call - Call - Pushes current IR into stack; jumps to VAL
        """

    def _i009_return(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        return - Return - Pops value from stack to IR
        """

    def _i010_jump(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        jump - Jump - Unconditional jump to VAL
        """

    def _i011_jumpc(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        jumpc - Jump Condition - Conditional jump to PR; Condition defined by bitmask
        """

    def _i012_clf(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        clf - Clear Flag - Clears flags; Flags are defined by bitmask
        """

    def _i016_and(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        and - And - Bitwise AND with ACC and VAL
        """

    def _i017_or(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        or - Or - Bitwise OR with ACC and VAL
        """

    def _i018_xor(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        xor - Xor - Bitwise XOR with ACC and VAL
        """

    def _i019_lsl(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        lsl - Logical Shift Left - Shifts ACC left VAL times
        """

    def _i020_lsr(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        lsr - Logical Shift Right - Shifts ACC right VAL times
        """

    def _i021_rol(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        rol - Rotate Left - Rotates ACC left VAL times
        """

    def _i022_ror(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        ror - Rotate Right - Rotates ACC right VAL times
        """

    def _i023_comp(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        comp - Compare - Compares ACC and VAL, -1 if ACC < VAL; 0 if ACC == VAL; 1 if ACC > VAL
        """

    def _i032_add(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        add - Add - Add ACC and VAL
        """

    def _i033_sub(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        sub - Add - Subtract VAL from ACC
        """

    def _i034_addc(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        addc - Add Carry - Add ACC and VAL, with carry
        """

    def _i035_subc(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        subc - Sub Carry - Subtract VAL from ACC, with carry
        """

    def _i036_inc(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        inc - Increment - Increment ACC
        """

    def _i037_dec(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        dec - Decrement - Decrement ACC
        """

    def _i038_mul(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        mul - Multiply - Multiply ACC with VAL
        """

    def _i039_div(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        div - Divide - Divide ACC by VAL
        """

    def _i040_mod(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        mod - Modulo - Remainder of division of ACC by VAL
        """

    def _i096_portw(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        portw - Port Write - Writes ACC into port by address VAL
        """

    def _i097_portr(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        portr - Port Read - Reads port by address VAL into ACC
        """

    def _i126_interrupt(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        Exit code: 201
        interrupt - Interrupt - Interrupts execution
        """

        self.running = False
        self.exit_code = 201

    def _i127_halt(self, flag: uint8, value: uint16):
        """
        INSTRUCTION CALL
        Exit code: 100
        halt - Halt - Halts execution
        """

        self.running = False
        self.exit_code = 200
