import geopandas as gpd

blocks_path = '../data/blocks.geojson'
blocks_gdf = gpd.read_file(blocks_path)
buildings_path = '../data/buildings.geojson'
buildings_gdf = gpd.read_file(buildings_path)

# Присоединение атрибута block_id к зданиям
joined_gdf = gpd.sjoin(buildings_gdf, blocks_gdf, how='left', predicate='within')
joined_gdf['storeys_count'] = joined_gdf['storey_count']
result_gdf = joined_gdf[['id', 'function', 'is_living', 'storeys_count', 'basement_area', 'total_area', 'population', 'living_area', 'block_id', 'geometry']]

result_gdf.to_file('C:/Users/sm_pa/OneDrive/Рабочий стол/analysys/citymodels/permModel/buildings_with_blockid.geojson', driver='GeoJSON')
