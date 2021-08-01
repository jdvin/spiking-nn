import argparse
import logging
import concurrent.futures
import matplotlib

from factory import Factory

from tools.visualisation import visualise_sim, graph_sim

from config import coreParameters

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
# parser.add_argument('test_type', type=str, help='Which type of test would you like to perform?')
# parser.add_argument('param_type', type=str, help='Would you like to run the test with the core or grid parameters?')
# args = parser.parse_args()
# ttype = args.test_type
# ptype = args.param_type

if __name__ == '__main__':    
    logger.info("=== jdvin Spiking Neural Network Testbed ===")
    network = factory.create_network(coreParameters.model)
    sim_logs = factory.run_simulation(network)
    visualise_sim(sim_logs)
    graph_sim(sim_logs)

