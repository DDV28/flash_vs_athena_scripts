#!/bin/bash
#
#SBATCH -J ARate3
#SBATCH -o ./%x.%j.out
#SBATCH -e ./%x.%j.err
#SBATCH -D ./
#SBATCH --mail-user ddvaida28@gmail.com
#SBATCH --mail-type=ALL
#SBATCH --no-requeue
#SBTACH --export=NONE
#SBATCH --get-user-env
#SBATCH --account=pn49ye
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=24:00:00
#SBATCH --partition=micro
#SBATCH --ear=off

echo "PWD: $PWD"
module list
date

python3 -u accretion_rate3.py

date
echo "SUCCESS!"
