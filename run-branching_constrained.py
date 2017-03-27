from src import job

jobDescription = {
	"jobName": "branching_constrained",
	"inputsDef": [
		{ "name": "code", "type": "series", "length": 25, "depth": 3, "mutationRate": 0.5}
		],
	"outputsDef": [
		{ "name": "width1", "type": "objective", "goal": "max"},
		{ "name": "width2", "type": "objective", "goal": "max"},
		{ "name": "height", "type": "objective", "goal": "max"},
		{ "name": "collision", "type": "constraint", "goal": "equals 0.0" }
		],
	"algo": "GA",
	"algoOptions": {
		"numGenerations": 50,
		"numPopulation": 50,
		"mutationRate": 0.05,
		"saveElites": 5
		},
	"jobOptions": {
		"screenshots": True
		}
	}

# job.createInputFile(jobDescription)
job.run(jobDescription)