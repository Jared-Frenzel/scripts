import numpy as np
def roll(string):
	rolls = string.split('+')
	return sum([sum([np.random.choice(int(roll.split('d')[1])) + 1 for _ in range(int(roll.split('d')[0]))]) if 'd' in roll else int(roll) for roll in rolls])


print(roll('2d6 + 7 + 1d20 + 1d100'))
