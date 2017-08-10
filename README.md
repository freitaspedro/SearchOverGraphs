# A Search Algorithm for Vertices with Specific Features over Networks

In this work, we use the homophily of the networks to propose a mathematical model that determines the probability of an unexplored vertex to have the feature. This model uses the features of the neighbor vertices already explored and global parameters of the network. The probabilities assigned by the model are used to guide an informed search, which at each step makes a greedy choice. We evaluated the algorithm in four networks looking for different features using variations of the model and comparing with others informed and uninformed search algorithms. The empirical results show that none of considered methods is consistently more efficient than the others.

## Getting Started

The Python modules and the pre-processed datasets must be downloaded and maintained in the same directory in your local machine.

Optional: Download [Gplus](http://snap.stanford.edu/data/gplus.tar.gz), [Facebook](http://snap.stanford.edu/data/facebook.tar.gz), [Twitter](http://snap.stanford.edu/data/twitter.tar.gz), [PolBlogs](http://networkdata.ics.uci.edu/data/polblogs/polblogs.gml), [PolBooks](http://networkdata.ics.uci.edu/data/polbooks/polbooks.gml) and [DBLP](http://dblp.uni-trier.de/xml/) datasets. 

### Prerequisites

UNIX machine with Python 2.7 and the module [graph-tool](https://graph-tool.skewed.de).

## Running

### For Gplus, Facebook, Twitter, PolBlogs and PolBooks datasets

You must run the modules __compact.py__, __pre.py__ and __main.py__, respectively. If you want plot the graphics, use/adapt the modules __plot2.py__ and __plotheu.py__.

The __compact.py__ have 7 principal methods that you need run for each feature in each network (examples are commented in code):

```
'generate_graph()' - generate the graph (.xml.gz) where vertices with value '1' (or True) have the feature passed as param. The other param is the path to the file with the edges and the file with the features in the dataset converted to .csv. So, if you want to run to Facebook, convert the file 'snap/facebook/1912.edges' and 'snap/facebook/1912.feat' to .csv format.
'count_positives()' - count the number and percentage of vertices with the feature.
'calculate_edges()' - calculate the fraction of edges T-T, T-N and N-N: 'pt','pd' and 'pn' respectively. And the conditional probabilities, 'pt_t' and 'pd_t', params of our model. 
'get_starts()' - randomly chooses x vertices to initialize the search. Note: This one is executed once per network. 
'graph_to_list()' - read the graph (.xml.gz) and generate a .txt with the lists of adjacencies. Note: This one is executed once per network.
'graph_values_to_list()' - read the graph (.xml.gz) and generate a .txt with a list of vertex values (True or False).
'get_positive_subgraph()' - read the graph (.xml.gz) and generate a subgraph (.xml.gz) with just the positives vertices to some feature.
```
You can run __compact.py__ uncommenting one or more lines in the __main__ (after "pos wperformance") and executing this file in your terminal, p.e: 

```
generate_graph("snap/facebook/1912", "240")

>> python compact.py 
```


For run the module __pre.py__ you need the graph (.xml.gz) generated in the previous module. This module is not necessary to run the __main4.py__ but running the __pre.py__ you obtain some files with some interesting graph properties, like: 

```
'gcc.xml.gz.props.txt' - num of vertices, num of edges, max_out_degree, global clustering, etc. 
'gcc.xml.gz.out_degrees.txt (gcc.xml.gz.in_degrees.txt)' - a counter of out (in) degrees in the graph. Note: For undirected graphs (our case), the "out-degree" is synonym for degree, and in this case the in-degree of a vertex is always zero.
'gcc.xml.gz.out_last100.txt (gcc.xml.gz.in_last100.txt)' - the 100 vertices (id, name, degree) with the lowest out (in) degree in the graph. 
'gcc.xml.gz.out_top100.txt (gcc.xml.gz.in_top100.txt)' - the 100 vertices (id, name, degree) with the biggest out (in) degree in the graph.
'gcc.xml.gz.out_ccdf (gcc.xml.gz.in_ccdf)' - a graphic with the complementary cumulative distribution function (CCDF) of out (in) degrees.
```

You can run __pre.py__ uncommenting any line in the __main__ and executing this file in your terminal, p.e: 

```
main("snap/facebook/1912/f240/gcc.xml.gz", -1, False)

>> python pre.py 
```


The module __main4.py__ perform the searchs - BFS, DFS, H_1, H_2, H_3 e MODs - by default. You can run __main4.py__ using any commented line in the __main__ in your terminal, p.e: 

```
>> python main4.py "starts_fb" "snap/facebook/1912/neighbours" "snap/facebook/1912/f240/values" 0.0648497148932 0.874238590573 747 20 20 16 20
```  
-__starts_fb__ - the file generate by 'get_starts()' in 'compact.py'.

-__snap/facebook/1912/neighbours__ - the file generate by 'graph_to_list()' in 'compact.py'.

-__snap/facebook/1912/f240/values__ - the file generate by 'graph_values_to_list' in 'compact.py'.

-__0.0648497148932__ - the param of the model, 'pt_t', calculated in 'calculate_edges()' in 'compact.py'.

-__0.874238590573__ - the param of the model, 'pd_t', calculated in 'calculate_edges()' in 'compact.py'.

-__747__ - the number of vertices in the whole graph and not only in the giant connected component (gcc).

-__20__ - initial budget

-__20__ - size of the increase in budget 

-__16__ - number of times the budget is increased

-__20__ - runs


If you want to run the variations of the heuristics it's just uncomment in code. At the end of the execution of this module will be created files (.csv) with the performance (the available budget, the time spent and the mean and standard desviation of positives found) of each search.

The modules __plot2.py__ and __plotheu.py__ can be used to build the graphics with this results in __main4.py__.


### For DBLP dataset

In this case, the modules used are in the dir '\hugo' (except __pre.py__) but the processes are similar. 

The big difference is that you need to build the graph from the xml provided by [DBLP](http://dblp.uni-trier.de/xml/) running the modules __hugo\removehtml.py__ and __hugo\parser.py__. From this graph we extracted a subgraph of 200 thousand vertices and worked with it. This can be done by running first the method __get_random_vertices()__ in __hugo\compact.py__ an then the other methods. 

So, you must run the modules __pre.py__ and __hugo\main2.py__, respectively. If you want plot the graphics, use/adapt the modules __hugo\plot.py__ and __hugo\plotheu.py__.


## Authors

* **Pedro Freitas** - pvpfreitas@gmail.com

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](https://github.com/freitaspedro/SearchOverGraphs/blob/disser/LICENSE) file for details
