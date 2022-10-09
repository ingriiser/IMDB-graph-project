from build_graph import build_graph
from collections import defaultdict, Counter
from heapq import heappush, heappop


def components(graph):
    """Finding and printing the number of components in a graph.

    Args:
        graph (dictionary): IMDb graph

    Returns:
        dictionary: dictionary with component indexes of all nodes
    """

    visited = defaultdict(lambda: False)
    heap = list(graph.keys())  # all nodes
    index = 0
    while heap:
        actor = heappop(heap)
        if visited[actor] is False:
            # BFS to find all nodes in the component actor belongs to
            visited[actor] = index
            sub_heap = [actor]
            while sub_heap:
                actor = heappop(sub_heap)
                for co_actor, _ in graph[actor]:
                    if visited[co_actor] is False:
                        visited[co_actor] = index
                        heappush(sub_heap, co_actor)
            index += 1

    no_each_comp = Counter(visited.values())
    no_comp_size = Counter(no_each_comp.values())
    sorted_items = sorted(no_comp_size.items(),
                          key=lambda x: (x[1], -x[0]), reverse=False)
    for key, val in sorted_items:

        if val == 1:
            print(f'There is {val} component of size {key}.')
        else:
            print(f'There are {val} components of size {key}.')
    print('\n')
    return visited


if __name__ == "__main__":
    # example use
    graph, _, _, _ = build_graph()

    visited = components(graph)

    """There is 1 component of size 103175.
    There is 1 component of size 19.
    There is 1 component of size 10.
    There is 1 component of size 8.
    There are 3 components of size 9.
    There are 5 components of size 7.
    There are 8 components of size 6.
    There are 14 components of size 5.
    There are 40 components of size 4.
    There are 112 components of size 3.
    There are 297 components of size 2.
    There are 4329 components of size 1.
    """
