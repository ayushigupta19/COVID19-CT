from geopy.distance import geodesic
from params import RADIUS
import pandas as pd

class Node:
    def __init__(self, id):
        self.id = id
        self.is_infected = False
        self.locn_data = []
        self.edge_dict = {}

class Graph:
    def __init__(self):
        self.nodes = {}

    def create_edge(self, p1_id, p2_id, time, dist):
        if p2_id in self.nodes[p1_id].edge_dict.keys():
            self.nodes[p1_id].edge_dict[p2_id].append((time, dist))
        else:
            self.nodes[p1_id].edge_dict[p2_id] = [(time, dist)]
        
        if p1_id in self.nodes[p2_id].edge_dict.keys():
            self.nodes[p2_id].edge_dict[p1_id].append((time, dist))
        else:
            self.nodes[p2_id].edge_dict[p1_id] = [(time, dist)]
            

def build_graph(path):
    graph = Graph()
    df = pd.read_csv(path, header=None, names=['id', 'x', 'y', 't_start', 't_end'])
    for idx, entry in df.iterrows():
        if entry['id'] not in graph.nodes.keys():
            graph.nodes[entry['id']] = Node(id=entry['id'])
            
        graph.nodes[entry['id']].locn_data.append(((entry['t_start'], entry['t_end']), (entry['x'], entry['y'])))

        for node in graph.nodes.values():
            if entry['id'] != node.id:
                for interval in node.locn_data:
                    if interval[0][0] <= entry['t_start'] and interval[0][1] >= entry['t_end']:
                        dist = geodesic((entry['y'], entry['x']), (interval[1][1], interval[1][0])).meters
                        if dist <= RADIUS:
                            time = (entry['t_start'], entry['t_end'])
                            graph.create_edge(node.id, entry['id'], time, dist)
                    elif interval[0][0] >= entry['t_start'] and interval[0][1] <= entry['t_end']:
                        dist = geodesic((entry['y'], entry['x']), (interval[1][1], interval[1][0])).meters 
                        if dist <= RADIUS:
                            time = interval[0]
                            graph.create_edge(node.id, entry['id'], time, dist)                       
  
