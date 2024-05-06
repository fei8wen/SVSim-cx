#!/bin/bash
#BSUB -P ###
#BSUB -W 1
#BSUB -nnodes 1
#BSUB -o out_cc.txt -e err_cc.txt
module use /soft/modulefiles
module load spack-pe-base cmake
module load conda
module load nvhpc/23.9
module load cudatoolkit-standalone 
conda activate svsim;
conda activate svsim;
module load craype-accel-nvidia80
echo "Active Conda Environment: $(conda info --env | grep \* | awk '{print $1}')"
module load PrgEnv-cray
#export PYTHONPATH=/lus/grand/projects/sbi-fair/qsac/SV-Sim/svsim/QASMBench:$PYTHONPATH
#cp /lus/grand/projects/sbi-fair/qsac/SV-Sim/svsim/QASMBench/libsvsim.so /lus/grand/projects/sbi-fair/qsac/SV-Sim/svsim/build/
export CUDA_HOME=/opt/nvidia/hpc_sdk/Linux_x86_64/23.3/cuda/11.8
export LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/23.3/cuda/11.8/lib64/:$LD_LIBRARY_PATH
export CUDA_HOME=/opt/nvidia/hpc_sdk/Linux_x86_64/23.3/cuda/11.8
export PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/23.3/cuda/11.8/lib64/:$PATH
export LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/23.3/comm_libs/openmpi/openmpi-3.1.5/lib/:$LD_LIBRARY_PATH
export OPAL_PREFIX=/opt/nvidia/hpc_sdk/Linux_x86_64/23.3/comm_libs/mpi/
export MPICH_GPU_SUPPORT_ENABLED=1
export PYTHONPATH=~/qsac/SVSim-cx/svsim/QASMBench:$PYTHONPATH
