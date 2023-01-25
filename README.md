### Swarmulator

Code for training and simulating simple UAV swarms

This repository currently consists of a single .ipynb notebook. In order to run the simulation code, the import, class definition, observe() definition, and onesim() definition cells must first be run. In its current state, drones can remain still, move about randomly, or move to the right. Upon colliding with another drone or an obstacle, the drone 'dies'.

In future, I intend to implement some learning algorithm, so that drones can navigate to the goal and avoid collisions. Once the code is working to it's full extent, the notebook may also be split into .py files so that this can be run from the command line.

* Jamie McGregor, 2023 *
