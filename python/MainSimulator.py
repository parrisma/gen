import sys
from BaseArgParser import BaseArgParser
from SimpleEnv import SimpleEnv
from Conf import Conf
from organism.basic.BasicOrganismFactory import BasicOrganismFactory
from organism.basic.BasicSelector import BasicSelector


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
        SimpleEnv(conf=Conf(self._config_file),
                  organism_factory=BasicOrganismFactory(),
                  selector=BasicSelector()).run()
        return


if __name__ == "__main__":
    MainSimulator().run()
    sys.exit(0)
