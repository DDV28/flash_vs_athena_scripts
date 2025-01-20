import numpy as np
import yt
import glob
import os
import matplotlib.pyplot as plt

def polar_plot(Code_Type, vn):
    print(Code_Type)
    print(vn)

    Base_Path = os.environ["SCRATCH"]
    Problem_Type = "DAVID_BLACKHOLE/"+vn
    resolution_pattern = "nx1"
    level = 0
    file_name = "athinput.DAVID_BLACKHOLE_"+vn[:-1].replace("no_", "")
    if "Athena" == Code_Type:
        Base_Path += "/ATHENA_RUNS/"
        output_type = "/id0/*vtk"
        fields = ["density", "pressure", "velocity_x", "velocity_y", "velocity_z", "Gravity"]
    
    elif "Athena++" == Code_Type:
        Base_Path += "/ATHENA++_RUNS/"
        output_type = "/*.out2*hdf"
        fields = ["rho", "press", "vel1", "vel2", "vel3"]
        #fields = ["dens", "Etot", "mom1", "mom2", "mom3"]
    
    elif "Flash" == Code_Type:
        Base_Path += "/FLASH_RUNS/"
        output_type = "/*plt_cnt_????"
        file_name = "flash.par"
        fields = ["density", "pressure", "velx", "vely", "velz", "grav"]
        resolution_pattern = "lrefine_min" 

    Run_Path = Base_Path+"run_data/"+Problem_Type 
    with open(Run_Path+"/"+file_name) as fid:
        data = fid.readlines()
    for line in data:
        #print("Line:", line)
        #print(resolution_pattern in line.lower())
        if resolution_pattern in line.lower():
            break
    print("Line before:", line)    
    line = line.split("=")
    print("Line after:", line)
    resolution = line[1]
    if "#" in resolution:
        resolution = resolution.split("#")
        resolution = resolution[0]
    resolution = int(resolution.replace("\n", "").replace(" ", ""))
 
    if "Flash" == Code_Type:
        level = resolution
        resolution = 8 * 2**(level-1)

    dims = [resolution, resolution, 1]
    
    save_type = Problem_Type+"_polar"
    files = np.sort(glob.glob(Base_Path+"run_data/"+Problem_Type+"/*forced*"))
    for kk in range (len(files)):
        os.system("rm "+files[kk])
    
    files = np.sort(glob.glob(Base_Path+"run_data/"+Problem_Type+output_type))
    
    #plot_path = Base_Path+"run_plots/"+Problem_Type.replace("/","_")+"_plots"
    plot_path = Base_Path+"run_plots/"+Problem_Type
    plotted_files = np.sort(glob.glob(plot_path+"/*.png"))

    os.system("mkdir -p "+plot_path)
    os.chdir(plot_path)
    print(files)
    print("plotted files length:", len(plotted_files))
    for ii in range (len(files)):
        print("ii:", ii)
        if "Gravity" in files[ii]:
            continue
        if len(plotted_files) > ii:
            print("Skipping because files already plotted")
            continue
        ds = yt.load(files[ii])
        
        if "Athena" == Code_Type:
            slc = ds.covering_grid(level = level, left_edge = ds.domain_left_edge, dims = dims)
            rr = slc["x"]
            theta = slc["y"]
    
        elif "Athena++" == Code_Type:
            slc = ds.covering_grid(level = level, left_edge = ds.domain_left_edge, dims = dims)
            rr = slc["r"]
            theta = slc["z"]
    
        elif "Flash" == Code_Type:
            dims = ds.domain_dimensions * 2 ** level
            dims[2] = 1
            slc = ds.covering_grid(level = level, left_edge = ds.domain_left_edge, dims = dims)
            rr = slc["r"]
            theta = slc["theta"]
    
        xx = rr * np.cos(theta)
        yy = rr * np.sin(theta)
        
        for jj in range (len(fields)):
            if Code_Type == "Athena" and fields[jj] == "Gravity":
                continue
                ds = yt.load(files[ii].replace(".vtk", ".Gravity.vtk"))
                slc = ds.covering_grid(level = level, left_edge = ds.domain_left_edge, dims = dims)
                print(ds.field_list)
    
            ff = slc[fields[jj]]
    
            plt.pcolormesh(xx[:, :, 0], yy[:, :, 0], ff[:, :, 0])
            plt.axis("equal")
            cbar = plt.colorbar()
            cbar.ax.set_ylabel(fields[jj])
    
            plt.xlabel("x (r * cos(theta))")
            plt.ylabel("y (r * sin(theta))")
            plt.title("Time:" + "%.2g"%ds.current_time)
            
            if "Athena" == Code_Type:
                file_number = files[ii].split(".")[1]
    
            elif "Athena++" == Code_Type:
                file_number = files[ii].split(".")[2]
    
            elif "Flash" == Code_Type:
                file_number = files[ii].split("_")[-1]
    
            save_name = save_type.replace("/", "_") + "_" + fields[jj] + "_" + file_number + ".png"
            plt.savefig(save_name)
            plt.close()

Parameters = {
        "Athena++":["no_v2", "v2"],
        "Athena":["v2", "v4"],
        "Flash":["v4", "v5"]}
for Code_Type in Parameters:
    for suffix in ["c","d","e","f","g", "h", "i", "j"]:
        vns = Parameters[Code_Type]
        for vn in vns:
            vn += suffix
            polar_plot(Code_Type, vn) 

