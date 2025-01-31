"""
The main application class that is executed
"""


from argparse import ArgumentParser, Namespace
from source.file_io import load
from source.qt_emulator import QTEmulator


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

        emulator.initialize_memory()
        emulator.import_code(instruction_tuples)
        # emulator.run()
