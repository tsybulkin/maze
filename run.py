#
#
from time import sleep
import world
import numpy as np
import sys


def run(ghost_nbr):
	print "ghosts:", ghost_nbr
	
	wrld = world.World(ghost_nbr)
	wrld.initialize()
	score = 0
	wrld.show()

	for i in range(50):
		available_actions = wrld.get_legal_actions(wrld.agent)
		move = np.random.choice(available_actions)
		agent_caught, food_eaten = wrld.take_agents_action(move)
		wrld.show()

		if agent_caught:			
			break
		else:
			score += food_eaten
		sleep(0.3)
	print "food_eaten:", score



if __name__ == '__main__':
	if len(sys.argv) == 2:
		ghost_nbr = int(sys.argv[1])
	else:
		ghost_nbr = 2
	run(ghost_nbr)