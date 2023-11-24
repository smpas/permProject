import sys
import folium
import geopandas as gpd
from CityGeoTools.metrics.data import CityInformationModel as BaseModel

city_model = BaseModel.CityInformationModel(city_name="Perm", city_crs=32640, cwd="CityGeoTools")

city_model.update_layer("Buildings", "./data/buildings.geojson")
city_model.update_layer("Services", "./data/services.geojson")
city_model.update_layer("Blocks", "./data/blocks.geojson")

print(city_model.methods.spacematrix.message)

from CityGeoTools.metrics.calculations import spacematrix
blocks_morphotypes = spacematrix.Spacematrix(city_model).get_morphotypes()
blocks_morphotypes = gpd.GeoDataFrame.from_features(blocks_morphotypes).set_crs(4326)

def style_fn(feature):
    colors = [
        'red', 'blue', 'green', 'orange', 'purple', 'pink', 'cadetblue', 'darkblue',
        'lightgreen', 'darkred', 'yellow'
    ]
    return {'fillColor': colors[int(feature["properties"]["spacematrix_cluster"])]}

blocks_morphotypes_61 = blocks_morphotypes[blocks_morphotypes["administrative_unit_id"] == 61]
blocks_morphotypes_61 = blocks_morphotypes_61.dropna(subset=["spacematrix_cluster"])
map = folium.Map(location = [59.931, 30.250], zoom_start = 13, tiles='CartoDB positron')
geo_j = folium.GeoJson(
    data=blocks_morphotypes_61,
    style_function=style_fn,
    tooltip=folium.features.GeoJsonTooltip(["FSI", "GSI", "L", "MXI", "OSR", "spacematrix_cluster"])).add_to(map)
geo_j.add_to(map)
map