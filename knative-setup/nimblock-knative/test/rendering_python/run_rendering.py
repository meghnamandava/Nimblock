import subprocess
import time


command = "./rendering_sw.exe"
start_time = time.time()
for i in range(10):
    response = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(response)
end_time = time.time()

print("Start time: " + str(start_time) + ", End time: " + str(end_time))  
