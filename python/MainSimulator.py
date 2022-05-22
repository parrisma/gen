import sys
from BaseArgParser import BaseArgParser
from BasicEnv import BasicEnv
from Conf import Conf


class MainSimulator:
    _verbose: bool
    _config_file: str

    def __init__(self):
        args = self._get_args(description="Run Evolutionary Simulation")
        self._verbose = args.verbose
        self._config_file = args.json
        return

    @staticmethod
    def _get_args(description: str):
        """
        Extract and verify command line arguments
        :param description: The description of the application
        """
        parser = BaseArgParser(description).parser()
        return parser.parse_args()

    def run(self) -> None:
        """
        Boostrap the environment and run the evolutionary simulation.
        """
        while BasicEnv(conf=Conf(self._config_file)).run():
            pass
        return


if __name__ == "__main__":
    MainSimulator().run()
    sys.exit(0)
