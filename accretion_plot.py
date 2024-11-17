import numpy as np
import glob
import os
import matplotlib.pyplot as plt


Base_Path = ["/home/david/ATHENA_RUNS/", "/home/david/FLASH_RUNS/"]
Problem_Type = ["DAVID_BLACKHOLE/v2", "DAVID_BLACKHOLE/v4d"]
save_name = ["Athena_Accretion_Data.npy", "Flash_Accretion_Data.npy"]
labels = ["Athena", "Flash"]
colors = ["red", "blue"]
line_styles = ["solid", "dotted"]

for ii in range (2): 
    plot_path = Base_Path[ii]+"run_plots/"+Problem_Type[ii]
    os.chdir(plot_path)
    
    data = np.load(Problem_Type[ii].replace("/", "_")+"_"+save_name[ii])

    indices = data[0, :] != 0
    plt.plot(data[0, indices], data[1, indices], color = colors[ii], linestyle = line_styles[ii], label = labels[ii])
    if labels[ii]=="Athena":
        print("Time: ",data[0,indices][:30])
        print("Accretion Rate: ",data[1, indices][:30])
plt.xlabel("Time [code-time]")
plt.ylabel("Accretion Rate [code-mass/code-time]")
plt.legend()
plt.title("Without Viscosity")
plt.tight_layout()
os.chdir("/home/david/flash_vs_athena_scripts")
plt.savefig("Accretion_Rate_No_Viscosity.png")
plt.close()


