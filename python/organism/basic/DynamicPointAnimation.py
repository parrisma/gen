import numpy as np
from typing import Tuple, Union, Callable, List
from python.visualise.PointAnimationData import PointAnimationData
from python.base.Organism import Organism
from python.base.Genome import Genome
from python.organism.basic.genes.LightToleranceGene import LightToleranceGene
from python.organism.basic.genes.DroughtToleranceGene import DroughtToleranceGene
from python.base.Gene import Gene
from python.organism.basic.BasicEnvironmentState import BasicEnvironmentState
from python.organism.basic.BasicEnvironmentAttributes import BasicEnvironmentAttributes


class DynamicPointAnimation(PointAnimationData):
    """
    Supply on the fly animation data for 3D Points.
    """

    def __init__(self,
                 env_state: Union[BasicEnvironmentState, Callable[[], BasicEnvironmentState]]):
        self._state = env_state
        return

    def extract_points(self) -> np.ndarray:
        """
        Extract the gene values for each organism as they represent the x,y point update for the animation
        """
        state = self._state
        if isinstance(state, Callable):
            state = state()

        organisms: List[Organism] = state.get(BasicEnvironmentAttributes.POPULATION)
        points: np.ndarray = np.zeros((len(organisms), 2))
        idx: int = 0
        for organism in organisms:
            genome = organism.get_genome()
            gene: Gene = None  # NOQA
            for gene in Genome.gene_list(genome=genome):
                if isinstance(gene, LightToleranceGene):
                    points[idx][0] = gene.value()
                if isinstance(gene, DroughtToleranceGene):
                    points[idx][1] = gene.value()
            idx += 1
        return points

    def get_data_for_frame(self,
                           frame_idx: int) -> np.ndarray:
        """
        For each point Add random +/- noise of the defined step size and clip to the x, y, z defined ranges
        :param frame_idx: not used.
        :return: the updated points
        """
        return self.extract_points()

    def num_frames(self) -> int:
        """
        The max number of data frames that will be returned.
        :return: MAX_INT as this is dynamic / on the fly there is no defined end frame.
        """
        return PointAnimationData.INF_POINTS

    def frame_data_shape(self) -> Tuple:
        """
        The data frame is the x,y coordinate to be re-calculated, so shape is 2,
        :return: Tuple(2) as frame is simple two float values for x,y
        """
        return (2,)  # NOQA
