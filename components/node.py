class Node():

    def __init__(self, layer, response_function, threshold_function, spiking_method,
                    base_threshold, abs_refrac, rel_refrac):
        self.layer = layer
        
        self.synapses = []

        self.threshold = base_threshold
        self.potential = 0

        self.last_fired = None

        self.firing_history = []

        self.response_function = response_function

        self.threshold_function = threshold_function
        self.base_threshold = base_threshold
        self.abs_refrac = abs_refrac
        self.rel_refrac = rel_refrac

        self.spike = spiking_method

    def reset(self):
        self.last_fired = None
        self.firing_history = []

    # p is recalculated each update, do we want a continuous value?
    def get_potential(self, t):
        '''
        calculate the firing potential for the node at t
        self is the post node
        '''
        p = 0
        for synapse in self.synapses:
            if synapse.pre_node.last_fired != None:
                # assign for cleaner use
                n = synapse.pre_node
                # determine dominate synapse
                if synapse.excit_perm > synapse.inhib_perm:
                    w = synapse.excit_perm
                else:
                    w = -1 * synapse.inhib_perm
                # calculate post synaptic potential
                psp = w * n.response_function(n.last_fired, t)
                # add to permanence
                p += psp
        return p 

    def update(self, t):
        '''
        update the firing behaviour of self at t 
        '''
        # 
        if self.last_fired != None:
            self.threshold = self.threshold_function(self.last_fired, t, self.base_threshold, 
                                            self.abs_refrac, self.rel_refrac)

        self.potential = self.get_potential(t)

        if self.spike(self.potential, self.threshold):
            self.last_fired = t
            self.firing_history.append(1)
        else:
            self.firing_history.append(0)