import random

NUM_REPLAY = 10
REPLAY_LEN = 10  

delay_min = 1500
delay_max = 2000

input_seq_file = "input_data/standard_lenet_het.py"


event_nums_no_knn = [0, 2, 3, 4, 5]
event_nums_no_alexnet = [0, 2, 3, 4]
event_nums = [0, 1, 2, 3, 4, 5]

max_batches = [30, 1, 30, 30, 20, 10]
max_batches_low = [10, 1, 10, 10, 5, 3]
priority_levels = [1, 3, 9]

def select_batch(max_size):
    return random.randint(1, max_size)

def select_event_delay(min_d, max_d):
    return 1.0*random.randint(min_d, max_d)/1000.0

def main():
    events = []
    batches = []
    priorities = []
    delays = []
    for _ in range (NUM_REPLAY):
        sub_list = []
        knn = False
        alexnet = 0
        knn = 0
        for j in range(REPLAY_LEN):
            if knn > -1:
                if alexnet < 5:
                    item = random.choice(event_nums_no_knn)
                    if item == 5:
                        alexnet += 1
                else:
                    item = random.choice(event_nums_no_alexnet)
            else:
                if alexnet < 5:
                    item = random.choice(event_nums)
                    if item == 1:
                        knn += 1
                    if item == 5:
                        alexnet += 1
                else:
                    item = random.choice(event_nums_no_alexnet)

            item = 0 
            sub_list.append(item)
        events.append(sub_list)

    for _ in range (NUM_REPLAY):
        sub_list = []
        sub_list2 = []
        for j in range(REPLAY_LEN):
            sub_list.append(random.choice(priority_levels))
            sub_list2.append(select_event_delay(delay_min,delay_max))
        priorities.append(sub_list)
        delays.append(sub_list2)

    for large in events:
        sub_batch = []
        for e in large:
            #sub_batch.append(1)
            sub_batch.append(select_batch(max_batches_low[e]))
        batches.append(sub_batch)


    with open(input_seq_file, "w") as f:
        f.write("#Begining replay test sequence\n")
        f.write("EventNumbers = ")
        f.write("[")
        for i in range(NUM_REPLAY):
            f.write("[")
            for j in range(REPLAY_LEN):
                if j == REPLAY_LEN -1:
                    f.write(" " + str(events[i][j]))
                else:
                    f.write( " " + str(events[i][j]) + ",")
            if i == NUM_REPLAY-1:
                f.write("]")
            else:
                f.write("],")
        f.write("]\n")

        f.write("BatchNumbers = ")
        f.write("[")
        for i in range(NUM_REPLAY):
            f.write("[")
            for j in range(REPLAY_LEN):
                if j == REPLAY_LEN -1:
                    f.write(" " + str(batches[i][j]))
                else:
                    f.write( " " + str(batches[i][j]) + ",")
            if i == NUM_REPLAY-1:
                f.write("]")
            else:
                f.write("],")
        f.write("]\n")

        f.write("PriorityNumbers = ")
        f.write("[")
        for i in range(NUM_REPLAY):
            f.write("[")
            for j in range(REPLAY_LEN):
                if j == REPLAY_LEN -1:
                    f.write(" " + str(priorities[i][j]))
                else:
                    f.write( " " + str(priorities[i][j]) + ",")
            if i == NUM_REPLAY-1:
                f.write("]")
            else:
                f.write("],")
        f.write("]\n")

        f.write("DelayNumbers = ")
        f.write("[")
        for i in range(NUM_REPLAY):
            f.write("[")
            for j in range(REPLAY_LEN):
                if j == REPLAY_LEN -1:
                    f.write(" " + str(delays[i][j]))
                else:
                    f.write( " " + str(delays[i][j]) + ",")
            if i == NUM_REPLAY-1:
                f.write("]")
            else:
                f.write("],")
        f.write("]\n")
    #print(events)
    #print(batches)
    #print(priorities)
    #print(delays)

if __name__ == "__main__":
    main()

