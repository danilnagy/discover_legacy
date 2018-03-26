from src import job

jobDescription = {
	"jobName": "hill",
	"inputsDef": [
		{ "name": "x", "type": "continuous", "range": [0,10]},
		{ "name": "y", "type": "continuous", "range": [0,10]},
		],
	"outputsDef": [
		{ "name": "height", "type": "objective", "goal": "max"},
		],
	"algo": "GA",
	"algoOptions": {
		"numGenerations": 15,
		"numPopulation": 5,
		"mutationRate": 0.25,
		"saveElites": 1,
		"DOE": "random",
		# "DOE": ["_job name_", -1],
		},
	"jobOptions": {
		"screenshots": True
		}
	}

job.createInputFile(jobDescription)
# job.run(jobDescription)