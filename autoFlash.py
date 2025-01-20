import os

Base_Path = "/hppfs/scratch/0D/di38yiw/FLASH_RUNS/run_data/DAVID_BLACKHOLE"
prefix = "v5"
par = "flash.par"

for ii, vn in enumerate(["h", "i", "j"]):
    os.chdir(Base_Path)
    os.system("mkdir -p " + prefix + vn)
    os.system("cp v5c/flash4 " + prefix + vn)
    os.system("cp v5g/flash.par " + prefix + vn)
    os.system("cp v5c/supermuc.slurm " + prefix + vn)
    os.chdir(prefix + vn)


    with open(par, "r") as fidr:
        with open(par + "_", "w") as fidw:
            for line in fidr:
                if "lrefine" in line:
                    line = line.replace("8", str(ii + 9))
                fidw.write(line)
    os.system("mv " + par + "_ " + par)
    
    with open("supermuc.slurm", "r") as fr:
        with open("supermuc.slurm_", "w") as fw:
            for line in fr:
                if "SBATCH -J" in line:
                    line = line.replace("Fv5c", "F" + prefix + vn)
                if "--nodes=1" in line:
                    if "j" in vn:
                        line = line.replace("--nodes=1", "--nodes=" + str(4 ** (5) * 2))
                    line = line.replace("--nodes=1", "--nodes=" + str(4 ** (ii+4)))
                if "--ntasks=48" in line:
                    if "j" in vn:
                        line = line.replace("--ntasks=48", "--ntasks=" + str(48 * (2048)))
                    line = line.replace("--ntasks=48", "--ntasks=" + str(48 * (4 ** (ii+4))))
                if "--time=00:09:00" in line:
                    line = line.replace("--time=00:09:00", "--time=01:00:00")
                if "--partition=test" in line:
                    line = line.replace("--partition=test", "--partition=micro")
                    if "h" in vn:
                        line = line.replace("--partition=micro", "--partition=general")
                    else:
                        line = line.replace("--partition=micro", "--partition=large")
                fw.write(line)

    os.system("mv supermuc.slurm_ supermuc.slurm")
    os.system("sbatch supermuc.slurm")
