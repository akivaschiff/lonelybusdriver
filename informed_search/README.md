####################################################################################
This folder contains the approximation algorithm + informed_search
For problems contant nir.moshe.nm@gmail.com
####################################################################################

Open a command prompt in the current folder

See run options by typing:
python clustering_cool_solution.py --help

Examples:
##########################################

To run a simulation on Mandl's graph with 4 busses and with the "HUB" algorithm type:

python clustering_cool_solution.py --map maps\mundel.map --algo=hub

To run a simulation on complete graph (mesh)) with 3 busses and with the "greedy" algorithm type:

python clustering_cool_solution.py --map maps\mesh_11_3 --algo=greedy

Output:
##########################################

The program output is as follows:
1) The scores and routes of the chosen solution are printed to the screen
2) The map of the chosen route set is displayed
3) The calculation time