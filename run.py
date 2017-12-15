#
#
from time import sleep
import world
import numpy as np
import sys
import agent


def run(ghost_nbr):
	print "ghosts:", ghost_nbr
	
	wrld = world.World(ghost_nbr)
	wrld.initialize()
	wrld.show()
	agnt = agent.GreedyAgent()

	for i in range(50):
		available_actions = wrld.get_legal_actions(wrld.agent)
		move = agnt.get_action(available_actions=available_actions, 
								my_coords=wrld.agent, 
								food=wrld.food,
								ghosts=wrld.ghosts)

		agent_caught, food_eaten = wrld.take_agents_action(move)
		wrld.show()

		if agent_caught:			
			break
		else:
			agnt.food += food_eaten
		sleep(0.3)
	print "food_eaten:", agnt.food



if __name__ == '__main__':
	if len(sys.argv) == 2:
		ghost_nbr = int(sys.argv[1])
	else:
		ghost_nbr = 2
	run(ghost_nbr)