from components.node import Node
import random as rand
import pdb

class Network():

    def __init__(self, logger):
        self.logger = logger
        
        self.layers = []
        self.all_nodes = []

    def reset(self):
        '''
        clear all nodes firing histories
        '''
        [node.reset() for node in self.all_nodes]

    def get_state(self, t):
        '''
        returns the binary state for each node in the network by layer at t
        '''
        network_states = {'spiking': [], 'potential': [], 'threshold': []}

        for layer in self.layers:
            layer_states = {'spiking': [], 'potential': [], 'threshold': []}
            for node in layer:
                layer_states['spiking'].append(node.firing_history[t])
                layer_states['potential'].append(node.potential)
                layer_states['threshold'].append(node.threshold)
            
            [network_states[key].append(layer_states[key].copy()) for key in network_states]
        #       [key][layer][node]
        return network_states

    def create_node(self, layer, response_function, threshold_function, 
                    spiking_method, base_threshold, abs_refrac, rel_refrac):
        '''
        create a node, append it to all nodes, and return it
        '''
        node = Node(layer, response_function, threshold_function, 
                    spiking_method, base_threshold, abs_refrac, rel_refrac)

        self.all_nodes.append(node)
        
        return node 

    def direct_activate(self, t, layer, activation_pattern):
        '''
        directly activate the nodes on layer with activation_pattern at t
        '''
        for i,node in enumerate(layer):
            if activation_pattern[i]:
                node.last_fired = t
                node.firing_history.append(1)
            else:
                node.firing_history.append(0)
            
    def train_node_synapses(self, t, node):
        '''
        train all the synapses on node according to the hebbian rule at t
        '''
        for synapse in node.synapses:
            # if at least one of the nodes were active
            if synapse.pre_node.last_fired == t or synapse.post_node.last_fired == t:
                # train the excitatory and inhibitory synapses with their respective valences
                # ensure that the synapses dont go negative
                synapse.excit_perm = max(0, synapse.excit_perm + synapse.delta(t, valence=1))
                synapse.inhib_perm = max(0, synapse.inhib_perm + synapse.delta(t, valence=-1))


    def training_epoch(self, t, training_data):
        '''
        activate the network with the current training data and then train each node
        with the hebbian rule
        '''
        # map the training data to the network
        [self.direct_activate(t, layer, training_data[i]) for i,layer in enumerate(self.layers)]
        # train network on current activation pattern
        [self.train_node_synapses(t, node) for node in self.all_nodes]


    def iterate(self, t):
        '''
        updates all the nodes and returns the networks current state
        '''
        rand.shuffle(self.all_nodes)
        for node in self.all_nodes:
            node.update(t)

        return self.get_state(t)