class Synapse():

    def __init__(self, pre_node, post_node, excit_perm, 
                    inhib_perm, base_learn_rate, pre_thresh, post_thresh):
        self.pre_node = pre_node
        self.post_node = post_node
        self.excit_perm = excit_perm
        self.inhib_perm = inhib_perm
        self.base_learn_rate = base_learn_rate

        self.pre_thresh = pre_thresh
        self.post_thresh = post_thresh

    def delta(self, t, valence):
        learn_rate = valence * self.base_learn_rate

        if learn_rate < 0:
            learn_rate *= (1 - self.inhib_perm)
        else:
            learn_rate *= (1 - self.excit_perm)
        
        pre_learn = (self.pre_node.last_fired == t)
        post_learn = (self.post_node.last_fired == t)

        delta = learn_rate * (pre_learn - self.pre_thresh) * (post_learn - self.post_thresh)
        return delta

    