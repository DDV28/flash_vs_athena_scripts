import numpy as np
import matplotlib.pyplot as plt
import os
import yt
import glob

code_type = "Athena++"

if code_type == "Athena":
    Base_Path = "/home/david/ATHENA_RUNS/run_plots/DAVID_BLACKHOLE/"
    Problem_Type = "v4/"
    var_list = ["pressure", "density", "velocity_x", "velocity_y", "velocity_z"]
    Movie_Name = "Athena_Blackhole_"+Problem_Type[:-1]
    glob_pattern = Base_Path+Problem_Type+"*density*.png"
    Movie_Directory = Base_Path.replace("run_plots/DAVID_BLACKHOLE/", "") + "/run_movies"

elif code_type == "Flash":
    Base_Path = "/home/david/FLASH_RUNS/run_plots/DAVID_BLACKHOLE/"
    Problem_Type = "v5/"
    var_list = ["pressure", "density", "velx", "vely", "velz", "grav"]
    Movie_Name = "Flash_Blackhole_"+Problem_Type[:-1]
    glob_pattern = Base_Path+Problem_Type+"*density*.png"
    Movie_Directory = Base_Path.replace("run_plots/DAVID_BLACKHOLE/", "") + "/run_movies"

elif code_type == "Athena++":
    Base_Path = "/home/david/ATHENA++_RUNS/run_plots/DAVID_BLACKHOLE/"
    Problem_Type = "v2e/"
    var_list = ["press", "rho", "vel1", "vel2", "vel3"]
    #var_list = ["Etot", "dens", "mom1", "mom2", "mom3"]
    Movie_Name = "Athena++_Blackhole_"+Problem_Type[:-1]
    glob_pattern = Base_Path+Problem_Type+"*"+var_list[1]+"*.png"
    Movie_Directory = Base_Path.replace("run_plots/DAVID_BLACKHOLE/", "") + "/run_movies"

files = np.sort(glob.glob(glob_pattern))
framerate = len(files)/3
framerate = min(60, framerate)
framerate = int(framerate)
framerate = str(framerate)

os.system("mkdir -p " + Movie_Directory)
os.chdir(Movie_Directory)


for quantity in var_list:
    os.system("/usr/bin/ffmpeg -framerate "+framerate+" -pattern_type glob -i '"
    +Base_Path+Problem_Type+"*"+quantity+"*.png' -c:v libx264 -pix_fmt yuv420p -vf 'pad=ceil(iw/2)*2:ceil(ih/2)*2' "
    +Movie_Name+"_"+quantity+".mp4")
