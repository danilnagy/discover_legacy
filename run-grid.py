from src import job

jobDescription = {
	"jobName": "grid",
	"inputsDef": [
		{ "name": "code", "type": "series", "length": 25, "depth": 3, "mutationRate": 0.5}
		],
	"outputsDef": [
		{ "name": "target", "type": "objective", "goal": "min"}
		],
	"algo": "GA",
	"algoOptions": {
		"numGenerations": 5,
		"numPopulation": 5,
		"mutationRate": 0.05,
		"saveElites": 1
		},
	"jobOptions": {
		"screenshots": True
		}
	}

job.createInputFile(jobDescription)
# job.run(jobDescription)