import math

def getDominantSet(data, objectiveGoals):

	# single objective ranking
	if len(objectiveGoals) == 1:
		scores = [float(x['scores'][0]) for x in data]
		if objectiveGoals[0] == "min":
			return [data[scores.index(min(scores))]]
		else:
			return [data[scores.index(max(scores))]]

	# multi-objective ranking
	else:
		P = sorted(data, key = lambda x: x['scores'][0])
		return front(P, objectiveGoals)

def front(P, objectiveGoals):

	if (len(P) == 1):
		return P
	else:
		div = int(math.floor(len(P)/2.0))
		T = front(P[:div], objectiveGoals)
		B = front(P[div:], objectiveGoals)
		M = []

		for des1 in B:
			dominated = True
			for des2 in T:
				dominated = True
				for k in range(len(des1['scores'])):
					# if target is not min, fac is -1 (reverse dominance criteria for maximization objective)
					fac = (objectiveGoals[k] == "min") * 2 - 1
					if (fac * float(des1['scores'][k])) < (fac * float(des2['scores'][k])):
						dominated = False
						break
				if dominated:
					break
			if not dominated:
				M.append(des1)
		return T + M