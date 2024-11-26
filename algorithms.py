import heapq
import time
import random

def dijkstra(graph, start, goal, _):
    pq = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited_count = 0
    while pq:
        curr_distance, curr_node = heapq.heappop(pq)
        visited_count += 1
        if curr_node == goal:
            return curr_distance, visited_count
        for neighbor, weight in graph[curr_node].items():
            distance = curr_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    return distances[goal], visited_count

def gbfs(graph, start, goal, heuristic):
    pq = [(heuristic(start, goal), 0, start)]
    visited = set()
    visited_count = 0
    while pq:
        _, curr_dist, curr_node = heapq.heappop(pq)
        visited_count += 1
        if curr_node == goal:
            return curr_dist, visited_count
        if curr_node in visited:
            continue
        visited.add(curr_node)
        for neighbor, weight in graph.get(curr_node, {}).items():
            if neighbor not in visited:
                heapq.heappush(pq, (heuristic(neighbor, goal), curr_dist + weight, neighbor))
    return None, visited_count

def a_star(graph, start, goal, heuristic):
    pq = [(0 + heuristic(start, goal), 0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited_count = 0
    while pq:
        _, g_score, curr_node = heapq.heappop(pq)
        visited_count += 1
        if curr_node == goal:
            return g_score, visited_count
        for neighbor, weight in graph[curr_node].items():
            tentative_g_score = g_score + weight
            if tentative_g_score < distances[neighbor]:
                distances[neighbor] = tentative_g_score
                heapq.heappush(pq, (tentative_g_score + heuristic(neighbor, goal), tentative_g_score, neighbor))
    return distances[goal], visited_count



def create_grid_graph(size=100, barrier_fraction=0.1):
    grid_graph = {}
    barriers = set()
    total_nodes = size * size
    barrier_count = int(total_nodes * barrier_fraction)
    
    while len(barriers) < barrier_count:
        x = int(random.gauss(size // 2, size // 7))
        y = int(random.gauss(size // 2, size // 7))
        
        # Ensure x and y stay within grid bounds
        if 0 < x < size - 1 and 0 < y < size - 1 and (x,y) not in [(20,20),(80,80)]:
            barriers.add((x, y))

    for y in range(size):
        print( ''.join([('B' if (x,y) in barriers else 'S' if (x,y) == (20,20) else 'G' if (x,y) == (80,80) else '.') for x in range(size)]))
    
    for x in range(size):
        for y in range(size):
            if (x, y) in barriers: continue
            neighbors = {}
            if x > 0 and (x - 1, y) not in barriers:  # Up
                neighbors[(x - 1, y)] = 1
            if x < size - 1 and (x + 1, y) not in barriers:  # Down
                neighbors[(x + 1, y)] = 1
            if y > 0 and (x, y - 1) not in barriers:  # Left
                neighbors[(x, y - 1)] = 1
            if y < size - 1 and (x, y + 1) not in barriers:  # Right
                neighbors[(x, y + 1)] = 1
            grid_graph[(x, y)] = neighbors
    return grid_graph, barriers

# Heuristic function
def manhattan_heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

grid_graph, barriers = create_grid_graph(size := 100, barrier_fraction=0.3)

# Example of heuristic usage
start = (20, 20)
goal = (80,80)

for name, algo in [("Dijkstra", dijkstra), ("GBFS", gbfs), ("A*", a_star)]:
    start_time = time.time()
    result, count = algo(grid_graph, start, goal, manhattan_heuristic)
    elapsed_time = time.time() - start_time
    print(f"{name}: Shortest Path = {result}, Visited {count} nodes, Time Taken = {elapsed_time * 1000} ms")
