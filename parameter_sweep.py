#!/usr/bin/env python3
import random
import subprocess
import multiprocessing

# Semaphore to keep track of writing data
import sys

lock = multiprocessing.Lock()


def run_experiment(seed, agents, node_degree, radius):
  command = "python3 lca.py --seed " + str(seed) + " --agents " + str(agents) + " --node_degree " + str(
    node_degree) + " --radius " + str(radius)
  command_array = command.split(" ")
  print(command)
  output = subprocess.check_output(command_array, encoding='UTF-8')
  output_lines = output.split("\n")
  consensus = ""
  iterations = ""
  start = ""
  for line in output_lines:
    if "reached" in line:
      consensus = line.split(" ")[2].strip()
    if "iterations" in line:
      iterations = line.split(" ")[1]
    if "Starting consensus:" in line:
      start = line.split(":")[1].strip()

  lock.acquire()
  with open("./results-lock.csv", "a") as f:
    line_to_write = str(seed) + "," + str(agents) + "," + str(node_degree) + "," + str(radius)
    line_to_write += "," + str(consensus) + "," + str(iterations) + "," + str(start) + "\n"
    f.write(line_to_write)
  lock.release()


def main():
  # Make the header
  with open("./results-lock.csv", "w") as f:
    f.write("seed,agents,node_degree,radius,consensus,iterations,start\n")

  # Create tasks
  tasks = []
  for seed in random.sample(range(sys.maxsize), k=100):
    for agents in range(50, 110, 2):
      for node_degree in range(2, 15):
        radius = 999
        tasks.append((seed, agents, node_degree, radius))

  print("Total of " + str(len(tasks)) + " experiments to be run")

  # Create multiprocessing pool
  with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
    p.starmap(run_experiment, tasks)
  p.join()


if __name__ == "__main__":
  sweep_seed = random.randrange(sys.maxsize)
  random.Random(sweep_seed)
  print("Sweep seed:", sweep_seed)
  main()
