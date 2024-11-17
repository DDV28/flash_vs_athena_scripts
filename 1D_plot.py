import numpy as np
import glob
import os
import matplotlib.pyplot as plt

files = np.sort(glob.glob("/home/david/RUNS/1D_noh/id0/*tab"))
os.chdir("/home/david/RUNS/1D_noh_plot")
for i in range (len(files)):
    print(files[i])
    ds = np.loadtxt(files[i])
    
    fig, axs = plt.subplots(2)
    axs[0].plot(ds[:, 1], ds[:, 2])
    axs[1].plot(ds[:, 1], ds[:, 6])
    axs[0].set_ylabel("density [code]")
    axs[1].set_ylabel("pressure [code]")
    axs[1].set_xlabel("x [code]")

    save_name = files[i].replace("tab", "png")
    save_name = save_name.split("/")
    save_name = save_name[-1]
    plt.savefig(save_name)
    plt.close()
