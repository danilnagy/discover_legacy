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
		"numGenerations": 5,
		"numPopulation": 5,
		"mutationRate": 0.05,
		"saveElites": 0,
		"DOE": "random",
		# "DOE": ["_job name_", -1],
		},
	"jobOptions": {
		"screenshots": True
		}
	}

job.createInputFile(jobDescription)
# job.run(jobDescription)