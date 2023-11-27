import geopandas as gpd
import os

folder_path = '/data/services'

# Создаем пустой GeoDataFrame, который будет содержать все сервисы
combined_gdf = gpd.GeoDataFrame()

# Итерируемся по всем файлам в папке
for filename in os.listdir(folder_path):
    if filename.endswith(".geojson"):
        # Загружаем GeoDataFrame из файла
        service_gdf = gpd.read_file(os.path.join(folder_path, filename))

        # Добавляем поле "service_code" с названием сервиса
        service_gdf['service_code'] = filename[:-8]  # удаляем расширение ".geojson"

        columns_to_keep = ['service_code', 'geometry']
        service_gdf = service_gdf[columns_to_keep]
        combined_gdf = combined_gdf.append(service_gdf, ignore_index=True)

combined_gdf['id'] = range(1, len(combined_gdf) + 1)
# Сохраняем объединенный GeoDataFrame в новый GeoJSON файл
combined_gdf.to_file('C:/Users/sm_pa/OneDrive/Рабочий стол/analysys/citymodels/permModel/data/services.geojson', driver='GeoJSON')
