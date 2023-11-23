import geopandas as gpd

blocks_path = './data/blocks.geojson'
blocks_gdf = gpd.read_file(blocks_path)
services_path = './data/services.geojson'
services_gdf = gpd.read_file(services_path)

# Присоединение атрибута block_id
joined_gdf = gpd.sjoin(services_gdf, blocks_gdf, how='left', predicate='within')
result_gdf = joined_gdf[['id', 'service_code', 'block_id', 'geometry']]

districts_path = './data/districts.geojson'
districts_gdf = gpd.read_file(districts_path)
districts_gdf['administrative_unit_id'] = districts_gdf['id']

# Присоединение атрибутов municipality_id и administrative_unit_id
joined_gdf_districts = gpd.sjoin(result_gdf, districts_gdf, how='left', predicate='within')
joined_gdf_districts['municipality_id'] = 1
joined_gdf_districts['id'] = joined_gdf_districts['id_left']
final_gdf = joined_gdf_districts[['id', 'service_code', 'block_id', 'administrative_unit_id', 'municipality_id', 'geometry']]

final_gdf.to_file('C:/Users/sm_pa/OneDrive/Рабочий стол/analysys/citymodels/permModel/data/services1.geojson', driver='GeoJSON')
