import numpy as np
import progressbar
import pdb

from components.network import Network
from components.node import Node
from components.synapse import Synapse

from tools.data_generation import generate_data

class Factory():

    def __init__(self, logger, sim_params):
        self.logger = logger
        self.params = sim_params
        self.networks = []

    def generate_synapse(self, pre_node, post_node, init_syn_min, 
                            init_syn_max, base_learn_rate, pre_thresh,
                            post_thresh):

        perms = [np.random.uniform(init_syn_min, init_syn_max) for _ in range(2)]
       
        synapse = Synapse(pre_node, post_node, perms[0], 
                            perms[1], base_learn_rate,
                            pre_thresh, post_thresh)

        post_node.synapses.append(synapse)

    # clean this code up using map()
    def connect_layers(self, pre_layer, post_layer, proportion, 
                        init_syn_min, init_syn_max, base_learn_rate,
                        pre_thresh, post_thresh):
        '''
        loop through all nodes pre and post layers and 
        connect them according to the proportion 
        '''
        for pre_node in pre_layer:
            for post_node in post_layer:
                if pre_node != post_node:
                    prob = np.random.random()
                    if prob < proportion:
                        self.generate_synapse(pre_node, post_node, 
                                              init_syn_min, init_syn_max,
                                              base_learn_rate, pre_thresh,
                                              post_thresh)


    def create_network(self, network_params):
        '''
        generates a network with n_layers, each layer i with layer_ns[i] nodes, connected according to layer connections
        where layer_connections is an array of pairing instructions represented as: [[0]layer pairings, [1]connectivity proportion between layer pair]
        '''
        # generate a new network instance
        network = Network(self.logger)

        # populate the layers with nodes
        network.layers = [[network.create_node(i, network_params['response_function'], 
                            network_params['threshold_function'], network_params['spiking_method'],
                            network_params['base_threshold'], network_params['abs_refrac'],
                            network_params['rel_refrac']) 
                            for _ in range(network_params['layer_ns'][i])] 
                            for i in range(network_params['n_layers'])]

        # connect the layers
        for connection in network_params['layer_connections']:
            self.connect_layers(network.layers[connection[0][0]], 
                network.layers[connection[0][1]], connection[1], 
                network_params['init_syn_min'], network_params['init_syn_max'], 
                network_params['base_learn_rate'], network_params['pre_thresh'],
                network_params['post_thresh'])
        
        # append the network to the factory and return it
        self.networks.append(network)
        return network

    def train_network(self, training_data, network, epochs):
        '''
        run training epochs
        '''
        bar = progressbar.ProgressBar()
        for t in bar(range(epochs)):
            network.training_epoch(t, training_data)

    def run_simulation(self, network):
        '''
        runs the a basic simulation
        --testing if everything works--
        '''
        # create training data and train network
        self.logger.info("Generating Training Data")
        training_data = [
                            generate_data(len(network.layers[0]), 0.25),
                            generate_data(len(network.layers[1]), 0.25),
                            generate_data(len(network.layers[2]), 0.25),
                        ]

        print(training_data[1])

        self.logger.info("Training Network")
        self.train_network(training_data, network, self.params['training_epochs'])
        
        # initialise the simulation
        self.logger.info("Running Simulation")
        network.reset()
        t = 0
        network.direct_activate(t, network.layers[0], training_data[0])
        sim_log = []
        
        # iterate the simulation and store the data
        bar = progressbar.ProgressBar()
        for t in bar(range(self.params['sim_length'])):
            iteration_data = network.iterate(t)
            sim_log.append(iteration_data.copy())

        return sim_log