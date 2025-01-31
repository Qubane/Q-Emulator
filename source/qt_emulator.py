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
        self.pointer_register: uint16 = uint16(0)
        self.program_counter: uint16 = uint16(0)
        self.stack_pointer: uint16 = uint16(0)
        self.address_stack_pointer: uint16 = uint16(0)

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

            # if memory flag -> use cache value
            if flag:
                value = self.cache[value]

            # call instruction
            self._instruction_lookup[opcode](flag, value)

            # increment counter
            self.program_counter += 1

    def _unknown_instruction_halt(self, *args):
        """
        Called on any unknown instruction that is called
        Exit code: 400
        """

        self.running = False
        self.exit_code = 400

    def _i000_nop(self, value: uint16):
        """
        INSTRUCTION CALL
        nop - No Operation
        """

        # Do nothing
        pass

    def _i001_load(self, value: uint16):
        """
        INSTRUCTION CALL
        load - Load - Loads VAL into ACC
        """

        self.accumulator = value

    def _i002_store(self, value: uint16):
        """
        INSTRUCTION CALL
        store - Store - Stores ACC into address defined by VAL
        """

        self.cache[value] = self.accumulator

    def _i003_loadp(self, value: uint16):
        """
        INSTRUCTION CALL
        loadp - Load Pointer - Loads value from cache using ACC as address
        """

    def _i004_loadpr(self, value: uint16):
        """
        INSTRUCTION CALL
        loadpr - Load Pointer Register - Load VAL into PR
        """

        self.pointer_register = value

    def _i005_storep(self, value: uint16):
        """
        INSTRUCTION CALL
        storep - Store Pointer - Store ACC into address defined by PR
        """

        self.cache[self.pointer_register] = self.accumulator

    def _i006_push(self, value: uint16):
        """
        INSTRUCTION CALL
        push - Push - Push ACC onto number stack
        """

        self.stack[self.stack_pointer] = self.accumulator
        self.stack_pointer += 1

    def _i007_pop(self, value: uint16):
        """
        INSTRUCTION CALL
        pop - Pop - Pop ACC from number stack
        """

        self.stack_pointer -= 1
        self.accumulator = self.stack[self.stack_pointer]

    def _i008_call(self, value: uint16):
        """
        INSTRUCTION CALL
        call - Call - Pushes current IR into stack; jumps to VAL
        """

        self.address_stack[self.address_stack_pointer] = self.program_counter
        self.address_stack_pointer += 1
        self.program_counter = value

    def _i009_return(self, value: uint16):
        """
        INSTRUCTION CALL
        return - Return - Pops value from stack to IR
        """

        self.address_stack_pointer -= 1
        self.program_counter = self.address_stack[self.address_stack_pointer]

    def _i010_jump(self, value: uint16):
        """
        INSTRUCTION CALL
        jump - Jump - Unconditional jump to VAL
        """

        self.program_counter = value

    def _i011_jumpc(self, value: uint16):
        """
        INSTRUCTION CALL
        jumpc - Jump Condition - Conditional jump to PR; Condition defined by bitmask
        """

        # TODO: conditions

        self.program_counter = self.pointer_register

    def _i012_clf(self, value: uint16):
        """
        INSTRUCTION CALL
        clf - Clear Flag - Clears flags; Flags are defined by bitmask
        """

    def _i016_and(self, value: uint16):
        """
        INSTRUCTION CALL
        and - And - Bitwise AND with ACC and VAL
        """

        self.accumulator = self.accumulator & value

    def _i017_or(self, value: uint16):
        """
        INSTRUCTION CALL
        or - Or - Bitwise OR with ACC and VAL
        """

        self.accumulator = self.accumulator | value

    def _i018_xor(self, value: uint16):
        """
        INSTRUCTION CALL
        xor - Xor - Bitwise XOR with ACC and VAL
        """

        self.accumulator = self.accumulator ^ value

    def _i019_lsl(self, value: uint16):
        """
        INSTRUCTION CALL
        lsl - Logical Shift Left - Shifts ACC left VAL times
        """

        self.accumulator = self.accumulator << value

    def _i020_lsr(self, value: uint16):
        """
        INSTRUCTION CALL
        lsr - Logical Shift Right - Shifts ACC right VAL times
        """

        self.accumulator = self.accumulator >> value

    def _i021_rol(self, value: uint16):
        """
        INSTRUCTION CALL
        rol - Rotate Left - Rotates ACC left VAL times
        """

        carry = self.accumulator >> (self.VALUE_BIT_WIDTH - 1)
        self.accumulator = (self.accumulator << value) + carry

    def _i022_ror(self, value: uint16):
        """
        INSTRUCTION CALL
        ror - Rotate Right - Rotates ACC right VAL times
        """

        carry = (self.accumulator & 1) << (self.VALUE_BIT_WIDTH - 1)
        self.accumulator = (self.accumulator >> value) + carry

    def _i023_comp(self, value: uint16):
        """
        INSTRUCTION CALL
        comp - Compare - Compares ACC and VAL, -1 if ACC < VAL; 0 if ACC == VAL; 1 if ACC > VAL
        """

        if self.accumulator < value:
            self.accumulator = self.VALUE_BIT_WIDTH - 1
        elif self.accumulator == value:
            self.accumulator = 0
        else:
            self.accumulator = 1

    def _i032_add(self, value: uint16):
        """
        INSTRUCTION CALL
        add - Add - Add ACC and VAL
        """

        self.accumulator = self.accumulator + value

    def _i033_sub(self, value: uint16):
        """
        INSTRUCTION CALL
        sub - Add - Subtract VAL from ACC
        """

        self.accumulator = self.accumulator - value

    def _i034_addc(self, value: uint16):
        """
        INSTRUCTION CALL
        addc - Add Carry - Add ACC and VAL, with carry
        """

    def _i035_subc(self, value: uint16):
        """
        INSTRUCTION CALL
        subc - Sub Carry - Subtract VAL from ACC, with carry
        """

    def _i036_inc(self, value: uint16):
        """
        INSTRUCTION CALL
        inc - Increment - Increment ACC
        """

        self.accumulator += 1

    def _i037_dec(self, value: uint16):
        """
        INSTRUCTION CALL
        dec - Decrement - Decrement ACC
        """

    def _i038_mul(self, value: uint16):
        """
        INSTRUCTION CALL
        mul - Multiply - Multiply ACC with VAL
        """

    def _i039_div(self, value: uint16):
        """
        INSTRUCTION CALL
        div - Divide - Divide ACC by VAL
        """

    def _i040_mod(self, value: uint16):
        """
        INSTRUCTION CALL
        mod - Modulo - Remainder of division of ACC by VAL
        """

    def _i096_portw(self, value: uint16):
        """
        INSTRUCTION CALL
        portw - Port Write - Writes ACC into port by address VAL
        """

    def _i097_portr(self, value: uint16):
        """
        INSTRUCTION CALL
        portr - Port Read - Reads port by address VAL into ACC
        """

    def _i126_interrupt(self, value: uint16):
        """
        INSTRUCTION CALL
        Exit code: 201
        interrupt - Interrupt - Interrupts execution
        """

        self.running = False
        self.exit_code = 201

    def _i127_halt(self, value: uint16):
        """
        INSTRUCTION CALL
        Exit code: 100
        halt - Halt - Halts execution
        """

        self.running = False
        self.exit_code = 200
