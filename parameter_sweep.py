import sys
import glob
import subprocess
import multiprocessing



def run_experiment(seed, agents):
    command = "python3 lca.py --seed " + str(seed) + " --agents " + str(agents)
    command_array = command.split(" ")
    print(command)
    output = subprocess.check_output(command_array)
    print(output)

def main():
    
    #Create tasks
    tasks = []
    for i in range(0,10):
        for b in range(50,100):
            tasks.append((i,b))
    p = multiprocessing.Pool(4)

    p.starmap(run_experiment, tasks)

if __name__ == "__main__":
    main()

