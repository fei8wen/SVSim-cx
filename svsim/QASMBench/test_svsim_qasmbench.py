import os
import sys
import subprocess
import psutil
import time
#qasmbench = ["small","medium","large"]
#qasmbench = ["small"]
qasmbench = ["medium"]
#qasmbench = ["large"]

rootpath = os.getcwd()
converter = "svsim_qasm.py"
liber = "libsvsim.so"
schm = "summit_gpu_omp"
test_time = 1
cores = [4]
#cores = [1,2,4,8,16]
#cores = [10]
#cores = [1,2,4]
#cores = [1,2,4,8,16,32,64,128,256]
#cores = [1]

def get_val(outstr, mark, stop):
    start_pos = outstr.find(mark)+len(mark)
    stop_pos = outstr.find(stop,start_pos)
    val = outstr[start_pos:stop_pos]
    return val

fout = open(schm+".txt","w")
fout.write("app, qubits, gates, cnots, cores, sim, rss\n")

def run_command_with_memory_reporting(command):
    process = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, text=True)
    process_id = process.pid

    # Create a psutil Process object for monitoring
    ps_process = psutil.Process(process_id)

    peak_rss = 0

    try:
        while process.poll() is None:
            # Monitor memory usage
            memory_info = ps_process.memory_info()
            current_rss = memory_info.rss

            # Update peak RSS if the current value is higher
            peak_rss = max(peak_rss, current_rss)

            # Sleep for a short interval (e.g., 1 second)
            time.sleep(0.01)

    finally:
        # Ensure the subprocess is terminated
        process.terminate()
        process.wait()
        results = {}
        outstr = process.communicate()[0]
        results['sim_time'] = float(get_val(outstr, "sim:", " "))
        results['rss'] = peak_rss
    
    return results

for cat in qasmbench:
    os.chdir(os.path.join(rootpath,cat))
    apps = os.listdir()

    print('Working on the apps:' + str(apps))

    for app in apps[:]:
        os.chdir(os.path.join(rootpath,cat,app))
        convert_cmd = "python " + rootpath + '/' +  converter + " -i " + app + ".qasm"  + " -o " + app + ".py"
        outstr = subprocess.run(convert_cmd, shell=True, stdout=subprocess.PIPE, text=True).stdout
        #print(outstr)
        n_qubits = int(get_val(outstr, "qubits:", "\n"))
        n_basic_gates = int(get_val(outstr, "basic gates:", "\n"))
        n_cnot_gates = int(get_val(outstr, "cnot gates:", "\n"))

        for core in cores:
            run_cmd = "python " + app + ".py " + str(n_qubits) + " " + str(core)
            sim_time = 0.0
            rss = 0
            for _ in range(test_time):
                result = run_command_with_memory_reporting(run_cmd)
                sim_time += result['sim_time']
                rss += result['rss']
            sim_time /=float(test_time)
            outline = app + ", " + str(n_qubits) + ", " + str(n_basic_gates) + ", " + str(n_cnot_gates)\
                    + ", " + str(core) + ", " + f"{sim_time:.2f}s" + ", " + f"Peak Memory Footprint (RSS): {rss / (1024 * 1024):.2f} MB"
            print(outline)
            fout.write(outline+"\n")

fout.close()

