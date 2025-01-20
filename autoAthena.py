import os

Base_Path = "/hppfs/scratch/0D/di38yiw/ATHENA_RUNS/run_data/DAVID_BLACKHOLE"
prefix = "v4"

for ii, vn in enumerate(["h", "i", "j"]):
    if "h" in vn:
        continue
    os.chdir(Base_Path)
    os.system("mkdir -p " + prefix + vn)
    os.system("cp v4c/athena " + prefix + vn)
    os.system("cp v4c/supermuc.slurm " + prefix + vn)
    os.system("cp " + prefix + "g" + "/athinput* " + prefix + vn + "/athinput.DAVID_BLACKHOLE_" + prefix)
    os.chdir(prefix + vn)

    with open("athinput.DAVID_BLACKHOLE_" + prefix, "r") as fidr:
        with open("athinput.DAVID_BLACKHOLE_" + prefix + "_", "w") as fidw:
            for line in fidr:
                if "nx1" in line or "nx2" in line:
                    line = line.replace("1024", str(1024 * (2 ** (ii + 1))))
                if "NGrid_x1" in line:
                    line2 = line.split("=")
                    line2[1] = line2[1].replace(" ", "").replace("\n", "")
                    if "#" in line2[1]:
                        line2[1] = line2[1].split("#")[0]
                    if "j" in vn:
                        line = line.replace(line2[1], str(int(line2[1]) * (4 ** (2) * 2)))
                    else:
                        line = line.replace(line2[1], str(int(line2[1]) * (4 ** (ii + 1))))  
                #if "nu_iso" not in line:
                fidw.write(line)
    
    os.system("mv athinput.DAVID_BLACKHOLE_" + prefix + "_ athinput.DAVID_BLACKHOLE_" + prefix)
    
    with open("supermuc.slurm", "r") as fr:
        with open("supermuc.slurm_", "w") as fw:
            for line in fr:
                if "SBATCH -J" in line:
                    line = line.replace("Av4c", "A" + prefix + vn)
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
