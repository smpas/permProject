import pandas as pd
import geopandas as gpd
import numpy as np
import networkit as nk
import shapely
import geopandas as gpd
import shapely
import copy
import pandas as pd
import shapely.wkt
import networkx as nx
import networkit as nk

from scipy import spatial
from shapely.geometry import LineString
from CityGeoTools.data_collecting.get_graphs import get_osmnx_graph, get_public_trasport_graph, get_intermodal_graph

def calculate_distance_matrix(road_network, houses, facilities, crs=32640, type=['walk'], weight='length_meter'):
    network = road_network.edge_subgraph(
        [(u, v, k) for u, v, k, d in road_network.edges(data=True, keys=True)
         if d["type"] in type]
    )

    # find nearest points to objects on road network
    gdf = gpd.GeoDataFrame.from_dict(dict(network.nodes(data=True)), orient='index')
    gdf["geometry"] = gdf.apply(lambda row: shapely.geometry.Point(row.x, row.y), axis=1)
    nodes_gdf = gpd.GeoDataFrame(gdf, geometry=gdf['geometry'], crs=crs)
    from_houses = nodes_gdf['geometry'].sindex.nearest(houses['geometry'], return_distance=True, return_all=False)
    to_facilities = nodes_gdf['geometry'].sindex.nearest(facilities['geometry'], return_distance=True, return_all=False)

    distance_matrix = pd.DataFrame(0, index=to_facilities[0][1], columns=from_houses[0][1])
    splited_matrix = np.array_split(distance_matrix.copy(deep=True), int(len(distance_matrix) / 1000) + 1)

    # conver nx graph to nk graph in oder to speed up the calculation
    nk_idmap = _get_nx2nk_idmap(network)
    net_nk = _convert_nx2nk(network, idmap=nk_idmap, weight=weight)

    # calculate distance matrix
    for i in range(len(splited_matrix)):
        r = nk.distance.SPSP(G=net_nk, sources=splited_matrix[i].index.values).run()
        splited_matrix[i] = splited_matrix[i].apply(lambda x: _get_nk_distances(r, x), axis=1)
        del r

    distance_matrix = pd.concat(splited_matrix)
    distance_matrix.index = list(facilities.iloc[to_facilities[0][0]].index)
    distance_matrix.columns = list(houses.iloc[from_houses[0][0]].index)

    del splited_matrix

    # replace 0 values (caused by road network sparsity) to euclidian distance between two points
    distance_matrix = distance_matrix.progress_apply(lambda x: _calculate_euclidian_distance(x, houses, facilities))
    return distance_matrix


def _calculate_euclidian_distance(loc, houses, facilities):
    s = copy.deepcopy(loc)
    s_0 = s[s == 0]
    if len(s_0) > 0:
        s.loc[s_0.index] = facilities["geometry"][s.index].distance(houses["geometry"][s.name])
        return s
    else:
        return s


"""Functions to convert Networkx graph to Networkit graph"""


def _get_nx2nk_idmap(G_nx):
    idmap = dict((id, u) for (id, u) in zip(G_nx.nodes(), range(G_nx.number_of_nodes())))
    return idmap


def _convert_nx2nk(G_nx, idmap=None, weight=None):
    if not idmap:
        idmap = _get_nx2nk_idmap(G_nx)
    n = max(idmap.values()) + 1
    edges = list(G_nx.edges())

    if weight:
        G_nk = nk.Graph(n, directed=G_nx.is_directed(), weighted=True)
        for u_, v_ in edges:
            u, v = idmap[u_], idmap[v_]
            d = dict(G_nx[u_][v_])
            if len(d) > 1:
                for d_ in d.values():
                    v__ = G_nk.addNodes(2)
                    u__ = v__ - 1
                    w = round(d_[weight], 1) if weight in d_ else 1
                    G_nk.addEdge(u, v, w)
                    G_nk.addEdge(u_, u__, 0)
                    G_nk.addEdge(v_, v__, 0)
            else:
                d_ = list(d.values())[0]
                w = round(d_[weight], 1) if weight in d_ else 1
                G_nk.addEdge(u, v, w)
    else:
        G_nk = nk.Graph(n, directed=G_nx.is_directed())
        for u_, v_ in edges:
            u, v = idmap[u_], idmap[v_]
            G_nk.addEdge(u, v)

    return G_nk


def _get_nk_distances(nk_dists, loc):
    target_nodes = loc.index
    source_node = loc.name
    distances = [nk_dists.getDistance(source_node, node) for node in target_nodes]
    return pd.Series(data=distances, index=target_nodes)


road_network = get_osmnx_graph(1084793, 32640, 'walk')

houses = gpd.read_file("../../data/buildings.geojson")
houses = houses[houses['is_living'] == 1]
houses = houses.to_crs(32640)
houses.set_index('id', inplace=True)

facilities = gpd.read_file("../../data/services/school.geojson")
facilities = facilities.to_crs(32640)
facilities.set_index('osm_id', inplace=True)

print("starting matrix calculation")
matrix = calculate_distance_matrix(road_network, houses, facilities)
print("saving matrix")
matrix.to_csv('provision\distance_matrix.csv', index=False)