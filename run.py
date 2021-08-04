import argparse
import logging
import concurrent.futures
import matplotlib

from factory import Factory

from tools.visualisation import visualise_sim, graph_sim

from config import coreParameters, simulations

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s\t=> %(message)s')
logger = logging.getLogger()
if logger.hasHandlers(): logger.handlers.clear()
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

factory = Factory(logger, coreParameters.simulation)

# Parse arguments
parser = argparse.ArgumentParser(description='''
Main initalisation file. 
Run this to kick off the whole process.
''')
parser.add_argument('sim_name', type=str, help='The name of the simulation to be run')
args = parser.parse_args()
try:
    sim = simulations.sim_table[args.sim_name]
except KeyError:
    raise Exception(f'simulation {args.sim_name} not recognised')

if __name__ == '__main__':    
    logger.info("=== jdvin Spiking Neural Network Testbed ===")
    network = factory.create_network(coreParameters.model)
    sim_logs = factory.run_simulation(sim, network)
    visualise_sim(sim_logs)
    graph_sim(sim_logs)

