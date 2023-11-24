import geopandas as gpd

blocks_path = '../data/blocks.geojson'
blocks_gdf = gpd.read_file(blocks_path)
districts_path = '../data/districts.geojson'
districts_gdf = gpd.read_file(districts_path)

# Присоединение атрибута block_id к зданиям с использованием операции пересечения
joined_gdf = gpd.sjoin(blocks_gdf, districts_gdf, how='left', predicate='intersects')

# Выбор строки с наибольшей площадью для каждого блока
result_gdf = joined_gdf.loc[joined_gdf.groupby('block_id')['area'].idxmax()]

result_gdf['administrative_unit_id'] = result_gdf['id']
result_gdf['municipality_id'] = 1
result_gdf = result_gdf[['block_id', 'area', 'administrative_unit_id', 'municipality_id', 'geometry']]

print(result_gdf.columns.tolist())
nan_count = result_gdf['administrative_unit_id'].isna().sum()
print(f"Количество значений NaN в столбце administrative_unit_id: {nan_count}")

result_gdf.to_file('C:/Users/sm_pa/OneDrive/Рабочий стол/analysys/citymodels/permModel/blocks_with_adm_id.geojson', driver='GeoJSON')
