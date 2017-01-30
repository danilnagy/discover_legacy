from src import job

jobDescription = {
	"jobName": "salesman",
	"inputsDef": [
		{ "name": "city order", "type": "sequence", "length": 10, "mutationRate": 0.30}
		],
	"outputsDef": [
		{ "name": "distance traveled", "type": "objective", "goal": "min"}
		],
	"algo": "GA",
	"algoOptions": {
		"numGenerations": 5,
		"numPopulation": 5,
		"mutationRate": 0.2,
		"saveElites": 0
		},
	"jobOptions": {
		"screenshots": True
		}
	}

job.createInputFile(jobDescription)
# job.run(jobDescription)