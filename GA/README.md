##########################################
This folder contains the genetic algorithm
For problems contact AkivaSchiff@gmail.com
##########################################

Open a command prompt in the current folder

See run options by typing:
python main.py --help

Examples:
##########################################

To run a simulation on Mandl's graph with 4 busses, type:

python main.py --busses 4 --graph Mandl --max 10 --initial 100 --generations 100

And a few other run examples:

python main.py --busses 6 --graph Mandl --max 8 --min 4 --initial 50 --generations 100
python main.py --busses 6 --graph Mumford0 --max 12 --tf 15 --initial 50 --generations 150

Output:
##########################################

The program output is as follows:
1) The scores and routes of the chosen solution are printed to the screen
2) The map of the chosen route set is displayed
3) In a folder called 'generating' you will find The chosen routeset as a picture, in textual form, and a statistical graph file with stats on best/average solution per generation, illegal offsprings, dominating offsprings, etc... per generation

Map format:
##########################################
Every graph is defined using 3 files as can be seen in the 'maps' folder.
Coords - first line is the number of nodes and all subsequent lines are x,y coordinates
TravelTimes - A symetrical matrix containing travel times between all pairs of nodes
Demand - A symetrical matrix containing number of passengers to travel between all pairs of nodes