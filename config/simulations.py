import numpy as np
import progressbar
import pdb

from components.network import Network
from components.node import Node
from components.synapse import Synapse

from tools.data_generation import generate_data, unpopulate_vector

def sim1(factory, network):
    '''
    runs a basic simulation
    --testing if everything works--
    '''
    # create training data and train network
    factory.logger.info("Generating Training Data")
    training_data = [
                        generate_data(1, len(network.layers[0]), 0.25, 0)[0],
                        generate_data(1, len(network.layers[1]), 0.25, 0)[0],
                        generate_data(1, len(network.layers[2]), 0.25, 0)[0],
                    ]

    # testing data is an incomplete version of the first layer training data
    # displays content addressible memory properties of NNs
    testing_data = unpopulate_vector(training_data[0].copy(), 5)

    factory.logger.info("Training Network")
    factory.train_network(training_data, network, factory.params['training_epochs'])
    
    # initialise the simulation
    factory.logger.info("Running Simulation")
    network.reset()
    t = 0
    network.direct_activate(t, network.layers[0], testing_data)
    sim_log = []
    
    # iterate the simulation and store the data
    bar = progressbar.ProgressBar()
    for t in bar(range(factory.params['sim_length'])):
        iteration_data = network.iterate(t)
        sim_log.append(iteration_data.copy())

    return sim_log

sim_table = {
    'sim1':sim1
}
