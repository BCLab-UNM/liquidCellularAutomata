#!/usr/bin/env python3
import turtle
import random  # for choice & randint 
import time  # for sleep
import math  # for sqrt
import argparse


class Agent:
  def __init__(self, node_degree=5):
    self.turt = turtle.Turtle()
    self.seed = None
    self.radius = None
    self.node_degree = node_degree
    self.group_id = 0  # for later clumping into different step timings
    self.duplex = None  # 4 states: does it get influenced or is an influencer
    self.original_pose = (self.turt.xcor(), self.turt.ycor())

  def within_range(self, agents):
    agents_in_range = []
    for o_agent in agents:
      dist = math.sqrt(abs(agent.turt.xcor() - o_agent.turt.xcor()) ** 2 +
                       abs(agent.turt.ycor() - o_agent.turt.ycor()) ** 2)
      if dist <= radius:
        agents_in_range.append((dist, o_agent))
    agents_in_range.sort(key=lambda agent: agent[0])
    return [agent_in_range[1] for agent_in_range in agents_in_range[:self.node_degree]]


def consensus(agents):
  colors = ["white", "black"]
  return max(set(colors), key=[agent.turt.color()[1] for agent in agents].count)


def consensus_reached(agents):
  return not any([not (agents[0].turt.color()[1] == agent.turt.color()[1]) for agent in agents])


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--agents', type=int, default=256, help='number of agents')
  parser.add_argument('--seed', type=int, default=random.randint(0, 9000), help='rng seed')
  parser.add_argument('--vis', action='store_true', help='Enable visualization')  # False default
  # Agent list with a list of args per?

  # ### Change things here while testing ###
  args = vars(parser.parse_args())
  # @NOTE we are always visualzing right now
  print(args)
  # args for time(speed), radius, colors, color balance, walk angles/type,rng seed

  # Initialize turtle environment
  screen = turtle.Screen()
  screen.title("LCA")
  screen.tracer(False)
  half_width = int(screen.window_width() / 2)
  print(half_width)
  half_height = int(screen.window_height() / 2)
  print(half_height)

  # Config values
  random.seed(args['seed'])
  radius = 20.0
  colors = ["white", "black"]

  # Initialize all of the agents
  agents = [Agent() for _ in range(args['agents'])]
  for agent in agents:
    agent.turt.penup()
    agent.turt.shape("circle")
    agent.turt.color("black", random.choice(colors))
    x = random.randint(-half_width, half_width)
    y = random.randint(-half_height, half_height)
    agent.turt.goto(x,y)
  screen.update()
  print("Starting consensus: ", consensus(agents))

  # Main loop
  loop_times = 0
  while not consensus_reached(agents):
    # movement
    loop_times = loop_times + 1
    for agent in agents:
      # if at edge bounce, @NOTE still can get stuck
      if abs(agent.turt.ycor()) > half_height or abs(agent.turt.xcor()) > half_width:
        agent.turt.back(5)  # this should reduce getting stuck at the edge
        # 180 would perfect bounce but at the corner would be bad could get stuck oscillating
        agent.turt.right(random.randint(160, 200))

      # correlated random walk
      agent.turt.right(random.randint(-45, 45))
      agent.turt.forward(random.randint(5, 10))
      # update agent color value with black outline
      new_consensus = consensus(agent.within_range(agents))
      if agent.turt.color()[1] != new_consensus:
        agent.turt.color("black", new_consensus)
        # agent.turt.right(random.randint(160, 200))  # if we changed then bounce
        agent.turt.right(180)  # if we changed state then bounce
    screen.update()

  # Print out results from experiment
  turtle.write("Consensus of " + agents[0].turt.color()[1] + " reached\nAfter " + str(loop_times) + " iterations",
               move=True, align="center")
  print("Consensus of", agents[0].turt.color()[1], "reached")
  print("After", str(loop_times), "iterations")
  time.sleep(5)
