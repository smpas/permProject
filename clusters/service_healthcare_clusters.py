import folium
import geopandas as gpd

from CityGeoTools.metrics.data import CityInformationModel as BaseModel
from CityGeoTools.metrics.calculations import services_clusterization

city_model = BaseModel.CityInformationModel(city_name="Perm", city_crs=32640, cwd="CityGeoTools")
city_model.update_layer("Services", "./data/services.geojson")

service_clusterization = services_clusterization.ServicesClusterization(city_model).get_clusters_polygon(
    service_types=['child_polyclinic', 'child_hospital', 'dentist', 'hospital', 'polyclinic', 'roddom', 'trauma'], n_std=2, condition_value=1000
    )

service_points = gpd.GeoDataFrame.from_features(service_clusterization['services']).set_crs(4326)
service_clusters = gpd.GeoDataFrame.from_features(service_clusterization['polygons']).set_crs(4326)

map_center = [58.014490, 56.231816]
map = folium.Map(location=map_center, zoom_start=13, tiles='CartoDB positron')

service_colors = {
    'child_polyclinic': 'red',
    'child_hospital': 'blue',
    'dentist': 'purple',
    'hospital': 'pink',
    'polyclinic': 'black',
    'roddom': 'brown',
    'trauma': 'grey'
}

for idx, row in service_points.iterrows():
    service_type = row['service_code']
    color = service_colors.get(service_type, 'gray')
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=3,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"Service Type: {service_type}"
    ).add_to(map)

geo_j = folium.GeoJson(
    data=service_clusters,
    tooltip=folium.features.GeoJsonTooltip(['child_polyclinic', 'child_hospital', 'dentist', 'hospital', 'polyclinic', 'roddom', 'trauma'])
).add_to(map)

legend_html = """
<div style="position: fixed; bottom: 50px; left: 50px; z-index:1000; font-size:14px; background-color:white; padding: 10px; border:1px solid grey; border-radius:5px;">
    <p style="margin:0;"><strong>Legend</strong></p>
"""

for service_type, color in service_colors.items():
    legend_html += f'<p style="margin:0;"><span style="color:{color}; font-size:20px;">&bull;</span> {service_type.capitalize()}</p>'

legend_html += "</div>"

map.get_root().html.add_child(folium.Element(legend_html))

map.save("clusters/healthcare_clusters.html")