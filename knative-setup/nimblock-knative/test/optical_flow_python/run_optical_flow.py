import subprocess
import time


command = "./optical_flow_sw.exe -p datasets/current/ -o output.flo"
start_time = time.time()
for i in range(10):
    response = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(response)
end_time = time.time()

print("Start time: " + str(start_time) + ", End time: " + str(end_time))  
