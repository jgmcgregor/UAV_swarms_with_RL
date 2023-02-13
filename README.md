### Swarmulator

Code for training and simulating simple UAV swarms

The swarmulator.ipynb notebook contains most of the simulation code. In order to run this simulation code, the import, class definition, observe() definition, and onesim() definition cells must first be run. In its current state, drones can remain still, move about randomly, or move to the right. Upon colliding with another drone or an obstacle, the drone 'dies'.

This functionality is replicated with the .py files and 'clean' notebook, which allow you to import class definitions and functions as packages.

The later sections of the notebook implement an A* algorithm, allowing a small number of drones to find the optimal path to the destination, without colliding. This functionality isn't available in the .py files (yet).

I have also begun working on implementing a convolutional neural network, to see if the drone swarms can be trained to follow the path provided by the A* algorithm.

Jamie McGregor, 2023
