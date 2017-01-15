from GA import Design, rank
from util import *


def run(jobDescription):

	try:
		jobName, inputsDef, outputsDef, algo, algoOptions, jobOptions = parseJobDescription(jobDescription)
	except TypeError:
		return

	paths, meta = init(jobName)

	print "Starting", algo, "algorithm..."

	if algo == "GA":
		error = runGA(inputsDef, outputsDef, algoOptions, jobOptions, paths, meta)
		if error is not None:
			print "error:", error

	elif algo == "random":
		error = runRandom(inputsDef, outputsDef, algoOptions, jobOptions, paths, meta)
		if error is not None:
			print "error:", error

	cleanup(paths["local"])


def runGA(inputsDef, outputsDef, algoOptions, jobOptions, paths, meta):

	# check if using constraints
	types = [x["type"] for x in outputsDef]
	usingConstraints = "constraint" in types

	# create results file header
	header = []
	header.append("id")
	header.append("generation")

	if usingConstraints:
		header.append("feasible")

	for _i in inputsDef:
		if _i["type"] == "series":
			header.append("[ser " + str(_i["depth"]) + "] " + _i["name"])
		elif _i["type"] == "sequence":
			header.append("[seq " + str(_i["length"]) + "] " + _i["name"])
		else:
			header.append("[in] " + _i["name"])
	for _o in outputsDef:
		header.append("[" + _o["goal"] + "] " + _o["name"])

	with open(paths["results"], 'a') as f:
		f.write("\t".join(header))

	# load options
	numGenerations = algoOptions["numGenerations"]
	numPopulation = algoOptions["numPopulation"]
	mutationRate = algoOptions["mutationRate"]
	saveElites = algoOptions["saveElites"]

	# initialise id
	idNum = 0

	# create initial population of designs
	population = []
	for i in range(int(numPopulation)):
		population.append(Design(0, i, idNum))
		idNum += 1

	print "Setting initial population..."

	# set random inputs for first generation
	for des in population:
		newInputs = []
		for _i in inputsDef:
			newInputs.append(create_input(_i))
		des.set_inputs(newInputs)

	for g in range(numGenerations):

		print "Computing designs for generation", str(g), "..."

		# for each design, calculate output metrics
		for des in population:

			meta, outputs = computeDesign(des.get_id(), des.get_inputs(), jobOptions, paths, meta)
			if outputs is None:
				return "model unresponsive"
			des.set_outputs(outputs, outputsDef, usingConstraints)

			print des.get_genNum(), "/", des.get_desNum(), ":", outputs
			
			# write results file
			with open(paths["results"], 'a') as f:
				d = [des.get_id(),des.get_genNum()]
				if usingConstraints:
					d.append(des.get_feasibility())
				f.write("\n" + "\t".join([str(x) for x in (d + printFormat(des.get_inputs(), inputsDef) + outputs)]))

		# compute ranking for population (higher value is better performance)
		ranking, crowding, penalties = rank(population, outputsDef, g, numGenerations, usingConstraints)
		print "Generation ranking:", ranking
		if len(outputsDef) > 1:
			print "Generation crowding:", [float("%.2f" % distance) for distance in crowding]

		# create new empty list of children
		children = []

		# combine all criteria in order of importance
		stats = [ [penalties[i], ranking[i], crowding[i]] for i in range(len(ranking))]

		# carry over elite to next generation
		if saveElites > 0:
			# get elites from sorted list of ranking and crowding
			elites = [i[0] for i in sorted(enumerate(stats), key=lambda x: (x[1][0], -x[1][1], -x[1][2]))][:saveElites]
			print "elite(s):", elites

			# add elites to next generation
			for i, eliteNum in enumerate(elites):
				child = Design(g+1, i, idNum)
				child.set_inputs(population[eliteNum].get_inputs())
				children.append(child)
				idNum += 1

		# MATING POOL SELECTOR (NOT CURRENTLY IN USE)
		# add designs to mating pool based on ranking
		# matingPool = []
		# for i, order in enumerate(ranking):
		# 	for j in range(order):
		# 		matingPool.append(population[i])

		# for i in range(len(population) - saveElites):				
		# 	parentA = matingPool[random.choice(range(len(matingPool)))]
		# 	parentB = matingPool[random.choice(range(len(matingPool)))]

		# 	child = parentA.crossover(parentB, inputsDef, g+1, saveElites+i, idNum)
		# 	child.mutate(inputsDef, mutationRate)
		# 	children.append(child)
		# 	idNum += 1

		# TOURNAMENT SELECTOR
		# for each new child...

		childNum = saveElites
		while childNum < len(population):
		# for i in range(len(population) - saveElites):
			# choose two parents through two binary tournaments
			pool = range(len(population))
			parents = []
			for j in range(2):
				# select one candidate from pool
				candidate1 = random.choice(pool)
				# take first candidate out of pool
				pool.pop(pool.index(candidate1))
				# select another candidate from remaining pool
				candidate2 = random.choice(pool)
				# take second candidate out of pool
				pool.pop(pool.index(candidate2))

				candidates = [[x, stats[x]] for x in [candidate1, candidate2]]
				standings = sorted( candidates, key=lambda x: (x[1][0], -x[1][1], -x[1][2]) )

				print "tournament:", candidate1, "/", candidate2, "->", standings[0][0]

				# add winner to parent set
				parents.append(standings[0][0])
				# add loser back to pool
				pool.append(standings[1][0])

			print "breeding:", parents, "->", childNum

			child = population[parents[0]].crossover(population[parents[1]], inputsDef, g+1, childNum, idNum)
			child.mutate(inputsDef, mutationRate)

			if not checkDuplicates(child, children):
				children.append(child)
				idNum += 1
				childNum += 1
			else:
				print "duplicate child, skipping..."

		# set children list as next population
		population = children


def runRandom(inputsDef, outputsDef, algoOptions, jobOptions, paths, meta):

	# create results file header
	header = []
	header.append("id")

	for _i in inputsDef:
		header.append("in_" + _i["name"])
	for _o in outputsDef:
		header.append(_o["type"] + "_" + _o["name"])

	with open(paths["results"], 'a') as f:
		f.write(",".join(header))

	# load options
	numPopulation = algoOptions["numPopulation"]

	for idNum in range(numPopulation):

		newInputs = []
		for _i in inputsDef:
			newInputs.append(create_input(_i))

		meta, outputs = computeDesign(idNum, newInputs, jobOptions, paths, meta)
		if outputs is None:
			return "model unresponsive"

		print idNum, ":", outputs
		
		with open(paths["results"], 'a') as f:
			f.write("\n" + ",".join([str(x) for x in ([idNum] + printFormat(newInputs, inputsDef) + outputs)]))