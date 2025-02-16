"""
The main application class that is executed
"""


from source.modules import *
from source.file_io import *
from source.qt_emulator import QTEmulator
from argparse import ArgumentParser, Namespace


class Application:
    """
    Main application class
    """

    def __init__(self):
        self.args: Namespace | None = None

    def parse_args(self):
        """
        Parses command line arguments
        """

        parser = ArgumentParser(prog="Q-Emulator", description="Emulates Quantum CPU's")
        parser.add_argument("-i", "--input",
                            help="binary file",
                            required=True)
        parser.add_argument("--namespace",
                            help="code namespace",
                            choices=["QT", "QM"],
                            default="QT")
        parser.add_argument("-d", "--dump",
                            help="make memory dump with given name")

        self.args = parser.parse_args()

    def run(self):
        """
        Runs the application
        """

        # parse args
        self.parse_args()

        # load instructions
        instruction_tuples = load(self.args.input)

        # define emulator
        if self.args.namespace == "QT":
            emulator = QTEmulator()
        elif self.args.namespace == "QM":
            raise NotImplementedError
        else:
            raise Exception

        # TODO: get rid of this temporary code
        test = ScreenModule(64, 64, "RGB888")
        test.init()

        emulator.initialize_memory()
        emulator.import_code(instruction_tuples)
        while emulator.exit_code != 0:
            emulator.run()

            if emulator.exit_code == 0x80:
                self.module_interrupt()

        if self.args.dump:
            QTEmulatorIO.create_memory_dump(self.args.dump, emulator)

    def module_interrupt(self):
        """
        Process any 0x80 interrupts
        """
