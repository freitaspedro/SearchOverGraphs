# Development of a Search Algorithm for Specific Vertices in Networks

In this project we use the homophily - inherent in many real networks - to propose a mathematical model that determines the probability of an unexplored vertex to have the feature. This model uses the features of the neighbor vertices already explored and global parameters of the network. The probabilities assigned by the model are used to guide an informed search, which at each step makes a greedy choice. 

## Getting Started

The Python modules and the pre-processed datasets ('\snap' and '\uci') must be downloaded and maintained in the same directory in your local machine.

```
Optional: Download [Gplus](http://snap.stanford.edu/data/gplus.tar.gz), [Facebook](http://snap.stanford.edu/data/facebook.tar.gz), [Twitter](http://snap.stanford.edu/data/twitter.tar.gz), [Polblogs](http://networkdata.ics.uci.edu/data/polblogs/polblogs.gml) and [Polbooks](http://networkdata.ics.uci.edu/data/polbooks/polbooks.gml) datasets. 

### Prerequisites

UNIX machine with Python 2.7 and the module [grap-tool](https://graph-tool.skewed.de).

## Running

You must run first the module 'pre.py' and after the module 'main.py'.

```
Attention! You can only run 'pre.py' if you have downloaded the optional datasets in #Getting Started. But you can skip this module and run directly the module 'main.py' using the pre-processed datasets.

You can run 'pre.py' uncommenting any line in the main and executing this file in your terminal, p.e: 

```
main("snap/facebook/1912", 481, False)

>> python pre.py

The first parameter in the line above is the path to the files of egonet 1912 in Facebook dataset. The second is the number of features in this egonet. The third say if the egonet is directed or not (this parameter must be always 'False').

At the end of the execution of this module will be created 5 files:
- 1912.png (Draw of the egonet)
- 1912.out_degrees.txt 
- 1912.in_degrees.txt
- 1912.feat.csv	
- 1912.edges.csv
  
The last two files are required for run 'main.py'.

You can run 'main.py' uncommenting any line in the main and executing this file in your terminal, p.e: 

```
main("snap/facebook/1912", False, "119", 20, 20, 16, 20)

>> python main.py 

The first parameter in the line above is the path to the files (1912.feat.csv and 1912.edges.csv) of egonet 1912. The second say if the egonet is directed or not (this parameter must be always 'False'). The third is the id of the feature that you want to search. The fourth parameter is the initial budget for the search. The fifth is the size of the increment in the current budget. The sixth say how many times this increment will occur. The last parameter is the number of runs of the simulation.

At the end of the execution of this module will be created 7 files:
- starts.txt (Randomly chosen vertices)
- 1912_f119_BFS.search.csv
- 1912_f119_DFS.search.csv
- 1912_f119_HEU1.search.csv
- 1912_f119_HEU2.search.csv
- 1912_f119_HEU3.search.csv
- 1912_f119_MOD.search.csv

The last six with information about the time, the positives and the exlpored+discoverd vertices in each type of search (BFS, DFS, HEU1, HEU2, HEU3 and MOD*).

## Authors

* **Pedro Freitas** - pfreitas@land.ufrj.br
* **Vitor Cardoso** 
* **Giulio Iacobelli** 
* **Daniel Figueiredo** 

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](https://github.com/freitaspedro/SearchOverGraphs/blob/wperfor/LICENSE) file for details
