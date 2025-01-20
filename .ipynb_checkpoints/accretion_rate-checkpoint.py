import numpy as np
import yt
import glob
import os
import matplotlib.pyplot as plt
import sys

def accretion_rate(Code_Type, vn):
    
    code_type = sys.argv[1] 
    Problem_Type = "DAVID_BLACKHOLE/v"+sys.argv[2]
    
    if code_type == "Athena":
        Base_Path = "/home/david/ATHENA_RUNS/"
        output_type = "/id0/blackhole.????.vtk"
        if "v2" in Problem_Type:
            output_type = "/id0/blackhole_v2.????.vtk"
        level = 0
        dims = [128, 128, 1]
        save_name = Problem_Type.replace("/", "_")+"_Athena_Accretion_Data.npy"
    
    elif code_type == "Athena++":
        Base_Path = "/home/david/ATHENA++_RUNS/"
        output_type = "/blackhole*?????*hdf"
        level = 0
        dims = [128, 128, 1]
        save_name = Problem_Type.replace("/", "_")+"_Athena++_Accretion_Data.npy"
    
    elif code_type == "Flash":
        Base_Path = "/home/david/FLASH_RUNS/"
        output_type = "/*plt_cnt_????"
        level = 5 - 1
        dims = [128, 128, 1]
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
    
    for ii in range (len(files)):
        ds = yt.load(files[ii])
       
        if code_type == "Athena":
            slc = ds.covering_grid(level = level, left_edge = ds.domain_left_edge, dims = dims)
            rr = slc["x"]
            vr = slc["velocity_x"]
            dr = slc["dx"]
            dtheta = slc["dy"]
            density = slc["density"]
    
        elif code_type == "Athena++":
            slc = ds.covering_grid(level = level, left_edge = ds.domain_left_edge, dims = dims)
            rr = slc["r"]
            dr = slc["dr"]
            dtheta = slc["dz"]
            
            if "2c" in Problem_Type:
                density = slc["dens"]
                vr = slc["mom1"] / slc["dens"] 
            else:
                density = slc["rho"]
                vr = slc["vel1"]
    
        elif code_type == "Flash":
            dims = ds.domain_dimensions * 2 ** level
            dims[2] = 1
            slc = ds.covering_grid(level = level, left_edge = ds.domain_left_edge, dims = dims)
            rr = slc["r"]
            vr = slc["velx"]
            dr = slc["dr"]
            dtheta = slc["dtheta"]
            density = slc["dens"]
        
        mass = density * dr * dtheta
        ins = rr == rr.min()
        mass_flux = mass * vr / (dr * 0.5)
        accretion_rate = np.median(mass_flux[ins])
    
        accretion_rates[ii] = accretion_rate
        accretion_times[ii] = ds.current_time
        np.save(save_name, [accretion_times, accretion_rates])
