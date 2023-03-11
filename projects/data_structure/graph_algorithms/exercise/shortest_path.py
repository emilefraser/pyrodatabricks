# Shortest Path - Dijkstra's Algorithm
from graph_algorithms.exercise.bfs_dfs_search import GraphNode


def update_distances(graph, current, distance, parent=None):
    """Update the distances of the current node's neighbors"""
    neighbors = graph.data[current]
    weights = graph.weight[current]
    for i, node in enumerate(neighbors):
        weight = weights[i]
        if distance[current] + weight < distance[node]:
            distance[node] = distance[current] + weight
            if parent:
                parent[node] = current


def pick_next_node(distance, visited):
    """Pick the next univisited node at the smallest distance"""
    min_distance = float('inf')
    min_node = None
    for node in range(len(distance)):
        if not visited[node] and distance[node] < min_distance:
            min_node = node
            min_distance = distance[node]
    return min_node


def shortest_path(graph, source, dest):
    """Find the length of the shortest path between source and destination"""
    visited = [False] * len(graph.data)
    distance = [float('inf')] * len(graph.data)
    parent = [None] * len(graph.data)
    queue = []
    idx = 0

    queue.append(source)
    distance[source] = 0
    visited[source] = True

    while idx < len(queue) and not visited[dest]:
        current = queue[idx]
        update_distances(graph, current, distance, parent)

        next_node = pick_next_node(distance, visited)
        if next_node is not None:
            visited[next_node] = True
            queue.append(next_node)
        idx += 1

    return distance[dest], distance, parent


if __name__ == "__main__":
    # Finding Shortest Path - Dijkstra's Algorithm
    print("Finding Shortest Path - Dijkstra's Algorithm")
    num_nodes7 = 6
    edges7 = [(0, 1, 4), (0, 2, 2), (1, 2, 5), (1, 3, 10), (2, 4, 3), (4, 3, 4), (3, 5, 11)]
    g7 = GraphNode(num_nodes7, edges7, directed=True)
    values = shortest_path(g7, 0, 5)
    print(f"\nShortest path, {values}")
