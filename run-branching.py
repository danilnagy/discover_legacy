from src import job

jobDescription = {
	"jobName": "branching",
	"inputsDef": [
		{ "name": "code", "type": "series", "length": 25, "depth": 3, "mutationRate": 0.5}
		],
	"outputsDef": [
		{ "name": "width1", "type": "objective", "goal": "max"},
		{ "name": "width2", "type": "objective", "goal": "max"},
		{ "name": "height", "type": "objective", "goal": "max"}
		],
	"algo": "GA",
	"algoOptions": {
		"numGenerations": 25,
		"numPopulation": 25,
		"mutationRate": 0.05,
		"saveElites": 1
		},
	"jobOptions": {
		"screenshots": True
		}
	}

# job.createInputFile(jobDescription)
job.run(jobDescription)