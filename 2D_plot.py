import numpy as np
import yt
import glob
import os

Base_Path = "/home/david/ATHENA++_RUNS/"
Problem_Type = "DAVID_BLACKHOLE/v2b"
files = np.sort(glob.glob(Base_Path+"run_data/"+Problem_Type+"/*hdf"))
os.system("mkdir -p "+Base_Path+"run_plots/"+Problem_Type)
os.chdir(Base_Path+"run_plots/"+Problem_Type)

for i in range (len(files)):
    ds = yt.load(files[i])
    slc = yt.SlicePlot(ds, "z", "rho")
    slc.annotate_title(ds.current_time)
    slc.save()

