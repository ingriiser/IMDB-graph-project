from build_graph import build_graph
from collections import defaultdict, deque
from heapq import heappush, heappop


def find_shortest_path(graph, start, goal):
    """Finding the shortest path between two actors

    Args:
        graph (dictionary): IMDb graph
        start (tuple): first actor on the form (nm-id, name)
        goal (tuple): second actor on the form (nm-id, name)

    Returns:
        list or None: shortest path
    """

    # elements in the path are given as ((nm-id, name), tt-id)
    # empty strings as the movie in the starting and finishing position
    start = (start, ' ')
    goal = (goal, ' ')

    visited = []

    # queue containing paths of different lengths
    queue = [[start]]

    while queue:
        path = queue.pop(0)

        # finding the actor in the last element of the path
        actor = path[-1][0]
        if actor not in visited:
            co_actors = graph[actor]
            for co_actor in co_actors:
                new_path = list(path)
                new_path.append(co_actor)
                queue.append(new_path)
                if co_actor[0] == goal[0]:
                    return new_path
            visited.append(actor)

    # if a path does not exist
    return None


def print_path(path, movies_dict):
    """Printing a path, which is output from find_shortest_path() or find_best_path()

    Args:
        path (list): a path
        movies_dict (dictionary): dictionary of movies
    """
    if path is None:
        print(f'There exists no path.\n')
        return

    start = path.pop(0)
    print(start[0][1])
    for b in path:
        actor = b[0][1]
        movie_id = b[1]
        movie_name, movie_rating, _ = movies_dict[movie_id]
        print(f'===[ {movie_name} ({movie_rating}) ] ===> {actor}')


def find_best_path(graph, movies_dict, start, goal):
    """The highest rated path between two actors 

    Args:
        graph (dictionary): IMDb graph
        movies_dict (dictionary): dictionary on movies
        start (tuple): first actor on the form (nm-id, name)
        goal (tuple): second actor on the form (nm-id, name)

    Returns:
        tuple or None: cost of path, highest rated path
    """

    # elements in the path are given as ((nm-id, name), tt-id)
    # empty strings as the movie in the starting and finishing position
    start = (start, ' ')
    goal = (goal, ' ')
    # priority queue containing paths of different lengths
    Q = [(0, start)]
    D = defaultdict(lambda: float('inf'))
    # tracking the parent nodes leading the shortest path back to start
    parents = {start: None}
    D[start[0]] = 0

    while Q:
        cost, v = heappop(Q)
        if v[0] is not goal:
            for u in graph[v[0]]:
                _, r, _ = movies_dict[u[1]]
                r = float(r)
                c = cost + 10 - r
                # only updates the cost to the node if the cost is lower than
                # the current lowest cost to goal
                if c < D[goal[0]]:
                    # only updates the cost and parent node if this cost
                    # is lower than the current cost
                    if c < D[u[0]]:
                        D[u[0]] = c
                        heappush(Q, (c, u))
                        parents[u] = v
                        if u[0] == goal[0]:
                            current_best = (c, u)

    if D[goal[0]] == 'inf':
        # no path between start and goal
        return None

    else:
        best_cost, path = current_best
        parent = parents[path]
        path = deque([path])
        while parent is not None:
            path.appendleft(parent)
            parent = parents[parent]
        return best_cost, list(path)


if __name__ == "__main__":
    # example use
    graph, actors_per_movie, movies_per_actor, movies_dict = build_graph()

    find_paths = [[('nm4608165', 'Antoine Olivier Pilon'), ('nm0880521', 'Liv Ullmann')],
                  [('nm0002000', 'Leslie Cheung'),
                   ('nm1898448', 'Eyþór Guðjónsson')],
                  [('nm0217950', 'Mireille Delunsch'),
                   ('nm4232273', 'Lindy Larsson')],
                  [('nm3220898', 'Saba Azad'), ('nm1313961', 'Jérôme Colin')]]

    for a in find_paths:
        shortest_path = find_shortest_path(graph, a[0], a[1])
        print('Shortest path:')
        print_path(shortest_path, movies_dict)
        print('\n')

        score, best_path = find_best_path(graph, movies_dict, a[0], a[1])
        print('Best path:')
        print_path(best_path, movies_dict)
        print(f'Total weight: {score:.1f}')
        print('\n')

    """
    Shortest path:
    Antoine Olivier Pilon
    ===[ Laurence Anyways (7.7) ] ===> Nathalie Baye
    ===[ Tomorrow's Another Day (6.1) ] ===> Hubert Saint-Macary
    ===[ Dangerous Moves (6.8) ] ===> Liv Ullmann


    Best path:
    Antoine Olivier Pilon
    ===[ Laurence Anyways (7.7) ] ===> Nathalie Baye
    ===[ Catch Me If You Can (8.1) ] ===> Sean Connery
    ===[ A Bridge Too Far (7.4) ] ===> Liv Ullmann
    Total weight: 6.8


    Shortest path:
    Leslie Cheung
    ===[ The Bride with White Hair 2 (5.9) ] ===> Eddy Ko
    ===[ Lethal Weapon 4 (6.6) ] ===> Rick Hoffman
    ===[ Hostel Dissected (7.0) ] ===> Eyþór Guðjónsson


    Best path:
    Leslie Cheung
    ===[ A Better Tomorrow (7.5) ] ===> Tsui Hark
    ===[ The Story of Film: An Odyssey (8.5) ] ===> Steven Spielberg
    ===[ The Shark Is Still Working (7.7) ] ===> Eli Roth
    ===[ Hostel Dissected (7.0) ] ===> Eyþór Guðjónsson
    Total weight: 9.3


    Shortest path:
    Mireille Delunsch
    ===[ Meeting with an Angel (5.5) ] ===> Claude Winter
    ===[ Le Bon Plaisir (6.2) ] ===> Daniel Mesguich
    ===[ Den döende dandyn (5.4) ] ===> Reine Brynolfsson
    ===[ House of Angels - Third Time Lucky (4.7) ] ===> Lindy Larsson


    Best path:
    Mireille Delunsch
    ===[ Meeting with an Angel (5.5) ] ===> Sergi López
    ===[ The Man Who Killed Don Quixote (6.4) ] ===> Stellan Skarsgård
    ===[ The Ox (7.1) ] ===> Rikard Wolff
    ===[ House of Angels - Third Time Lucky (4.7) ] ===> Lindy Larsson
    Total weight: 16.3


    Shortest path:
    Saba Azad
    ===[ Mujhse Fraaandship Karoge (6.9) ] ===> Tara D'Souza
    ===[ Mere Brother Ki Dulhan (5.8) ] ===> John Abraham
    ===[ Baabul (5.4) ] ===> Amitabh Bachchan
    ===[ The Story of Film: An Odyssey (8.5) ] ===> Wim Wenders
    ===[ Hitler in Hollywood (5.8) ] ===> Jérôme Colin


    Best path:
    Saba Azad
    ===[ Mujhse Fraaandship Karoge (6.9) ] ===> Saqib Saleem
    ===[ Hawaa Hawaai (7.4) ] ===> Makarand Deshpande
    ===[ Sarfarosh (8.1) ] ===> Naseeruddin Shah
    ===[ Valley of Flowers (7.0) ] ===> Mylène Jampanoï
    ===[ Hitler in Hollywood (5.8) ] ===> Jérôme Colin
    Total weight: 14.8
    """
