"""
File reading and writing implementations.
"""


from source.qt_emulator import QTEmulator


def load(filepath: str) -> list[tuple[int, int, int]]:
    """
    Reads binary executable file, compiled by Q-Compiler
    :param filepath: executable filepath
    :return: list of instruction tuples
    """

    instructions = list()
    with open(filepath, "rb") as file:
        namespace = b''  # namespace header
        while (char := file.read(1)) != b'\x00':
            namespace += char

        # read and decode instructions
        while True:
            if namespace == b'QT':
                raw_instruction = file.read(4)
            elif namespace == b'QM':
                raw_instruction = file.read(3)
            else:
                raise Exception
            if not raw_instruction:
                break

            memory_flag = raw_instruction[0] & 1
            value = int.from_bytes(raw_instruction[1:3])
            opcode = raw_instruction[3]

            instructions.append((memory_flag, value, opcode))
    return instructions


class QTEmulatorIO:
    """
    File IO for QTEmulator
    """

    @staticmethod
    def create_memory_dump(filepath: str, emulator: QTEmulator):
        """
        Creates a memory dump
        """

        offset = 16
        index_offset = 4
        added_offset = 3
        number_offset = 5
        with open(filepath, "w", encoding="ASCII") as file:
            # cache dump
            file.write("[CACHE START]\n")
            file.write(" " * (index_offset + added_offset))
            for i in range(offset):
                file.write(f"{i: {number_offset}d} ")
            for index in range(0, len(emulator.cache), offset):
                file.write(
                    "\n" +
                    f"{index:0{index_offset}d} | " +
                    " ".join(f"{val:0{number_offset}d}" for val in emulator.cache[index:index+offset]))
            file.write("\n[CACHE END]")
