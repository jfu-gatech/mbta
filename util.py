def breadth_first_search(graph, start, target):
    # breath first search that outputs the path taken
    # TODO: expand documentation with parameter details
    visited = []
    queue = []
    queue.append([start])

    if start == target:
        return [start]

    while queue:
        path = queue.pop(0)
        last_node = path[-1]

        if last_node not in visited:
            visited.append(last_node)
            for neighbor in graph[last_node]:
                new_path = path[:]
                new_path.append(neighbor)
                queue.append(new_path)

                if neighbor == target:
                    return new_path

    return []
