#
#
from time import sleep
import world
import numpy as np
import sys
import agent
import pickle


def run(ghost_nbr):
	print "ghosts:", ghost_nbr
	
	wrld = world.World(ghost_nbr)
	wrld.initialize()
	wrld.show()
	
	# agnt = agent.GreedyAgent()
	# agnt = agent.RandomAgent()
	agnt = agent.LearningAgent()

	for i in range(200):
		available_actions = wrld.get_legal_actions(wrld.agent)
		move = agnt.get_action(available_actions=available_actions, 
								my_coords=wrld.agent, 
								food=wrld.food,
								ghosts=wrld.ghosts)

		agent_caught, food_eaten = wrld.take_agents_action(move)
		wrld.show()

		agnt.observe(agent_caught, food_eaten, wrld)

		if agent_caught:			
			break
		sleep(0.5)
	print "food_eaten:", agnt.food, "time:", i


def train(n=1000):
	ghost_nbr = 4
	agnt = agent.LearningAgent()
	for i in range(n):
		if i%100 == 0: print "epoch:", i
		wrld = world.World(ghost_nbr)
		wrld.initialize()

		for i in range(200):
			available_actions = wrld.get_legal_actions(wrld.agent)
			move = agnt.get_action(available_actions=available_actions, 
									my_coords=wrld.agent, 
									food=wrld.food,
									ghosts=wrld.ghosts)

			agent_caught, food_eaten = wrld.take_agents_action(move)
			
			agnt.observe(agent_caught, food_eaten, wrld)

			if agent_caught:			
				break
	f = open('qtab.dat', 'wb')
	pickle.dump(agnt.qTab, f)
	f.close()




if __name__ == '__main__':
	if len(sys.argv) == 2:
		ghost_nbr = int(sys.argv[1])
	else:
		ghost_nbr = 2
	run(ghost_nbr)