from typing import Dict
import concurrent.futures
from base.Env import Env
from BasicOrganism import BasicOrganism
from BasicMetrics import BasicMetrics
from Conf import Conf


class BasicEnv(Env):
    _num_gen_zero_organisms: int
    _population: Dict[str, BasicOrganism]
    _metrics: Dict[str, BasicMetrics]

    def __init__(self,
                 conf: Conf):
        super(BasicEnv, self).__init__()
        self._num_gen_zero_organisms = conf.config["environment"]["num_generation_zero_organisms"]
        self._population = {}
        self._metrics = {}
        return

    def create_generation_zero(self):
        """
        Create the initial generation zero population.
        """
        for _ in range(self._num_gen_zero_organisms):
            o = BasicOrganism()
            self._population[o.get_id_as_str()] = o
        return

    def termination_conditions_met(self) -> bool:
        """
        Evaluate the conditions that indicate the simulation has ended
        :return: True if the conditions to exit run have been met
        """
        return len(self._population) == 0

    def run_population(self) -> None:
        """
        Call the run method on each member of the population
        """
        self._metrics.clear()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(organism) for organism in self._population.values()]

            for f in concurrent.futures.as_completed(results):
                res: BasicMetrics = f.result()
                if not res.is_alive():
                    self._population.pop(res.get_organism_id())
                else:
                    self._metrics[res.get_organism_id()] = res
        return

    def run(self) -> bool:
        """
        Run the evolutionary simulation until termination condition are met
        :return: False if the evolutionary simulation has met termination conditions.
        """
        self.create_generation_zero()

        while not self.termination_conditions_met():
            self.run_population()

        return False
