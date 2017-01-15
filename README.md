# Discover + Explore
### A flexible[1], modular[2], super light-weight[3] framework for generative design and design space exploration.

1. The framework is designed to be extensible to many different search algorithms, visualization strategies, and other features. Currently only random search and a basic multi-objective genetic algorithm (MOGA) are implemented but more can easily be added following the the structure outlined in this documentation.
2. Various functionalities are broken up into separate script files whenever possible to facilitate learning of all the components that go into modern stochastic metaheuristic algorithms.
3. All code is written with an emphasis on simplicity and readability. The goal is not to develop the fastest or best performing algorithms or code, but to present the functionalities in a way that facilitates learning and accessibility to students and designers with only basic familiarity with coding and programming languages.

## Overview

This project consists of two parts:

1. *Discover* - A modular library for multi-objective optimization written in Python
2. *Explore* - An interface for exploring the optimization process written in JavaScript.

![diagram](docs/diagram.png)

Although *Discover* can be used as a general optimization tool, it is specifically devised for physical design problems, and is thus designed to run alongside a parametric CAD platform such as Rhino/Grasshopper. The Python library communicates with the CAD model using input and output text files that it writes to the local directory. This repository includes example files for Rhino/Grasshopper, but any CAD platform can be used as long as it can write and react to changes in the local text files.

With the CAD model open, an optimization job is started by executing a Python script that launches the job handler and passes to it all the relevant information about the job, including the inputs used by the model, the objectives of the optimization, and any relevant options. When a job is started a subfolder is automatically created to store all the information of that job, including a dataset of all designs explored and optionally a folder of screenshots for each design.

Each job folder also contains an "index.html" file, which is used to launch the *Explore* interface. The file can be directly opened in the Firefox browser (by right-clicking and selecting Open with Firefox), or viewed in any browser using a local server. To make this easier, each job folder also contains a Bash script called `explorer.sh` which will automatically start a local server using Python, and launch *Explorer* in your default browser. If you do not have Bash installed, you can install [git](https://git-scm.com/downloads) which comes with a version of Bash.

## Getting started

To start using *Discover*, all you need is a local copy of this repository. If you are familiar with GitHub, you can fork this repository and clone it to a local folder of your choice. If you don't want to use Github you can simply download the repository by clicking on the green "Clone or download" button above and clicking on "Download ZIP". Then unzip the files to a local folder of your choice.

The repository includes several example files which you can use to test Discover, or modify for your own projects. Each project must have as a minimum a `.gh` Grasshopper file which describes the parametric model, and a `.py` Python script which describes and runs the optimization job. In order for *Discover* to work, both of these files must stay in the main repository folder. The repository includes two template files, `template.gh` and `run-template.py` which you can use as a starting point for your own projects. 

## Tutorial 1 - setting up a job

Start by creating a new Rhino project. Then type 'Grasshopper' to launch the Grasshopper window and load in the `template.gh` file. 

[tutorial1-1](docs/tutorial1-1.png)



## Input types



## Output types

## GA options

## License

This software is distributed under the GNU/GPL license. It can be used freely for non-commercial purposes, and may be redistributed as long as attribution is provided back to the original author and any derivative work is given the same license. Please see the [LICENSE](https://github.com/danilnagy/discover/blob/master/LICENSE) document for more information.
