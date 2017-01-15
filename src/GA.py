import random
import math
from kung import getDominantSet

def permutation2inversion(permutation):

    inversion = []

    for i in range(len(permutation)):
        inversion.append(0)
        m = 0
        while permutation[m] != i:
            if permutation[m] > i: 
                inversion[i] += 1
            m += 1

    return inversion

def inversion2permutation(inversion):

    permutation = [0] * len(inversion)
    pos = [0] * len(inversion)

    l = range(len(inversion))
    l.reverse()

    for i in l:
        for m in range(i,len(inversion)):

            if pos[m] >= inversion[i] + 1:
                pos[m] += 1
        pos[i] = inversion[i] + 1

    for i in range(len(inversion)):
        permutation[pos[i]-1] = i

    return permutation

# http://antoinecomeau.blogspot.com/2014/07/mapping-between-permutations-and.html

def int2perm(n, k):
    m = k

    permuted = [0] * n
    elems = []

    for i in range(n):
        elems.append(i)

    for i in range(n):
        ind = m % (n-i)
        m = m / (n-i)
        permuted[i] = elems[ind]
        elems[ind] = elems[n-i-1]

    return permuted

def perm2int(permutation):
    n = len(permutation)

    pos = []
    elems = []

    k = 0
    m = 1

    for i in range(n):
        pos.append(i)
        elems.append(i)

    for i in range(n-1):
        k += m * pos[permutation[i]]
        m = m * (n-i)
        pos[elems[n-i-1]] = pos[permutation[i]]
        elems[pos[permutation[i]]] = elems[n-i-1]

    return k 

class Design:
    
    def __init__(self, genNum, desNum, id):
        self.genNum = genNum
        self.desNum = desNum
        self.id = id
        self.inputs = []
        self.objectives = []
        self.feasible = True
        self.penalty = 0
        self.rank = 0

    def get_id(self):
        return self.id

    def get_genNum(self):
        return self.genNum

    def get_desNum(self):
        return self.desNum
    
    def set_inputs(self, inputs):
        self.inputs = inputs

    def get_inputs(self):
        return self.inputs

    def set_outputs(self, outputs, outputsDef, usingConstraints):
        if usingConstraints:
            for i,_o in enumerate(outputs):
                if outputsDef[i]["type"] == "objective":
                    self.objectives.append(_o)
                elif outputsDef[i]["type"] == "constraint":
                    goal = outputsDef[i]["goal"].split(" ")
                    goal_def = " ".join(goal[:-1])
                    goal_val = float(goal[-1])

                    if goal_def == "less than":
                        if _o > goal_val:
                            self.penalty += 1
                            self.feasible = False
                    elif goal_def == "greater than":
                        if _o < goal_val:
                            self.penalty += 1
                            self.feasible = False
                    elif goal_def == "equals":
                        if _o != goal_val:
                            self.penalty += 1
                            self.feasible = False
        else:
            self.objectives = outputs

    def get_objectives(self):
        return self.objectives

    def get_feasibility(self):
        return self.feasible

    def get_penalty(self):
        return self.penalty

    def update_rank(self, var):
        self.rank = var

    def get_rank(self):
        return self.rank
    
    def crossover(self, partner, inputsDef, genNum, desNum, idNum):
        child = Design(genNum, desNum, idNum)

        childInputs = []
        
        for i in range(len(self.inputs)):
            if inputsDef[i]["type"] == "continuous":

                # establish spread of possible values based on values from two parents
                x1 = self.get_inputs()[i]
                x2 = partner.get_inputs()[i]
                d = abs(x1 - x2)
                y1 = min(x1, x2) - d/3
                y2 = max(x1, x2) + d/3

                newVal = y1 + (y2-y1) * random.random()
                clippedVal = float(max(inputsDef[i]["range"][0], min(newVal, inputsDef[i]["range"][1])))

                # print x1, "+", x2, "=", clippedVal

                # choose random value from range
                childInputs.append( clippedVal )

            elif inputsDef[i]["type"] == "categorical":
                # coin flip
                childInputs.append( self.get_inputs()[i] if random.random() > 0.5 else partner.get_inputs()[i] )
            elif inputsDef[i]["type"] == "series":
                # coin flip on each value of series
                a = self.get_inputs()[i]
                b = partner.get_inputs()[i]
                newSeries = [a[j] if random.random() > 0.5 else b[j] for j in range(len(a))]
                childInputs.append( newSeries )
            elif inputsDef[i]["type"] == "sequence":

                print "genes [", self.get_desNum(), "] :", self.get_inputs()[i]
                print "genes [", partner.get_desNum(), "] :", partner.get_inputs()[i]

                a = permutation2inversion(self.get_inputs()[i])
                b = permutation2inversion(partner.get_inputs()[i])

                parents = [a,b]

                # single-point crossover on inverted sequences (not currently in use)
                # choose random crossover point
                # point = random.choice(range(1,len(a)))
                # choose crossover point in the middle
                # point = int(len(a)/2.0)
                # print "crossover point:", point

                # choose random parent to define first half of chromosome
                # h1 = parents.pop(int(round(random.random())))[:point]
                # use other parent for second half of chromosome
                # h2 = parents[0][point:]

                # calculate new permutation from new chromosome
                # newSequence = inversion2permutation(h1 + h2)

                # coin flip on each value of inverted sequence
                newSequence = inversion2permutation([a[j] if random.random() > 0.5 else b[j] for j in range(len(a))])

                childInputs.append( newSequence )
                print "genes [", child.get_desNum(), "] :", newSequence

        child.set_inputs(childInputs)
        
        return child
    
    def mutate(self, inputsDef, mutationRate):
        for i in range(len(self.inputs)):
            # mutation based on probability
            if random.random() < mutationRate:
                if inputsDef[i]["type"] == "continuous":
                    # jitter input based on normal distribution
                    x = self.get_inputs()[i]
                    goalRange = float(abs(inputsDef[i]["range"][1] - inputsDef[i]["range"][0]))
                    newVal = self.inputs[i] + random.gauss(0, goalRange/5.0)
                    # final value clipped by bounds
                    mutation = float(max(inputsDef[i]["range"][0], min(newVal, inputsDef[i]["range"][1])))
                elif inputsDef[i]["type"] == "categorical":
                    # random assignment
                    mutation = int(math.floor(random.random() * inputsDef[i]["num"]))
                elif inputsDef[i]["type"] == "series":
                    # random assignment for randomly chosen value in series
                    newSeries = list(self.inputs[i])
                    for j in range(len(newSeries)):
                        if random.random() < inputsDef[i]["mutationRate"]:
                            newSeries[j] = int(math.floor(random.random() * inputsDef[i]["depth"]))
                    mutation = newSeries
                elif inputsDef[i]["type"] == "sequence":
                    # some number of random swaps based on input-specific mutation rate 
                    # we want mutation rate to roughly correspond to percentage of sequence altered
                    # since each flip alters 2 places we divide mutation rate by 2
                    numMutations = int(math.ceil(inputsDef[i]["length"] * (inputsDef[i]["mutationRate"] / 2.0)))

                    newSequence = list(self.inputs[i])
                    for j in range(numMutations):
                        choices = range(len(newSequence))
                        choice1 = choices.pop(choices.index(random.choice(choices)))
                        choice2 = choices.pop(choices.index(random.choice(choices)))

                        val1 = newSequence[choice1]
                        val2 = newSequence[choice2]
                        newSequence[choice2] = val1
                        newSequence[choice1] = val2
                    mutation = newSequence

                print "mutation: ", self.desNum, "/", str(i), ":", self.inputs[i], "->", mutation
                self.inputs[i] = mutation


def rank(population, outputsDef, g, numGenerations, usingConstraints):

    designs = []
    for i, des in enumerate(population):
        designs.append({'id': i, 'scores': des.get_objectives()})

    objectiveGoals = [x["goal"] for x in outputsDef if x["type"] == "objective"]

    validSet = [x for x in designs if len(x['scores']) == len(objectiveGoals)]

    dom = []
    ranking = []

    P = validSet

    while len(P) > 0:
        ranking.append([x['id'] for x in getDominantSet(P, objectiveGoals)])
        dom = dom + ranking[-1]
        P = [x for x in validSet if x['id'] not in dom]

    # ranking list format = [[design id's in pareto front 1], [design id's in pareto front 2], ...]

    # initialize distances for all designs
    distances = [ 0.0 ] * len(population)

    # calculate crowding factor for each pareto front
    for front in ranking:
        frontDesigns = [design for design in designs if design['id'] in front]

        # compute normalized distance of neighbors for each objective
        for score in range(len(objectiveGoals)):
            sortedDesigns = sorted(frontDesigns, key=lambda k: k['scores'][score])

            # assign infinite distance to boundary points so they are always selected
            distances[sortedDesigns[0]['id']] += float("inf")
            distances[sortedDesigns[-1]['id']] += float("inf")

            # min/max objective values for normalization
            f_min = sortedDesigns[0]['scores'][score]
            f_max = sortedDesigns[-1]['scores'][score]

            # for all interior designs, calculate distance between neighbors
            for i, des in enumerate(sortedDesigns[1:-1]):
                distances[des['id']] += (sortedDesigns[i+2]['scores'][score] - sortedDesigns[i]['scores'][score]) / (f_max - f_min)

    ranking.reverse()

    penalties = [x.get_penalty() for x in population]

    if usingConstraints:
        print "Constraint penalties:", penalties

    rankingOut = [0] * len(population)
    for i, ids in enumerate(ranking):
        for id in ids:
            rankingOut[id] = (i + 1)

    return rankingOut, distances, penalties


def testRanking():

    outputsDef = [
        { "name": "y1", "type": "min"},
        { "name": "y2", "type": "min"}
        ]

    performance = [
        {'id': 0, 'scores': [0, 4]},
        {'id': 1, 'scores': [1, 4]},
        {'id': 2, 'scores': [2, 4]},
        {'id': 3, 'scores': [4, 4]},
        {'id': 4, 'scores': [1, 3]},
        {'id': 5, 'scores': [2, 3]},
        {'id': 6, 'scores': [3, 3]},
        {'id': 7, 'scores': [2, 2]},
        {'id': 8, 'scores': [3, 2]},
        {'id': 9, 'scores': [4, 2]},
        {'id': 10, 'scores': [3, 1]},
        {'id': 11, 'scores': [4, 1]},
        {'id': 12, 'scores': [4, 0]},
        ]

    print rank(performance, outputsDef)

# testRanking()