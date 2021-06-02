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
// File: adder_n10_nvgpu_omp.cu
// A 10-qubit adder example based on OpenMP using NVIDIA GPU backend.
// For single-node (1 or more GPUs); no inter-GPU communication required.
// ---------------------------------------------------------------------------

#include <stdio.h>
#include "../src/util_nvgpu.cuh"
#include "../src/svsim_nvgpu_omp.cuh"

using namespace SVSim;

//You can define circuit module functions as below.
void majority(Simulation &sim, const IdxType a, const IdxType b, const IdxType c)
{
    sim.append(Simulation::CX(c, b));
    sim.append(Simulation::CX(c, a));
    sim.append(Simulation::CCX(a, b, c));
}
void unmaj(Simulation &sim, const IdxType a, const IdxType b, const IdxType c)
{
    sim.append(Simulation::CCX(a, b, c));
    sim.append(Simulation::CX(c, a));
    sim.append(Simulation::CX(a, b));
}

int main()
{
//=================================== Initialization =====================================
    srand(RAND_SEED);
    int n_qubits = 10;
    int n_gpus = 4;

    //Obtain a simulator object
    Simulation sim(n_qubits, n_gpus);

    //Add the gates to the circuit
    sim.append(Simulation::X(1));
    sim.append(Simulation::X(5));
    sim.append(Simulation::X(6));
    sim.append(Simulation::X(7));
    sim.append(Simulation::X(8));
    
    //Call user-defined module functions 
    majority(sim, 0, 5, 1);
    majority(sim, 1, 6, 2);
    majority(sim, 2, 7, 3);
    majority(sim, 3, 8, 4);
    sim.append(Simulation::CX(4, 9));
    unmaj(sim, 3, 8, 4);
    unmaj(sim, 2, 7, 3);
    unmaj(sim, 1, 6, 2);
    unmaj(sim, 0, 5, 1);

    //Upload to GPU, ready for execution
    sim.upload();

    //Run the simulation
    sim.sim();
    
    //Measure
    auto* res = sim.measure(5);
    print_measurement(res, 10, 5);
    delete res; 

    return 0;
}

