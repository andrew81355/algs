import math
import heapq
import time
import tracemalloc
nodes = {"Hauptbahnhof": (49.4036, 8.6755),
        "Bismarckplatz": (49.4108, 8.6947),
        "Altstadt": (49.4123, 8.7090),
        "Schloss": (49.4106, 8.7153),
        "Neuenheim_Markt": (49.4176, 8.7002),
        "Philosophenweg": (49.4187, 8.6965),
        "Handschuhsheim": (49.4300, 8.6900),
        "Wieblingen": (49.4170, 8.6350),
        "Kirchheim": (49.3888, 8.6712),
        "Rohrbach": (49.3935, 8.6905),
        "Universitaetsklinikum": (49.4196, 8.6725),
        "St_Josef": (49.4028, 8.6847),
        "ATOS": (49.4077, 8.6888),
        "Salem": (49.4198, 8.6906),
        }
graph = {"Hauptbahnhof": {
        "Bismarckplatz": 2.1,
        "St_Josef": 1.0,
        "Kirchheim": 2.2,
        "Wieblingen": 3.4,
        "ATOS": 1.5,
},
        "Bismarckplatz": {
        "Hauptbahnhof": 2.1,
        "Altstadt": 1.2,
        "Neuenheim_Markt": 1.1,
        "ATOS": 0.8,
        "St_Josef": 1.3,
    
},
        "Altstadt": {
        "Bismarckplatz": 1.2,
        "Schloss": 1.4,
        "ATOS": 1.4,
},
        "Schloss": {
        "Altstadt": 1.4,
},
        "Neuenheim_Markt": {
        "Bismarckplatz": 1.1,
        "Philosophenweg": 0.9,
        "Salem": 1.1,
        "Universitaetsklinikum": 2.0,
        "Handschuhsheim": 1.8,
},
        "Philosophenweg": {
        "Neuenheim_Markt": 0.9,
        "Salem": 1.0,
},
        "Handschuhsheim": {
        "Neuenheim_Markt": 1.8,
        "Salem": 1.6,
        "Universitaetsklinikum": 2.2,
},
        "Wieblingen": {
        "Hauptbahnhof": 3.4,
        "Universitaetsklinikum": 3.0,
},
        "Kirchheim": {
        "Hauptbahnhof": 2.2,
        "Rohrbach": 2.1,
        "St_Josef": 2.5,
},
        "Rohrbach": {
        "Kirchheim": 2.1,
        "ATOS": 2.6,
        "St_Josef": 2.2,
},
        "Universitaetsklinikum": {
        "Wieblingen": 3.0,
        "Neuenheim_Markt": 2.0,
        "Handschuhsheim": 2.2,
        "Salem": 1.6,
},
        "St_Josef": {
        "Hauptbahnhof": 1.0,
        "Bismarckplatz": 1.3,
        "Kirchheim": 2.5,
        "Rohrbach": 2.2,
        "ATOS": 1.2,
},
        "ATOS": {
        "Hauptbahnhof": 1.5,
        "Bismarckplatz": 0.8,
        "Altstadt": 1.4,
        "Rohrbach": 2.6,
        "St_Josef": 1.2,
},
        "Salem": {
        "Neuenheim_Markt": 1.1,
        "Philosophenweg": 1.0,
        "Handschuhsheim": 1.6,
        "Universitaetsklinikum": 1.6,
    },
}
hospitals = {"Universitaetsklinikum", "St_Josef", "ATOS", "Salem"}
# end is the end node, prev is the dictionary with nodes and their parents
# we start from the end node and go to their parents until we get the start node
# we get the way in reversed order and we reverse it
def get_way(prev, end):
    way=[]
    curr = end
    while curr is not None:
        way.append(curr)
        curr = prev.get(curr)
    way.reverse()
    return way
# simple formula for calculating distance between 2 points on earth
def distance(a, b):
    lat1, lon1 = nodes[a]
    lat2, lon2 = nodes[b]
    dx = (lat1 - lat2) * 111
    dy = (lon1 - lon2) * 111 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot(dx, dy)
def dijkstra(start):
    # priority queue to get the node with the lowest dist
    priority_queue = [(0, start)]
    dist= {} # dict with best distance to each node
    for node in nodes:
        dist[node] = math.inf
    dist[start] = 0
    prev = {start: None} # dict with way to each node
    visited = set()
    visited_number = 0
    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)
        if current_node in visited: #if node is visited just skip
            continue
        visited.add(current_node)
        visited_number = visited_number + 1
        if current_node in hospitals and current_node != start: #if its hospital we found way because dijkstra saves the best way to each node
            way = get_way(prev, current_node)
            return current_dist, way, visited_number
        for neighbor, weight in graph[current_node].items():
            new_distance = current_dist + weight
            if new_distance < dist[neighbor]: #if better way to neighbor found update best distance and way to neighbor
                dist[neighbor] = new_distance
                prev[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))
    return math.inf, [], visited_number
def a_star(start):
    priority_queue = [(0, 0, start)] #(f, g, node) where g is distance from start to node and h is estimate distance from node to near hospital and f is g + h
    dist = {}
    for node in nodes:
        dist[node] = math.inf
    prev = {start: None}
    visited = set()
    visited_number = 0
    dist[start] = 0
    while priority_queue:
        current_f, current_g, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue
        visited.add(current_node)
        visited_number = visited_number + 1
        if current_node in hospitals and current_node != start:
            way = get_way(prev, current_node)
            return current_g, way, visited_number
        for neighbor, weight in graph[current_node].items():
            new_g = current_g + weight
            if new_g < dist[neighbor]:
                dist[neighbor] = new_g
                prev[neighbor] = current_node
                min_dist=float('inf')
                for hospital in hospitals:
                    h = distance(neighbor, hospital)
                    if h < min_dist:
                        min_dist = h
                heuristic = min_dist #heuristic is distance to nearest hospital we have
                new_f = new_g + heuristic
                heapq.heappush(priority_queue, (new_f, new_g, neighbor))
    return math.inf, [], visited_number
def measure_alg(function, start, repeats=3000):
    tracemalloc.start()
    start_time = time.perf_counter()
    for i in range(repeats):
        result = function(start)

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    average_time=(end_time - start_time) *1000 / repeats
    peak_memory=peak / 1024
    return result, average_time, peak_memory
scenarios = [
    "Hauptbahnhof",
    "Schloss",
    "Wieblingen",
    "Kirchheim",
    "Handschuhsheim",
    "Philosophenweg",
]
print("Emergency routing to nearest hospital in Heidelberg \n")
for start in scenarios:
    d_result, d_time, d_memory = measure_alg(dijkstra, start)
    a_result, a_time, a_memory = measure_alg(a_star, start)
    d_dist, d_way, d_visited = d_result
    a_dist, a_way, a_visited = a_result
    print(f"Start node: {start}")
    print("Dijkstra's algorithm:")
    print(f"  distance: {d_dist:.1f} km")
    print(f"  way: {' -> '.join(d_way)}")
    print(f"  visited nodes: {d_visited}")
    print(f"  average time: {d_time:.5f} ms")
    print(f"  peak memory: {d_memory:.2f} KB")
    print("A* algorithm:")
    print(f"  distance: {a_dist:.1f} km")
    print(f"  way: {' -> '.join(a_way)}")
    print(f"  visited nodes: {a_visited}")
    print(f"  average time: {a_time:.5f} ms")
    print(f"  peak memory: {a_memory:.2f} KB")