from src import job

# Binh and Korn function
# https://en.wikipedia.org/wiki/Test_functions_for_optimization

jobDescription = {
	"jobName": "function",
	"inputsDef": [
		{ "name": "x1", "type": "continuous", "range": [0,5]},
		{ "name": "x2", "type": "continuous", "range": [0,3]}
		],
	"outputsDef": [
		{ "name": "f1", "type": "objective", "goal": "min"},
		{ "name": "f2", "type": "objective", "goal": "min"},
		# { "name": "g1", "type": "constraint", "goal": "less than 25" },
		# { "name": "g2", "type": "constraint", "goal": "greater than 7.7" }
		],
	"algo": "GA",
	"algoOptions": {
		"numGenerations": 20,
		"numPopulation": 20,
		"mutationRate": 0.05,
		"saveElites": 4
		},
	"jobOptions": {
		"screenshots": False
		}
	}

job.createInputFile(jobDescription)
# job.run(jobDescription)