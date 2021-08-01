from matplotlib import pyplot as plt
from celluloid import Camera
import numpy as np
import pdb

def visualise_sim(sim_logs):
    fig, plts = plt.subplots(3)

    camera = Camera(fig)

    for log in sim_logs:
        [plts[i].bar(range(len(log['spiking'][i])), log['spiking'][i]) for i in range(len(log['spiking']))]
        camera.snap()

    animation = camera.animate()
    animation.save('data/sim_vis.gif', writer='imagemagick')

def graph_sim(sim_logs):
    fig, plts = plt.subplots(3)
    for i,key in enumerate(['spiking', 'potential', 'threshold']):
        for j in range(3):
            layer_data = []

            for log in sim_logs:
                layer_data.append(np.mean(log[key][j]))

            plts[i].plot(layer_data)
    plt.show()
        
    
    
