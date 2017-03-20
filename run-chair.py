from src import job

jobDescription = {
	"jobName": "chair",
	"inputsDef": [
		{ "name": "code1", "type": "series", "length": 4, "depth": 4, "mutationRate": 0.5},
		{ "name": "h1-1", "type": "continuous", "range": [0,1]},
		{ "name": "h1-2", "type": "continuous", "range": [0,1]},
		{ "name": "h1-3", "type": "continuous", "range": [0,1]},
		{ "name": "h1-4", "type": "continuous", "range": [0,1]},
		{ "name": "code2", "type": "series", "length": 4, "depth": 8, "mutationRate": 0.5},
		{ "name": "h2-1", "type": "continuous", "range": [0,1]},
		{ "name": "h2-2", "type": "continuous", "range": [0,1]},
		{ "name": "h2-3", "type": "continuous", "range": [0,1]},
		{ "name": "h2-4", "type": "continuous", "range": [0,1]},
		{ "name": "code3", "type": "series", "length": 4, "depth": 4, "mutationRate": 0.5}
		],
	"outputsDef": [
		{ "name": "displacement", "type": "objective", "goal": "min"},
		{ "name": "material", "type": "objective", "goal": "min"}
		],
	"algo": "GA",
	"algoOptions": {
		"numGenerations": 100,
		"numPopulation": 100,
		"mutationRate": 0.05,
		"saveElites": 5
		},
	"jobOptions": {
		"screenshots": True
		}
	}

job.createInputFile(jobDescription)
# job.run(jobDescription)