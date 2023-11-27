import warnings
warnings.simplefilter(action='ignore')

import geopandas as gpd
import folium


from CityGeoTools.metrics.data import CityInformationModel as BaseModel
from CityGeoTools.metrics.calculations import utils
from CityGeoTools.metrics.calculations import mobility_analysis


city_model = BaseModel.CityInformationModel(city_name="Perm", city_crs=32640, cwd="CityGeoTools")
city_model.update_layer("MobilityGraph", "./data/graph.graphml")

point = [[57.996353, 56.239028]]
point = utils.request_points_project(point, set_crs=4326, to_crs=32640)[0]

if city_model.methods.if_method_available("mobility_analysis"):
    walk_accessibility_zone = mobility_analysis.AccessibilityIsochrones(city_model).get_accessibility_isochrone(
        travel_type="walk",
        x_from=point[0],
        y_from=point[1],
        weight_type="time_min",
        weight_value=10)
    walk_isochrone = gpd.GeoDataFrame.from_features(walk_accessibility_zone["isochrone"]).set_crs(4326)
    walk_isochrone.to_file("C:/Users/sm_pa/OneDrive/Рабочий стол/analysys/citymodels/permModel/graphs/walk_isochrone.geojson", driver="GeoJSON")

    drive_accessibility_zone = mobility_analysis.AccessibilityIsochrones(city_model).get_accessibility_isochrone(
        travel_type="drive",
        x_from=point[0],
        y_from=point[1],
        weight_type="time_min",
        weight_value=5)
    drive_isochrone = gpd.GeoDataFrame.from_features(drive_accessibility_zone["isochrone"]).set_crs(4326)
    drive_isochrone.to_file("C:/Users/sm_pa/OneDrive/Рабочий стол/analysys/citymodels/permModel/graphs/drive_isochrone.geojson", driver="GeoJSON")

    transport_accessibility_zone = mobility_analysis.AccessibilityIsochrones(city_model).get_accessibility_isochrone(
        travel_type="public_transport",
        x_from=point[0],
        y_from=point[1],
        weight_type="time_min",
        weight_value=20)
    transport_isochrone = gpd.GeoDataFrame.from_features(transport_accessibility_zone["isochrone"]).set_crs(4326)
    transport_isochrone.to_file("C:/Users/sm_pa/OneDrive/Рабочий стол/analysys/citymodels/permModel/graphs/transport_isochrone.geojson", driver="GeoJSON")

map = folium.Map(location = [57.996353, 56.239028], zoom_start = 15, tiles='CartoDB positron')
folium.GeoJson(data=walk_isochrone, style_function=lambda x: {'fillColor': 'green'}).add_to(map)
folium.GeoJson(data=drive_isochrone, style_function=lambda x: {'fillColor': 'pink'}).add_to(map)
folium.GeoJson(data=transport_isochrone, style_function=lambda x: {'fillColor': 'yellow'}).add_to(map)
folium
folium.Marker([57.996353, 56.239028]).add_to(map)
map.save("graphs/intermodal_graph.html")