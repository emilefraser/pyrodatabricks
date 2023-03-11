
class Graph:
    def __init__(self, num_nodes, edges):
        self.data = [[] for _ in range(num_nodes)]
        for v1, v2 in edges:
            self.data[v1].append(v2)
            self.data[v2].append(v1)

    def __repr__(self):
        return "\n".join(["{} : {}".format(i, neighbors) for (i, neighbors) in enumerate(self.data)])

    def __str__(self):
        return repr(self)


def bfs(graph, source):
    visited = [False] * len(graph.data)
    queue = []

    visited[source] = True
    queue.append(source)
    i = 0

    while i < len(queue):
        for v in graph.data[queue[i]]:
            if not visited[v]:
                visited[v] = True
                queue.append(v)
        i += 1

    return queue


def dfs(graph, source):
    visited = [False] * len(graph.data)
    stack = [source]
    result = []

    while len(stack) > 0:
        current = stack.pop()
        if not visited[current]:
            result.append(current)
            visited[current] = True
            for v in graph.data[current]:
                stack.append(v)

    return result


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


# Directed and Weighted Graph
class GraphNode:
    def __init__(self, num_nodes, edges, directed=False):
        self.data = [[] for _ in range(num_nodes)]
        self.weight = [[] for _ in range(num_nodes)]

        self.directed = directed
        self.weighted = len(edges) > 0 and len(edges[0]) == 3

        for e in edges:
            self.data[e[0]].append(e[1])
            if self.weighted:
                self.weight[e[0]].append(e[2])

            if not directed:
                self.data[e[1]].append(e[0])
                if self.weighted:
                    self.data[e[1]].append(e[2])

    def __repr__(self):
        result = ""
        for i in range(len(self.data)):
            pairs = list(zip(self.data[i], self.weight[i]))
            result += "{}: {}\n".format(i, pairs)
        return result

    def __str__(self):
        return repr(self)


if __name__ == "__main__":
    num_nodes7 = 6
    edges7 = [(0, 1, 4), (0, 2, 2), (1, 2, 5), (1, 3, 10), (2, 4, 3), (4, 3, 4), (3, 5, 11)]
    print(f"\nnumber_node7 value, {num_nodes7}, length of edges, {len(edges7)}")

    print("Input values, \n")
    num_nodes1 = 5
    edges1 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 4), (1, 3)]
    print(f"number node1 value, {num_nodes1}, length of edges1, {len(edges1)}\n")

    num_nodes3 = 9
    edges3 = [(0, 1), (0, 3), (1, 2), (2, 3), (4, 5), (4, 6), (5, 6), (7, 8)]
    print(f"number nodes3 value, {num_nodes3}, length of edges3, {len(edges3)}\n")

    num_nodes5 = 9
    edges5 = [(0, 1, 3), (0, 3, 2), (0, 8, 4), (1, 7, 4), (2, 7, 2), (2, 3, 6),
              (2, 5, 1), (3, 4, 1), (4, 8, 8), (5, 6, 8)]
    print(f"number nodes5 value, {num_nodes5}, length of edges3, {len(edges5)}\n")

    # Directed graph
    num_nodes6 = 5
    edges6 = [(0, 1), (1, 2), (2, 3), (2, 4), (4, 2), (3, 0)]
    print(f"number nodes6 value, {num_nodes6}, length of edges3, {len(edges6)}\n")

    num_nodes7 = 6
    edges7 = [(0, 1, 4), (0, 2, 2), (1, 2, 5), (1, 3, 10), (2, 4, 3), (4, 3, 4), (3, 5, 11)]
    print(f"number nodes7 value, {num_nodes7}, length of edges3, {len(edges7)}\n")

    # Adjacency List
    print("\nAdjacency list")
    g1 = Graph(num_nodes1, edges1)
    print(f"\ng1 value, {g1}")
    print("\nBFS ,")
    result = bfs(g1, 3)
    print(f"\nresult of bfs g1, 3, {result}")
    print("\nDFS, ")
    result = dfs(g1, 0)
    print(f"\nDFS result g1, 0, {result}")

    g7 = GraphNode(num_nodes7, edges7, directed=True)
    print(f"\ng7 variable value, {g7}")
    print(f"\ng7 graph weight, {g7.weight}")

    