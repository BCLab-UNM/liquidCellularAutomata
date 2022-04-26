import sys
import glob
import subprocess
import multiprocessing
import logging

lock = multiprocessing.Lock()


def run_experiment(seed, agents, node_degree, radius):
    command = "python3 lca.py --seed " + str(seed) + " --agents " + str(agents) + " --node_degree " + str(node_degree) + " --radius " + str(radius) 
    command_array = command.split(" ")
    print(command)
    output = subprocess.check_output(command_array, encoding='UTF-8')
    print(type(output))
    print(output)

    lock.aquire()
    logging.info(output)
    lock.release()

def main():

    
    fd = open("./results.txt", "w")
    
    #Create tasks
    tasks = []
    for i in range(0,3):
        for b in range(50,100,2):
            for c in range(2,15):
                for d in range(10,50,2):
                    tasks.append((i,b,c,d))

    print("Total of " + str(len(tasks)) + " experiments to be run")


    #Create multiprocessing pool
    p = multiprocessing.Pool(4)
    p.starmap(run_experiment, tasks)
    p.join()
    fd.close()

if __name__ == "__main__":
    main()

