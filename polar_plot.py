import numpy as np
import yt
import glob
import os
import matplotlib.pyplot as plt

def polar_plot(Code_Type, vn):
    Code_Type = "Athena++"
    
    if "Athena" == Code_Type:
        Base_Path = "/home/david/ATHENA_RUNS/"
        Problem_Type = "DAVID_BLACKHOLE/v4"
        output_type = "/id0/*vtk"
        level = 0
        dims = [64, 64, 1]
        fields = ["density", "pressure", "velocity_x", "velocity_y", "velocity_z", "Gravity"]
    
    elif "Athena++" == Code_Type:
        Base_Path = "/home/david/ATHENA++_RUNS/"
        Problem_Type = "DAVID_BLACKHOLE/v2d"
        output_type = "/*hdf"
        level = 0
        dims = [128, 128, 1]
        fields = ["rho", "press", "vel1", "vel2", "vel3"]
        #fields = ["dens", "Etot", "mom1", "mom2", "mom3"]
    
    elif "Flash" == Code_Type:
        Base_Path = "/home/david/FLASH_RUNS/"
        Problem_Type = "DAVID_BLACKHOLE/v5"
        output_type = "/*plt_cnt_????"
        level = 4 - 1
        dims = [64, 64, 1]
        fields = ["density", "pressure", "velx", "vely", "velz", "grav"]
    
    save_type = Problem_Type+"_polar"
    files = np.sort(glob.glob(Base_Path+"run_data/"+Problem_Type+"/*forced*"))
    for kk in range (len(files)):
        os.system("rm "+files[kk])
    
    files = np.sort(glob.glob(Base_Path+"run_data/"+Problem_Type+output_type))
    
    #plot_path = Base_Path+"run_plots/"+Problem_Type.replace("/","_")+"_plots"
    plot_path = Base_Path+"run_plots/"+Problem_Type
    
    os.system("mkdir -p "+plot_path)
    os.chdir(plot_path)
    print(files)
    for ii in range (len(files)):
        if "Gravity" in files[ii]:
            continue
       # if !("130" in files[ii]):
        #    continue
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
