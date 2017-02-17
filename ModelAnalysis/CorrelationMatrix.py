import matplotlib.pyplot as plt
import numpy as np

def correlationMatrix(data):
    correl = data.transpose().corr()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(correl, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0,9,1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    plt.show()