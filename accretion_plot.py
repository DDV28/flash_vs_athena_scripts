import numpy as np
import glob
import os
import matplotlib.pyplot as plt

title = "With Viscosity 128 Log10 Y v8 (sum)"
Problem_Type = ["DAVID_BLACKHOLE/v4b", "DAVID_BLACKHOLE/v5b", "DAVID_BLACKHOLE/v2e"]
#Problem_Type = ["DAVID_BLACKHOLE/v2", "DAVID_BLACKHOLE/v4d", "DAVID_BLACKHOLE/v2d"]

Base_Path = ["/home/david/ATHENA_RUNS/", "/home/david/FLASH_RUNS/", "/home/david/ATHENA++_RUNS/"]
save_name = ["Athena_Accretion_Data_Sum.npy", "Flash_Accretion_Data_Sum.npy", "Athena++_Accretion_Data.npy"]
labels = ["Athena", "FLASH", "Athena++"]
colors = ["red", "blue", "green"]
line_styles = ["solid", "dotted", "dashed"]
run_data = []
save = title.replace(" ", "_")

for ii in range(len(Base_Path)): 
    plot_path = Base_Path[ii]+"run_plots/"+Problem_Type[ii]
    os.chdir(plot_path)
    
    data = np.load(Problem_Type[ii].replace("/", "_")+"_"+save_name[ii])
    print("data", data[1, -1])
    
    indices = data[0, :] != 0
    run_data.append(data[1, :])

    run_data[-1][:] = np.log10(np.abs(run_data[-1][:]))

    plt.plot(data[0, :],np.log10(np.abs(data[1, :])), color = colors[ii], linestyle = line_styles[ii], label = labels[ii])
    if labels[ii]=="Athena":
        print("Time: ",data[0,:][:30])
        print("Accretion Rate: ",data[1, :][:30])

plt.xlabel("Time [code-time]")
plt.ylabel("Log Accretion Rate [code-mass/code-time]")
#plt.ylim(-4, -.7)
plt.legend()
plt.title(title)
plt.tight_layout()
os.chdir("/home/david/flash_vs_athena_scripts")
plt.savefig("Accretion_Rate_"+save+".png")
plt.close()

indices = run_data[0] != 0
labels = ["|Athena - Athena++| / Athena", "|FLASH - Athena| / FLASH", "|Athena++ - FLASH| / Athena++"]

for jj in range(len(Base_Path)):
    error = np.abs(run_data[jj][:] - run_data[jj-1][:]) / np.abs(run_data[jj][:])
    plt.plot(data[0, :], error, color = colors[jj], linestyle = line_styles[jj], label = labels[jj])
    print(run_data[jj][-1])
    print((run_data[jj][-1] - run_data[jj-1][-1]) / run_data[jj][-1])
    print(error[-1])
plt.legend()
plt.xlabel("Time [code-time]")
plt.ylabel("Relative Error")
plt.title("Accretion Rate Relative Error " + title)
plt.tight_layout()
plt.savefig("Accretion_Rate_Error_"+save+".png")
plt.close()
print("Error: ", error)


