import logging
import networkx as nx
from shapely.wkt import loads
import joblib
import sys
sys.path.append("/workspace/pyspark-app")

from .ndm_road_segment_utils import *



class RoadNetworkGraph():

    def __init__(self, road_segments, log_step = 250000):
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        LOGGER = logging.getLogger(__name__)
        
        self.graph = nx.DiGraph()
        
        LOGGER.info("Building graph from road segments...")
       
        # Build the graph from the road network data
        for i, row in enumerate(road_segments.itertuples()):
            if i % log_step == 0:
                LOGGER.info("Processing %s (%.1f%%)", i, float(i)/road_segments.shape[0]*100)
            
            self.add_node(row)
            if row.form_of_way in NON_NAVIGABLE_ROADS:
                # Add both direction of edges
                self.add_edge(row, forward=True)
                self.add_edge(row, forward=False)
            else:
                if row.forw_nav == True: # or row.forw_nav == 'nan':
                    self.add_edge(row, forward=True)
                if row.back_nav == True: # or row.forw_nav == 'nan':
                    self.add_edge(row, forward=False)

        LOGGER.info("Complete!")   
        LOGGER.info("Graph stats (n_edges, n_nodes, n_selfloops): %s, %s, %s", self.graph.number_of_edges(), self.graph.number_of_nodes(), nx.number_of_selfloops(self.graph))


    def add_edge(self, row, forward=True):
        if forward:
            n1, n2, fow = row.from_node, row.to_node, row.form_of_way
        else:
            n1, n2, fow = row.to_node, row.from_node, row.form_of_way

        n1 = str(n1)
        n2 = str(n2)
        self.graph.add_edge(n1,n2,fow=fow,fid=row.feature_id,length=row.haversine_meters)    
        self.graph.nodes[n1]['out_fow'] = self.graph.nodes[n1].get('out_fow', []) + [fow]
        self.graph.nodes[n2]['in_fow'] = self.graph.nodes[n2].get('in_fow', []) + [fow]
        self.graph.nodes[n1]['outdegree'] = self.graph.nodes[n1].get('outdegree', 0) + 1
        self.graph.nodes[n2]['indegree'] = self.graph.nodes[n2].get('indegree', 0) + 1
        self.graph.nodes[n1]['out_road_ids'] = self.graph.nodes[n1].get('out_road_ids', []) + [row.feature_id]
        self.graph.nodes[n2]['in_road_ids'] = self.graph.nodes[n2].get('in_road_ids', []) + [row.feature_id]


    def add_node(self, row):
        geometry = loads(row.wkt_geom)
        self.graph.add_node(str(row.from_node), pos=geometry.coords[0])
        self.graph.add_node(str(row.to_node), pos=geometry.coords[-1])
        self.graph.nodes[str(row.from_node)]['potential_ap'] = 0
        self.graph.nodes[str(row.to_node)]['potential_ap'] = 0


    def graph_generator(self):
        for n in self.graph.nodes:
            node = self.graph.nodes[n]
            pos = node['pos']
            try:
                yield (int(n), (pos[0], pos[1], pos[0], pos[1]), int(n))
            except (ValueError) as err:
                print(err)

    def save_graph(self, location):
        joblib.dump(self.graph, location)


    # Parameter is a list that identifies segments allowed
    def get_graph_copy_subset_fows(self, fows_allowed):
        g = self.graph.copy()
        non_permissible_edges = (k for (k,v) in nx.get_edge_attributes(g, 'fow').items() if v not in fows_allowed)
        g.remove_edges_from(non_permissible_edges)
        return g
