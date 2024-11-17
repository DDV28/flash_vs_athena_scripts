import numpy as np
import yt
import glob
import os

Base_Path = "/home/david/ATHENA_RUNS/"
Problem_Type = "DAVID_BLACKHOLE_V2"
files = np.sort(glob.glob(Base_Path+"run_data/"+Problem_Type+"/id0/*vtk"))
os.system("mkdir -p "+Base_Path+"run_plots/"+Problem_Type+"_plot")
os.chdir(Base_Path+"run_plots/"+Problem_Type+"_plot")
for i in range (len(files)):
    ds = yt.load(files[i])
    slc = yt.SlicePlot(ds, "z", ["density", "pressure", "velocity_x", "velocity_y", "velocity_z"])
    slc.annotate_title(ds.current_time)
    slc.save()

