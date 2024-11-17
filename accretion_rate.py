import numpy as np
import yt
import glob
import os
import matplotlib.pyplot as plt

isAthena = True

if isAthena:
    Base_Path = "/home/david/ATHENA_RUNS/"
    Problem_Type = "DAVID_BLACKHOLE/v2"
    output_type = "/id0/*vtk"
    level = 0
    dims = [64, 64, 1]
    save_name = Problem_Type.replace("/", "_")+"_Athena_Accretion_Data.npy"
else:
    Base_Path = "/home/david/FLASH_RUNS/"
    Problem_Type = "DAVID_BLACKHOLE/v5"
    output_type = "/*plt_cnt_????"
    level = 4 - 1
    dims = [64, 64, 1]
    save_name = Problem_Type.replace("/", "_")+"_Flash_Accretion_Data.npy"

print(save_name)

save_type = Problem_Type+"_polar"
files = np.sort(glob.glob(Base_Path+"run_data/"+Problem_Type+"/*forced*"))
for kk in range (len(files)):
    os.system("rm "+files[kk])

files = np.sort(glob.glob(Base_Path+"run_data/"+Problem_Type+output_type))

#plot_path = Base_Path+"run_plots/"+Problem_Type.replace("/","_")+"_plots"
plot_path = Base_Path+"run_plots/"+Problem_Type

os.system("mkdir -p "+plot_path)
os.chdir(plot_path)

accretion_rates = np.zeros(len(files))
accretion_times = np.zeros(len(files))

file_exist = glob.glob(save_name+"*")
if len(file_exist) > 0:
    data = np.load(file_exist[0])
    plt.plot(data[0, :], data[1, :])
    plt.xlabel("Time [code-time]")
    plt.ylabel("Accretion Rate [code-mass/code-time]")
    plt.tight_layout()
    plt.savefig("Athena_Accretion_Rate.png")
    plt.close()
    exit()

for ii in range (len(files)):
    ds = yt.load(files[ii])
   
    if isAthena:
        if "Gravity" in files[ii]:
            continue
        slc = ds.covering_grid(level = level, left_edge = ds.domain_left_edge, dims = dims)
        rr = slc["x"]
        vr = slc["velocity_x"]
        dr = slc["dx"]

    else:
        dims = ds.domain_dimensions * 2 ** level
        dims[2] = 1
        slc = ds.covering_grid(level = level, left_edge = ds.domain_left_edge, dims = dims)
        rr = slc["r"]
        vr = slc["velx"]
        dr = slc["dr"]

    mass = slc["cell_mass"]
    ins = rr == rr.min()
    mass_flux = mass * vr / (dr * 0.5)
    accretion_rate = np.median(mass_flux[ins])

    accretion_rates[ii] = accretion_rate
    accretion_times[ii] = ds.current_time
    np.save(save_name, [accretion_times, accretion_rates])
