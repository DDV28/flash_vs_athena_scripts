import numpy as np
import glob
import os
import matplotlib.pyplot as plt

title = "1024 v16"

labels = ["FLASH", "Athena", "Athena++"]
label_vn = ["64", "128", "256", "512", "1024", "2048"]
glob_labels = ["Flash", "Athena", "Athena++"]
colors = ["purple", "blue", "red", "green", "grey", "black"]
line_styles = ["solid", "dashed", "dotted"]
line_sizes = [1, 1, 1]
run_data_visc = {
          "Flash":[[], []],
          "Athena":[[], []],
          "Athena++":[[], []]}
run_data_no_visc = {
          "Flash":[[], []],
          "Athena":[[], []],
          "Athena++":[[], []]}
fig,axes = plt.subplots(nrows = 2, ncols = 2, figsize = (9, 6))
save = title.replace(" ", "_")
Parameters = {
         "Flash":["v4" , "v5"],
         "Athena":["v2", "v4"],
         "Athena++":["no_v2", "v2"]}
jj = -1
#os.chdir("/home/david/fromSupermuc/flash_vs_athena_scripts")
for Code_Type in Parameters:
    ii = -1
    jj += 1
    for suffix in ["c","d","e","f","g", "h"]:
        ii += 1
        vns = Parameters[Code_Type]
        for kk,vn in enumerate(vns):
            vn += suffix
            save_name = "DAVID_BLACKHOLE_" + vn + "_"  + Code_Type + "_Accretion_Data.npy"
            if not os.path.exists(save_name):
               continue
            data = np.load(save_name)
            if Code_Type == "Flash" and suffix == "h":
               data[0, :] = -1 
            #indices = data[0, :] != 0
            print("kk:", kk)
            #print("run_data", run_data[0][kk])
            #print("run_data[0]", run_data[0])
            data[1, :] = np.log10(np.abs(data[1, :]))
            if kk == 0:
               run_data_no_visc[Code_Type][0].append(data[1, :])
               run_data_no_visc[Code_Type][1].append(data[0, :])
               if Code_Type == "Flash":
                   axes[kk][0].plot(data[0, :], run_data_no_visc[Code_Type][0][-1], color = colors[ii], linestyle = line_styles[jj], lw = line_sizes[jj], label = label_vn[ii])
               else:
                   axes[kk][0].plot(data[0, :], run_data_no_visc[Code_Type][0][-1], color = colors[ii], lw = line_sizes[jj], linestyle = line_styles[jj])

            else:
               run_data_visc[Code_Type][0].append(data[1, :])
               run_data_visc[Code_Type][1].append(data[0, :])
               if suffix == "g" and Code_Type == "Athena":
                   continue
               if Code_Type == "Flash":
                   axes[kk][0].plot(data[0, :], run_data_visc[Code_Type][0][-1], color = colors[ii], linestyle = line_styles[jj], lw = line_sizes[jj], label = label_vn[ii])
               else:
                   axes[kk][0].plot(data[0, :], run_data_visc[Code_Type][0][-1], color = colors[ii], lw = line_sizes[jj], linestyle = line_styles[jj])


           # input(">>")
            print("code_type", Code_Type)
            print("vns", vn)
            print("data[1, :]", data[1, :])
            print("log", np.log10(np.abs(data[1, :])))

for ii in range(2):
     axes[1][ii].set_xlabel("Time [code-time]")
     axes[ii][0].set_xlim(0, 108)
axes[1][0].set_ylim(-6, -2)
axes[1][0].set_ylabel("Log Accretion Rate [code-mass/code-time]")
if "Sum" in title:
     axes[1][0].set_ylim(-2, -.5)
axes[1][0].legend()
plots = []
for ii in range(3):
    plot, = axes[1][0].plot([-10, -9], [-12, -11], color = "black", linestyle = line_styles[ii])
    plots.append(plot)
legend1 = axes[1][0].legend(loc = "lower right", fontsize = 9)
axes[1][0].legend(plots, labels, loc="upper right", fontsize = 9)
axes[1][0].add_artist(legend1)

os.chdir("/home/david/flash_vs_athena_scripts")
#plt.savefig("Publication_Accretion_Rate_"+save+".png")
#plt.close()

labels = ["|FLASH - Athena++| / FLASH", "|Athena - FLASH| / Athena", "|Athena++ - Athena| / Athena++"]

res = -2
for jj, Code_Type in enumerate(Parameters):
    for kk in range(2):
        if kk == 0:
            first = run_data_no_visc[glob_labels[jj]][0][res]
            second = run_data_no_visc[glob_labels[jj-1]][0][res]
            times = run_data_no_visc[glob_labels[jj]][1][res]
        else:
            first = run_data_visc[glob_labels[jj]][0][res]
            second = run_data_visc[glob_labels[jj-1]][0][res]
            times = run_data_visc[glob_labels[jj]][1][res]

        if len(first) > len(second):
           max_index = len(second)
        else:
           max_index = len(first)
        error = np.abs(first[:max_index] - second[:max_index]) / np.abs(first[:max_index])
        axes[kk][1].plot(times[:max_index], error, color = colors[res], linestyle = line_styles[jj], label = labels[jj])
axes[0][1].legend()
axes[-1][1].set_xlabel("Time [code-time]")
axes[0][1].set_ylabel("Relative Error")
plt.tight_layout()
plt.savefig("Publication_Accretion_Rate_With_Error_"+save+".png")
plt.close()
print("Error: ", error)


