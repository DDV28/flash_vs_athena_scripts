import numpy as np
import yt
import glob
import os
import matplotlib.pyplot as plt
import sys

def accretion_rate(Code_Type, vn):
    Base_Path = os.environ["SCRATCH"]
    Problem_Type = "DAVID_BLACKHOLE/"+vn
    resolution_pattern = "nx1"
    level = 0
    file_name = "athinput.DAVID_BLACKHOLE_"+vn[:-1].replace("no_", "")
    
    if Code_Type == "Athena":
        Base_Path += "/ATHENA_RUNS/"
        output_type = "/id0/blackhole.????.vtk"
        if "v2" in Problem_Type:
            output_type = "/id0/blackhole_v2.????.vtk"
        save_name = Problem_Type.replace("/", "_")+"_Athena_Accretion_Data.npy"
    
    elif Code_Type == "Athena++":
        Base_Path += "/ATHENA++_RUNS/"
        output_type = "/blackhole.out2*?????*hdf"
        save_name = Problem_Type.replace("/", "_")+"_Athena++_Accretion_Data.npy"
    
    elif Code_Type == "Flash":
        Base_Path += "/FLASH_RUNS/"
        output_type = "/*plt_cnt_????"
        resolution_pattern = "lrefine_min"
        file_name = "flash.par"
        save_name = Problem_Type.replace("/", "_")+"_Flash_Accretion_Data.npy"
    
    print(save_name)
    
    files = np.sort(glob.glob(Base_Path+"run_data/"+Problem_Type+"/*forced*"))
    for kk in range (len(files)):
        os.system("rm "+files[kk])
    
    files = np.sort(glob.glob(Base_Path+"run_data/"+Problem_Type+output_type))
    
    accretion_rates = np.zeros(len(files))
    accretion_times = np.zeros(len(files))
    
    Run_Path = Base_Path+"run_data/"+Problem_Type
    with open(Run_Path+"/"+file_name) as fid:
        data = fid.readlines()
    for line in data:
        if resolution_pattern in line.lower():
            break
    line = line.split("=")
    resolution = line[1]
    if "#" in resolution:
        resolution = resolution.split("#")
        resolution = resolution[0]
    resolution = int(resolution.replace("\n", "").replace(" ", ""))

    if "Flash" == Code_Type:
        level = resolution
        resolution = 8 * 2**(level-1)

    dims = [resolution, resolution, 1]

    for ii in range (len(files)):
        try:
            ds = yt.load(files[ii])
        except:
            print("Failed to Load " + files[ii])

        if Code_Type == "Athena":
            slc = ds.covering_grid(level = level, left_edge = ds.domain_left_edge, dims = dims)
            rr = slc["x"]
            vr = slc["velocity_x"]
            dr = slc["dx"]
            dtheta = slc["dy"]
            density = slc["density"]
    
        elif Code_Type == "Athena++":
            slc = ds.covering_grid(level = level, left_edge = ds.domain_left_edge, dims = dims)
            rr = slc["r"]
            dr = slc["dr"]
            dtheta = slc["dz"]
            density = slc["rho"]
            vr = slc["vel1"]
    
        elif Code_Type == "Flash":
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

Parameters = {
        "Athena++":["no_v2", "v2"]}
 #       "Athena":["v2", "v4"],
 #       "Flash":["v4", "v5"]}
for Code_Type in Parameters:
    for suffix in ["c","d","e","f","g", "h"]:
        vns = Parameters[Code_Type]
        for vn in vns:
            vn += suffix
            if Code_Type == "Athena++":
                if suffix in ["c","d","e","f"]:
                    if "v2f" != vn:
                        continue
            accretion_rate(Code_Type, vn)
