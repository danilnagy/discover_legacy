from src import job

jobDescription = {
	"jobName": "pill",
	"inputsDef": [
		{ "name": "r1", "type": "continuous", "range": [0,5]},
		{ "name": "r2", "type": "continuous", "range": [0,5]},
		{ "name": "r3", "type": "continuous", "range": [0,5]},
		],
	"outputsDef": [
		{ "name": "surface area", "type": "objective", "goal": "min"},
		{ "name": "volume", "type": "objective", "goal": "max"},
		],
	"algo": "GA",
	"algoOptions": {
		"numGenerations": 20,
		"numPopulation": 20,
		"mutationRate": 0.25,
		"saveElites": 1
		},
	"jobOptions": {
		"screenshots": True
		}
	}

job.createInputFile(jobDescription)
# job.run(jobDescription)