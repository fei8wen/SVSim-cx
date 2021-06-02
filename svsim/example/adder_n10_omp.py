# ---------------------------------------------------------------------------
# NWQsim: Northwest Quantum Circuit Simulation Environment
# ---------------------------------------------------------------------------
# Ang Li, Senior Computer Scientist
# Pacific Northwest National Laboratory(PNNL), U.S.
# Homepage: http://www.angliphd.com
# GitHub repo: http://www.github.com/pnnl/DM-Sim
# PNNL-IPID: 31919-E, ECCN: EAR99, IR: PNNL-SA-143160
# BSD Lincese.
# ---------------------------------------------------------------------------
# File: adder_n10_omp.py
# A 10-qubit adder example using Python API.
# Single-node multiple NVIDIA GPUs; No inter-GPU communication required.
# Requires: PyBind11 (https://github.com/pybind/pybind11)
#           CUDA-10.0 or newer (required by pybind11 for Python API)
# ---------------------------------------------------------------------------
import sys

# Using SV-Sim NVGPU backend
import libsvsim_py_nvgpu_omp as svsim_omp

# Using SV-Sim CPU backend
#import libsvsim_py_cpu_omp as svsim_omp

# Using SV-Sim AMDGPU backend
#import libsvsim_py_amdgpu_omp as svsim_omp


## Call via: $python circuit.py num_of_qubits num_of_gpus
if (len(sys.argv) != 3):
    print("Call using $python circuit.py n_qubits n_gpus/n_cpus\n")
    exit()

n_qubits = int(sys.argv[1])
n_gpus = int(sys.argv[2])

## Create simulator object
sim = svsim_omp.Simulation(n_qubits, n_gpus)

## Quantum ripple-carry adder from Cuccaro et al, quant-ph/0410184
## Define circuit module functions as below
def majority(sim, a, b, c):
	sim.append(sim.CX(c, b))
	sim.append(sim.CX(c, a))
	sim.append(sim.CCX(a, b, c))

def unmaj(sim, a, b, c):
	sim.append(sim.CCX(a, b, c))
	sim.append(sim.CX(c, a))
	sim.append(sim.CX(a, b))

## Add the gates to the circuit
sim.append(sim.X(1))
sim.append(sim.X(5))
sim.append(sim.X(6))
sim.append(sim.X(7))
sim.append(sim.X(8))

## Upload to GPU, ready for execution
sim.upload()
## Run the simulation
sim.run()
## Clear existing circuit
sim.clear_circuit()

## Add a new circuit for the current density matrix
majority(sim, 0, 5, 1)
majority(sim, 1, 6, 2)
majority(sim, 2, 7, 3)
majority(sim, 3, 8, 4)
sim.append(sim.CX(4, 9))
unmaj(sim, 3, 8, 4)
unmaj(sim, 2, 7, 3)
unmaj(sim, 1, 6, 2)
unmaj(sim, 0, 5, 1)

## Upload the new circuit to GPU
sim.upload()
## Run the new circuit
sim.run()
## Measure, 10 is the repetition or shots, return a list
res = sim.measure(10)
## Print measurement results
print ("\n===============  Measurement (tests=" + str(len(res)) + ") ================")
for i in range(len(res)):
    print ("Test-"+str(i)+": " + "{0:b}".format(res[i]).zfill(n_qubits))
