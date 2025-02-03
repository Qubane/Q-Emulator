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
    with open(filepath, "rb") as filepath:
        namespace = b''  # namespace header
        while (char := filepath.read(1)) != b'\x00':
            namespace += char

        # read and decode instructions
        while True:
            if namespace == b'QT':
                raw_instruction = filepath.read(4)
            elif namespace == b'QM':
                raw_instruction = filepath.read(3)
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


