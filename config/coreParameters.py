from config import functions as f

simulation = dict(
    sim_length = 20,
    training_epochs = 500,
)

model = dict (
    init_syn_min = 0,
    init_syn_max = 0.1,

    n_layers = 3, # the number of layers in the network
    layer_ns = [100,100,100], # the number of nodes in each layer
    
    # [0](the indexes of the [0]:pre, and [1]: post synaptic layers)  
    # [1](the proportion of nodes in those layers to be connected)
    layer_connections = [[[0,1],1], 
                         [[1,0],1], 
                         [[1,2],1], 
                         [[2,1],1],
                         [[2,2],1],],

    base_learn_rate = 0.01, 
    pre_thresh = 0.55,
    post_thresh = 0.05,
 
    threshold_function = f.inv_exp_threshold,
    base_threshold = 0.01,
    abs_refrac = 2,
    rel_refrac = 10,

    response_function = f.triangle_response,
    spiking_method = f.exp_rand_spike,

)
