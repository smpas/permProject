import sys
import os
import numpy as np
from CityGeoTools.metrics.data import CityInformationModel as BaseModel

city_model = BaseModel.CityInformationModel(city_name="Perm", city_crs=32640, cwd="CityGeoTools")

city_model.update_layer("Buildings", "./data/buildings.geojson")
city_model.update_layer("Blocks", "./data/blocks.geojson")
city_model.update_layer("Services", "./data/services.geojson")

print("All methods implemented in CityGeoTools:\n")

all_methods = city_model.methods.get_list_of_methods()
available_methods = city_model.methods.get_list_of_available_methods()

for method in all_methods:
    if method in available_methods:
        print(method, "--> available")
    else:
        print(method, "--> unavailable")

print(city_model.get_all_attributes())