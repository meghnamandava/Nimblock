import sys

log_file_base = "output_data/" + sys.argv[1] + ".txt"
overall = 0.0
overall_resp = 0.0
fpga_resp = 0.0
for i in range(int(sys.argv[2])):
    log_file = log_file_base + str(i)
    with open(log_file, 'r') as f:
        total_overhead = 0
        num_overheads = 0
        for line in f:
            if not line.startswith('"'):
                continue
            parts = line.split('|')
            #print(line)
            start_time_col2 = float(parts[1].split(' ')[2].strip())
            end_time_col2 = float(parts[1].split(' ')[4].strip())
            start_time_col3 = parts[2].split(' ')[2].strip()
            end_time_col3 = parts[2].split(' ')[4].strip()
            if not start_time_col3 or not end_time_col3:
                continue
            if start_time_col3 == 'equest':
                continue
            start_time_col3 = float(start_time_col3)
            end_time_col3 = float(end_time_col3)
            overall_resp += end_time_col2 - start_time_col2
            fpga_resp += end_time_col3 - start_time_col3
            overhead = (end_time_col2 - start_time_col2) / (end_time_col3 - start_time_col3)
            if overhead > 1.5:
                print(line) 
                print(overhead)
            total_overhead += overhead
            num_overheads += 1
        if num_overheads > 0:
            avg_overhead = total_overhead / num_overheads
            print(f"Average overhead: {avg_overhead}")
        else:
            print("No overheads found")
    overall += avg_overhead
overall_avg = overall / float(sys.argv[2])
print(f"Average overhead: {overall_avg}")
overall_resp_avg = overall_resp/6.0 # (float(sys.argv[2])*10.0)
print(f"Average overall resp time: {overall_resp_avg}")
fpga_resp_avg = fpga_resp/6.0 # (float(sys.argv[2])*10.0)
print(f"Average fpga resp time: {fpga_resp_avg}")
    #with open(log_file, 'a') as f:
    #    f.write(f"Average overhead: {avg_overhead}")
