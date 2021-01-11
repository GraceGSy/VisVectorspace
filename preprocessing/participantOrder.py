import random

equalCount = False

def isEqual(s):
	if len(s) != 12:
		return False
	learnerCount = 0
	solverCount = 0
	for choice in s:
		if choice == "constraintLearner":
			learnerCount += 1
		else:
			solverCount += 1
		if learnerCount > 6: return False
		if solverCount > 6: return False
	if learnerCount == solverCount:
		return True
	return False

while not equalCount:
	order = []
	for i in range(12):
		select = random.choice(["constraintLearner", "constraintSolver"])
		order.append(select)
	equalCount = isEqual(order)
	if equalCount:
		print(order)

['constraintSolver',
'constraintLearner',
'constraintSolver',
'constraintSolver',
'constraintSolver',
'constraintLearner',
'constraintSolver',
'constraintLearner',
'constraintLearner',
'constraintSolver',
'constraintLearner',
'constraintLearner']