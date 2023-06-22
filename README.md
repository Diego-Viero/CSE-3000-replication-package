# CSE-3000-replication-package
Replication package of the paper titled "Is PSO a valid option for search-based test case generation in the context of dynamically-typed languages?" published at TU Delft 2023.

The aforementioned paper introduces two Particle Swarm Optimization adaptations for the context of search-based test case generation for dynamically-typed languages. This repository contains all the necessary tools needed to replicate the experiment, including tools to visualize the results.


---
## Configuration
To select the configuration of the experiment and select the related parameters, the [.syntest.json](syntest-javascript-benchmark/.syntest.json) file should be accessed:
- `target-root-directory` specifies the benchmark directory of the files, the available directories can be found [here](syntest-javascript-benchmark/.syntest-projects.json)
- `include` specifies the files for which the algorithm should try to generate tests, the available files can be found [here](syntest-javascript-benchmark/.syntest-projects.json) 
- `preset` specifies the algorithm, valid options are `MOSAPSO`, `DynaMOSAPSO`, `DynaMOSA`, `MOSA`, and `NSGAII`.
- `total-time`: represents the maximum search time of the algorithm.
---
## Running the experiment

In order to run the experiment, two bash scripts are provided [build.sh](build.sh) and [clean-build.sh](clean-build.sh) the first one builds and runs the experiment, while the latter deltes and reinstall all the node_modules, then builds and runs the experiment.
We suggest to always use the first file, unless new changes were pulled from any of the repositories.


---
## Plotting results

To see the coverage over time of the different files tested, run the `extract.py` file insidethe `plot/` directory, followed by the name of the folder containing the results. e.g, "python extract.py base"
