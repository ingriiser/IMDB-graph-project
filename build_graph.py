import csv


def build_graph():
    """Builds a graph with an adjacency list representation

    Returns:
        tuple: graph and supporting dictionaries
    """
    actors_tsv = open("database/actors.tsv", encoding="utf8")
    actors = csv.reader(actors_tsv, delimiter="\t")
    movies_tsv = open("database/movies.tsv", encoding="utf8")
    movies = csv.reader(movies_tsv, delimiter="\t")

    # dict of movies
    movies_dict = {}
    for row in movies:
        key = row[0]
        value = row[1:]
        movies_dict[key] = value

    # dict of all actors appearing in a movie
    actors_per_movie = {}

    # dict of all movies an actor has played in
    movies_per_actor = {}

    for row in actors:
        key = tuple(row[:2])
        value = []
        for id in row[2:]:
            # checks if tt-id is in the database
            if id in movies_dict:
                value.append(id)
                if id in actors_per_movie:
                    actors_per_movie[id].append(key)
                else:
                    actors_per_movie[id] = [key]
        movies_per_actor[key] = value

    # constructing the adjacency list graph as a dictionary
    graph = {}

    # using movies_per_actor and actors_per_movie to find all edges
    for key, value in movies_per_actor.items():
        # list of edges
        edges = []
        for movie in value:
            co_actors = actors_per_movie[movie]
            for co_actor in co_actors:
                # no edges between the same node
                if co_actor != key:
                    edges.append((co_actor, movie))
        graph[key] = edges

    return graph, actors_per_movie, movies_per_actor, movies_dict


def size_graph(graph):
    """ Finding the size of the graph

    Returns:
        tuple: number of nodes and number of edges
    """
    # finner antall noder
    no_nodes = len(graph)
    print(f'Nodes: {no_nodes}')

    # finner antall kanter
    no_edges = 0
    for val in graph.values():
        no_edges += len(val)
    no_edges = no_edges//2
    print(f'Edges: {int(no_edges)}\n')

    return no_nodes, no_edges


if __name__ == "__main__":
    # example usage of the graph
    graph, actors_per_movie, movies_per_actor, movies_dict = build_graph()

    size_graph(graph)

    print(graph[('nm0006563', 'Iggy Pop')][:2])

    print(actors_per_movie['tt0102494'][:2])

    print(movies_per_actor[('nm0880521', 'Liv Ullmann')][:2])

    print(movies_dict['tt0109913'])

    """
    Nodes: 108811
    Edges: 4775477

    [(('nm0393222', 'James Hong'), 'tt0114614'), (('nm0367496', 'Donald Patrick Harvey'), 'tt0114614')]
    [('nm0367696', 'Rodney Harvey'), ('nm0873773', 'Tom Troupe')]
    ['tt0063759', 'tt0087560']
    ['Go Fish', '5.6', '2085']
    """
