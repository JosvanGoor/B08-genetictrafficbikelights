# B08-genetictrafficbikelights

## Installation
We are using the SUMO platform, installation instructions for SUMO can be found at https://sumo.dlr.de/docs/Installing.html

having SUMO installed and the SUMO_HOME environment variable set correct is required to run the scripts. It is also required to have python3 installed together with the numpy package.


## Running the beta
The beta currently only has a fitness function part for the genetic algorithm, which is still a work in progress. To run the example just do
```
python SUMOsim.py
```
n.b. this assumes that `python` refers to the python 3 installation, else replace `python` with `python3` in the previous command.