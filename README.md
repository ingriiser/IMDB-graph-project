# IMDb graph project
Implementations of graph algorithms using IMDb, such as BFS and Dijkstra.

This is is an extended version of an individual project submitted for the course *IN2010: Algorithms and Data Structures* at UiO. 

## Organizing the graph

Each node represents an actor, uniquely identified by a name id, and edges between two nodes represents movies both actors have played in. A movie is uniquely identified by a title id. Each edge is marked with the movie's name and IMDb rating. 

![illustration](https://github.com/ingriiser/IMDB-graph-project/blob/main/figures/my_own_private_idaho.PNG)

The database is organized in two separate .tsv files. In [actors.tsv](https://github.com/ingriiser/IMDB-graph-project/blob/main/database/actors.tsv) each record is an actor with the co-variates *nm-id, Name, tt-id_1, .... ,tt-id_k*. tt-id is the title id of a movie the actor has been in. 

In [movies.tsv](https://github.com/ingriiser/IMDB-graph-project/blob/main/database/movies.tsv) there is a record for each movie with the co-variates *tt-id, Title, Rating, Number of votes*. Rating refers to the IMDb rating of the movie, and Number of votes is the number of votes behind the rating. 

The graph consists of about 100 000 nodes and 5 million edges. Most actors never work together, which results in a dense graph. This makes adjacency list a natural choice for representing the graph, in this case a python dictionary. The construction of the graph can be found found at [build_graph.py](https://github.com/ingriiser/IMDB-graph-project/blob/main/build_graph.py).

The dictionary is organized so that each key is a node, the actor, and each value is a list of all co-actors and the tt-id of the movie they have played in together. The following example with Iggy Pop illustrates the syntax. 

*graph[('nm0006563', 'Iggy Pop')] = [(('nm0000204', 'Natalie Portman'), ..., (('nm0001250', 'Charlotte Gainsbourg'), 'tt0368794')]*

Under the construction of the graph, 3 additional dictionaries are obtained: 
- actors_per_movie lists all the actors that play in a movie. To find all the actors in *My Own Private Idaho* one can do the following: 

  *actors_per_movie['tt0102494'] = [('nm0000203', 'River Phoenix'), ...,  ('nm0001814', 'Gus Van Sant')]*

- movies_per_actor gives us a list of all the movies an actor has played in, which is the information found in [actors.tsv](https://github.com/ingriiser/IMDB-graph-project/blob/main/database/actors.tsv).

  *movies_per_actor[('nm0880521', 'Liv Ullmann')] = ['tt0063759', ...., 'tt1170396']*

- movies_dict gives us the name, rating and votes of each movie, as in [movies.tsv](https://github.com/ingriiser/IMDB-graph-project/blob/main/database/movies.tsv)

  *movies_dict['tt0109913'] = ['Go Fish', '5.6', '2085']*

They are kept for future convenience. 

## 6 degrees of IMDb
The problem at hand is to find the shortest path between two given actors, and this is solved by a BFS algorithm. There might exist several paths of the same length, but by using BFS the search will terminate as soon as  the first path of length *n* is found, after ensuring that there are no paths shorter than *n*. To increase efficiency, the algorithm keeps track of visited nodes, so that the nodes are not visited more than once.

I have yet to find two actors that are further than 6 links apart, and not for lack of trying. Despite choosing the most obscure actors I can think of, and actors from vastly different eras and countries, it always seems to be a short link between them. (As long as they are in the same component. More on this below.) Give it a try yourself using [finding_paths.py](https://github.com/ingriiser/IMDB-graph-project/blob/main/finding_paths.py). 

If one instead want to find the highest rated path between two actors, using Dijkstra is the way forward, where the nodes are visited in accordance of a priority queue. The ratings are used as weights. Because there may be many paths between two actors, the algorithm does not terminate when the first path is found. Instead, it will save the current cost to reach all nodes (as long as they have a lower cost than the current lowest cost of the goal node). 

A future addition might be to find the most popular or most obscure path by using the number of votes as weights instead. 

## Components

Even though most actors never appear in the same movie, it turns out that most actors in the database are connected in a way. Their nodes are a part of the same component in the graph. By a modified BFS algorithm one can find the number of components in a graph. This is done in [components.py](https://github.com/ingriiser/IMDB-graph-project/blob/main/components.py). 

A future update can use the dictionary which maps each node to their component index to systematize the search for long links between actors. If we know that they belong to the same component, then it will be a link between them. 

