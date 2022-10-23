import sys
import time
import numpy as np
import argparse
from rltrace.Trace import Trace
from python.organism.basic.BasicEnvVisualiserProxy import BasicEnvVisualiserProxy
from python.visualise.VisualisationAgentProxy import VisualisationAgentProxy


class TestVisualisationProducer:

    def __init__(self):
        self._hours_of_light_per_day: float = 12
        self._hours_since_last_rain: float = 2
        self._basic_env_visualiser_proxy = BasicEnvVisualiserProxy(hours_of_light_per_day=12,
                                                                   hours_since_last_rain=2,
                                                                   num_organisms=10)
        self._trace = Trace()
        parser = argparse.ArgumentParser(description='Test Visualisation')
        VisualisationAgentProxy.add_args(parser)
        args = parser.parse_args()
        self._visualisation_agent_proxy = \
            VisualisationAgentProxy(trace=self._trace,
                                    args=args,
                                    basic_visualiser_env_proxy=self._basic_env_visualiser_proxy)
        return

    def send_updates(self) -> None:
        topic: str = 'visualisation_agent_e5db0744374a44f69cde62cb32ea05e0'
        self._visualisation_agent_proxy.initialise()

        r = np.random.rand(30)
        for i in range(10):
            self._visualisation_agent_proxy.update(frame_index=i,
                                                   frame_data=[
                                                       (r[0], r[1], r[2]),
                                                       (r[3], r[4], r[5]),
                                                       (r[6], r[7], r[8]),
                                                       (r[9], r[10], r[11]),
                                                       (r[12], r[13], r[14]),
                                                       (r[15], r[16], r[17]),
                                                       (r[18], r[19], r[20]),
                                                       (r[21], r[22], r[23]),
                                                       (r[24], r[25], r[26]),
                                                       (r[27], r[28],
                                                        r[29])])
            ru = (np.random.rand(30) - 0.5) * .05
            r = r + ru
            r = np.minimum(np.ones(30), r)
            r = np.maximum(np.zeros(30), r)
            time.sleep(.25)

        self._visualisation_agent_proxy.terminate()
        return


if __name__ == "__main__":
    TestVisualisationProducer().send_updates()
    sys.exit(0)
