from src import job

jobDescription = {
	"jobName": "box",
	"inputsDef": [
		{ "name": "length", "type": "continuous", "range": [0,10]},
		{ "name": "width", "type": "continuous", "range": [0,10]},
		{ "name": "height", "type": "continuous", "range": [0,10]}
		],
	"outputsDef": [
		{ "name": "surface area", "type": "objective", "goal": "min"},
		{ "name": "volume", "type": "objective", "goal": "max"}
		],
	"algo": "GA",
	"algoOptions": {
		"numGenerations": 10,
		"numPopulation": 10,
		"mutationRate": 0.05,
		"saveElites": 2
		},
	"jobOptions": {
		"screenshots": True
		}
	}

# job.createInputFile(jobDescription)
job.run(jobDescription)