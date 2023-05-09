import sys

het_log_file = "output_data/" + sys.argv[1] + ".txt"

#cpu_log_file = "output_data/lenet_cpu.txt"
fpga_log_file = "output_data/realtime_mixed_fpga2.txt"
#het_log_file = "output_data/lenet_het.txt"

replays = 10

het_overall = 0.0
cpu_overall = 0.0

for i in range(replays):
    times_fpga = []
    #times_cpu = []
    times_het = []

    fpga_log_file_r = fpga_log_file + str(i)
    fpga = open(fpga_log_file_r, "r")
    #cpu_log_file_r = cpu_log_file + str(i)
    #cpu = open(cpu_log_file_r, "r")
    het_log_file_r = het_log_file + str(i)
    het = open(het_log_file_r, "r")
    for line in fpga:
        if not line.startswith('"'):
            continue
        parts = line.split('|')
        start_time_col2 = float(parts[1].split(' ')[2].strip())
        end_time_col2 = float(parts[1].split(' ')[4].strip())
        times_fpga.append(end_time_col2 - start_time_col2)
    """
    for cpu in cpu:
        if not line.startswith('"'):
            continue
        parts = line.split('|')
        start_time_col2 = float(parts[1].split(' ')[2].strip())
        end_time_col2 = float(parts[1].split(' ')[4].strip())
        times_cpu.append(end_time_col2 - start_time_col2)
    """
    for line in het:
        if not line.startswith('"'):
            continue
        parts = line.split('|')
        start_time_col2 = float(parts[1].split(' ')[2].strip())
        end_time_col2 = float(parts[1].split(' ')[4].strip())
        times_het.append(end_time_col2 - start_time_col2)
    #print(times_fpga)
    #print(times_het)
    overall = 0.0
    for i in range(10):
        base_time = times_fpga[i]
#        cpu_time = times_cpu[i]
        het_time = times_het[i]
#        cpu_overhead = cpu_time/base_time
#        cpu_overall += cpu_overhead
        het_overhead = het_time/base_time
        overall += het_overhead
        #if het_overhead > 1.5:
            #print(f"Times: {het_time} {base_time}")
    het_overhead_seq = overall/10.0
    print(het_overhead_seq)
    het_overall += het_overhead_seq

het_overall_avg = het_overall / float(replays)
#cpu_overall_avg = cpu_overall / float(replays)
print(f"Relative response time: {het_overall_avg}")
#print(f"Het relative response time: {cpu_overall_avg}")

