import folium
import geopandas as gpd
from folium import Choropleth

# Загрузка геоданных с местоположением сервисов
services_gdf = gpd.read_file('data/services.geojson')
services_gdf = services_gdf[(services_gdf['service_code'] == 'cafe') | (services_gdf['service_code'] == 'fast_food')]

# Загрузка геоданных с полигонами кварталов
quarters_gdf = gpd.read_file('data/blocks.geojson')

# Подсчет количества сервисов для каждого квартала
services_count_per_block = services_gdf.groupby('block_id').size().reset_index(name='num_services')

# Объединение количества сервисов с данными о кварталах
quarters_gdf = quarters_gdf.merge(services_count_per_block, left_on='id', right_on='block_id', how='left')

# Заполнение пропущенных значений (кварталов без сервисов)
quarters_gdf['num_services'] = quarters_gdf['num_services'].fillna(0)
print(quarters_gdf)

# Создание интерактивной карты с использованием Folium
map_center = [quarters_gdf['geometry'].centroid.y.mean(), quarters_gdf['geometry'].centroid.x.mean()]
mymap = folium.Map(location=map_center, zoom_start=12)

folium.GeoJson(quarters_gdf,
               name='Quarters',
               style_function=lambda x: {'fillColor': 'transparent', 'color': 'blue', 'weight': 2},
               highlight_function=lambda x: {'weight': 4},
               tooltip=folium.GeoJsonTooltip(fields=['num_services'], labels=True, sticky=False)
              ).add_to(mymap)

Choropleth(geo_data=quarters_gdf,
           data=quarters_gdf,
           columns=['block_id', 'num_services'],
           key_on='feature.properties.id',
           fill_color='YlOrRd',
           fill_opacity=0.7,
           line_opacity=0.2,
           legend_name='Number of Services',
           nan_fill_color='#ffffb2',
           ).add_to(mymap)

# Отображение интерактивной карты
mymap.save("provision/cafe_quantity.html")