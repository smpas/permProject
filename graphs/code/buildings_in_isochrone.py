import geopandas as gpd

buildings_gdf = gpd.read_file("../../data/buildings.geojson")
walk_isochrone = gpd.read_file("../results/walk_isochrone.geojson")
drive_isochrone = gpd.read_file("../results/drive_isochrone.geojson")
transport_isochrone = gpd.read_file("../results/transport_isochrone.geojson")

buildings_in_walk_isochrone = gpd.sjoin(buildings_gdf, walk_isochrone, how="inner", op="intersects")
buildings_in_drive_isochrone = gpd.sjoin(buildings_gdf, drive_isochrone, how="inner", op="intersects")
buildings_in_transport_isochrone = gpd.sjoin(buildings_gdf, transport_isochrone, how="inner", op="intersects")

buildings_in_walk_isochrone.to_file("C:/Users/sm_pa/OneDrive/Рабочий стол/analysys/citymodels/permModel/graphs/buildings_in_walk_isochrone.geojson", driver="GeoJSON")
buildings_in_drive_isochrone.to_file("C:/Users/sm_pa/OneDrive/Рабочий стол/analysys/citymodels/permModel/graphs/buildings_in_drive_isochrone.geojson", driver="GeoJSON")
buildings_in_transport_isochrone.to_file("C:/Users/sm_pa/OneDrive/Рабочий стол/analysys/citymodels/permModel/graphs/buildings_in_transport_isochrone.geojson", driver="GeoJSON")
