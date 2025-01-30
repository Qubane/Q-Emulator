"""
The main application class that is executed
"""


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

        self.args = parser.parse_args()

    def run(self):
        """
        Runs the application
        """

        # parse args
        self.parse_args()
