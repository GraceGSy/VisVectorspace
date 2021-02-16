import json

participantOrder = ['constraintSolver', 'constraintLearner',
					'constraintSolver', 'constraintSolver',
					'constraintSolver', 'constraintLearner',
					'constraintSolver', 'constraintLearner',
					'constraintLearner', 'constraintSolver',
					'constraintLearner', 'constraintLearner']

baseFilename = "../session_data/sessionData_"

allPinned = []

for i in range(2, 7):

	systemType = participantOrder[i - 1]
	# print()
	# print(systemType)
	filename = baseFilename + str(i) + ".json"

	pinnedVis = {"systemType": systemType}

	pinnedCount = 1

	with open(filename, 'r') as file:
		data = json.load(file)

		sessionData = data["session"]

		for j in sessionData:
			if j["label"] == "pinned":
				pinnedVis["vis" + str(pinnedCount)] = j
				pinnedCount += 1
				# print(j)

	allPinned.append(pinnedVis)

with open("allPinned.json", "w") as wf:
	json.dump(allPinned, wf)