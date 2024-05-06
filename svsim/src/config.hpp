// ---------------------------------------------------------------------------
// NWQsim: Northwest Quantum Circuit Simulation Environment
// ---------------------------------------------------------------------------
// Ang Li, Senior Computer Scientist
// Pacific Northwest National Laboratory(PNNL), U.S.
// Homepage: http://www.angliphd.com
// GitHub repo: http://www.github.com/pnnl/DM-Sim
// PNNL-IPID: 31919-E, ECCN: EAR99, IR: PNNL-SA-143160
// BSD Lincese.
// ---------------------------------------------------------------------------
// File: config.hpp
// Configuration file defining the gate and runtime settings.
// ---------------------------------------------------------------------------

#ifndef CONFIG_HPP
#define CONFIG_HPP

//QIR backend: {CPU, NVGPU, AMDGPU}

//#define CPU
//#define NVGPU
//#define AMDGPU

//Track per circuit execution performance
#define PRINT_MEA_PER_CIRCUIT

//Error check for all NVIDIA CUDA Runtim-API calls and Kernel check
#define CUDA_ERROR_CHECK

//Error check for all AMD HIP Runtim-API calls and Kernel check
#define HIP_ERROR_CHECK

//Accelerate by AVX512
//#define USE_AVX512

#include <cuda_fp16.h>
// ================================= Configurations =====================================
namespace SVSim 
{
//Basic Type for indices, adjust to uint64_t when qubits > 15
using IdxType = unsigned;
//Basic Type for value, expect to support half, float and double
using ValType = __half;
//Random seed
#define RAND_SEED time(0)
//Tile for transposition in the adjoint operation
#define TILE 16
//Threads per GPU Thread BLock (Fixed)
#define THREADS_PER_BLOCK 256
//Error bar for validation
#define ERROR_BAR (1e-3)
// constant value of PI
#define PI 3.14159265358979323846
// constant value of 1/sqrt(2)
#define S2I 0.70710678118654752440 
//// avx bitwidth for CPU
#define AVX 512
//// vector length
#define VEC ((AVX)/sizeof(IdxType))

}; //namespace SVSim

#endif
