import networkx as nx

from CityGeoTools.data_collecting.get_graphs import get_intermodal_graph

# Get graph from OSMNX

# 1084793 - city osm ID for Perm city district
# 32640 - EPSG projection for 40 UTM zone where Perm is located

# Get intermodal graph
intermodal_G = get_intermodal_graph(1084793, 32640)
nx.write_graphml(intermodal_G, "../../data/graph.graphml")