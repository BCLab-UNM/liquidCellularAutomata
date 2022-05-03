#!/usr/bin/env python3
import turtle
import random  # for choice & randint 
import time  # for sleep
import math  # for sqrt
import argparse

class Agent:
  def __init__(self, x=None, y=None, node_degree=5, half_height=100, half_width=100, args=None):
    if args is None:
      args = dict()
    x = x if x else random.randint(-half_width, half_width)
    y = y if y else random.randint(-half_height, half_height)
    self.turt = turtle.Turtle()
    self.radius = None
    self.node_degree = node_degree
    self.group_id = 0  # for later clumping into different step timings
    self.duplex = None  # 4 states: does it get influenced or is an influencer
    self.original_pose = (x, y)
    self.turt.penup()
    self.turt.goto(x, y)
    self.turt.shape("circle")
    self.turt.color("black", random.choices(args['colors'], weights=args['weights'], k=1)[0])

  def within_range(self, agents):
    agents_in_range = []
    for o_agent in agents:
      dist = math.sqrt(abs(agent.turt.xcor() - o_agent.turt.xcor()) ** 2 +
                       abs(agent.turt.ycor() - o_agent.turt.ycor()) ** 2)
      if dist <= radius:
        agents_in_range.append((dist, o_agent))
    agents_in_range.sort(key=lambda bob: bob[0])
    return [agent_in_range[1] for agent_in_range in agents_in_range[:self.node_degree]]

def consensus(agents, colors, agent=None):
  agent_colors = [agent.turt.color()[1] for agent in agents]
  black_count = 0
  white_count = 0
  for color in agent_colors:
    if color == "black":
        black_count += 1
    if color == "white":
        white_count += 1

  if black_count > white_count:
    return "black"
  elif white_count > black_count:
    return "white"
  else:
    if agent:
        return agent.turt.color()[1]
    else:
        return "equal"

  #return max(colors, key=agent_colors.count)


def consensus_reached(agents):
  return not any([not (agents[0].turt.color()[1] == agent.turt.color()[1]) for agent in agents])


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--agents', type=int, default=256, help='number of agents')
  parser.add_argument('--seed', type=int, default=random.randint(0, 9000), help='rng seed')
  parser.add_argument('--node_degree', type=int, default=2, help='node degree')
  parser.add_argument('--radius', type=float, default=20.0, help='radius of local network')
  parser.add_argument('--sleep', type=float, default=0.0, help='Step Sleep in seconds')
  parser.add_argument('--vis', action='store_true', help='Enable visualization')  # False default
  parser.add_argument('--bounce', action='store_true', help='Bounce on state change')  # False default
  parser.add_argument('-c', '--colors', nargs='+', default=["white", "black"], help='list of colors')
  parser.add_argument('-w', '--weights', nargs='+', default=[0.6, 0.4], help='list of weights of said colors')
  parser.add_argument('--min_walk_angle', type=int, default=-45, help='walk step min angle turned')
  parser.add_argument('--max_walk_angle', type=int, default=45, help='walk step max angle turned')
  parser.add_argument('--min_walk_distance', type=float, default=5, help='min walk step distance forward')
  parser.add_argument('--max_walk_distance', type=float, default=10, help='max walk step distance forward')
  parser.add_argument('--output', type=str, default=None, help='output name postfix')

  args = vars(parser.parse_args())
  # @NOTE we are always visualzing right now
  #print(args)
  # args for time(speed), radius, colors, color balance, walk angles/type,rng seed

  # Initialize turtle environment
  screen = turtle.Screen()
  screen.title("LCA")
  screen.tracer(False)
  half_width = 300
  #half_width = int(screen.window_width() / 2)
  #print(half_width)
  half_height = 300
  #half_height = int(screen.window_height() / 2)
  #print(half_height)

  # Config values
  random.seed(args['seed'])
  radius = args['radius']
  colors = args['colors']
  degree = args['node_degree']
  # Initialize all of the agents
  agents = [Agent(half_width=half_width, half_height=half_height, node_degree=degree, args=args) for _ in range(args['agents'])]
  screen.update()
  print("Seed:", args['seed'])
  print("Starting consensus: ", consensus(agents, colors))
  print(colors)
  if args['output']:
    turtle.getscreen().getcanvas().postscript(file=args['output'] + "_start.eps")

  # Main loop
  loop_times = 0
  while not consensus_reached(agents):
    if loop_times % 100 == 0:
      print([[agent.turt.color()[1] for agent in agents].count(color) for color in colors])
    if loop_times > 15000:
      print("terminated early")  
      exit()
      # movement
    for agent in agents:

      if abs(agent.turt.ycor()) > half_height or abs(agent.turt.xcor()) > half_width:  
      # if at edge bounce, @NOTE still can get stuck
        my_x = agent.turt.xcor()
        my_y = agent.turt.ycor()
        if abs(agent.turt.ycor()) > half_height:
          if (agent.turt.ycor() <= 0):
            my_y = -half_height + 1
          else:
            my_y = half_height - 1 
        if abs(agent.turt.xcor()) > half_width:
          if (agent.turt.xcor() <= 0):
            my_x = -half_width + 1
          else:
            my_x = half_width - 1
        # agent.turt.back(args['max_walk_distance']+1)  # this should reduce getting stuck at the edge
        
        # 180 would perfect bounce but at the corner would be bad could get stuck oscillating
        agent.turt.right(random.randint(160, 200))
        agent.turt.goto(my_x, my_y)
      # correlated random walk
      agent.turt.right(random.randint(args['min_walk_angle'], args['max_walk_angle']))
      agent.turt.forward(random.randint(args['min_walk_distance'], args['max_walk_distance']))

      # update agent color value with black outline
      new_consensus = consensus(agent.within_range(agents), colors, agent=agent)
      if agent.turt.color()[1] != new_consensus:
        agent.turt.color("black", new_consensus)
        if args['bounce']:
          agent.turt.right(180)  # if we changed state then bounce, could use random.randint(160, 200)
    screen.update()
    loop_times = loop_times + 1

  # Print out results from experiment
  turtle.write("Consensus of " + agents[0].turt.color()[1] + " reached\nAfter " + str(loop_times) + " iterations",
               move=True, align="center")
  if args['output']:
    turtle.getscreen().getcanvas().postscript(file=args['output'] + "_end.eps")
  print("Consensus of", agents[0].turt.color()[1], "reached")
  print("After", str(loop_times), "iterations")
