### Swarmulator

Code for training and simulating simple UAV swarms

This repository currently consists of a single .ipynb notebook. In order to run the simulation code, the import, class definition, observe() definition, and onesim() definition cells must first be run. In its current state, drones can remain still, move about randomly, or move to the right. Upon colliding with another drone or an obstacle, the drone 'dies'.

This functionality is replicated with the .py files and 'clean' notebook, which allow you to import class definitions and functions as packages.

The later sections of the notebook implement an A* algorithm, allowing a small number of drones to find the optimal path to the destination, without colliding. This functionality isn't available in the .py files (yet).

Jamie McGregor, 2023
