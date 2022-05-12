#!/usr/bin/env python3
import random
import subprocess
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed

import lca
# Semaphore to keep track of writing data
import sys
import threading
from multiprocessing.pool import ThreadPool

lock = multiprocessing.Lock()


def main():
  # Make the header
  with open("./results-lock.csv", "w") as f:
    f.write("seed,agents,node_degree,radius,consensus,iterations,start\n")

  # Create tasks
  tasks = []
  for seed in random.sample(range(sys.maxsize), k=3):
    for agents in range(50, 100, 2):
      for node_degree in range(2, 16):
        for radius in range(20, 50, 2):
          tasks.append(threading.Thread(target=lca.main({'agents': agents, 'seed': seed, 'node_degree': node_degree,
                                                         'radius': radius,
                                    'vis': True, 'bounce': False, 'colors': ["white", "black"], 'weights': [0.6, 0.4],
                                    'min_walk_angle': -45, 'max_walk_angle': 45, 'min_walk_distance': 5,
                                    'max_walk_distance': 10, 'output': None})))

  print("Total of " + str(len(tasks)) + " experiments to be run")

  with ThreadPoolExecutor(multiprocessing.cpu_count()) as executor:
    futures = [executor.submit(task) for task in tasks]
    for future in as_completed(futures):
      print(future.result())
      """
      lock.acquire()
      with open("./results-lock.csv", "a") as f:
        line_to_write = str(seed) + "," + str(agents) + "," + str(node_degree) + "," + str(radius)
        line_to_write += "," + str(consensus) + "," + str(iterations) + "," + str(start) + "\n"
        f.write(line_to_write)
      lock.release()
      """

if __name__ == "__main__":
  sweep_seed = random.randrange(sys.maxsize)
  random.Random(sweep_seed)
  print("Sweep seed:", sweep_seed)
  main()
