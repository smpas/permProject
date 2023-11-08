import sys
import os
import numpy as np
from CityGeoTools.metrics.data import CityInformationModel as BaseModel

city_model = BaseModel.CityInformationModel(city_name="Perm", city_crs=32640, cwd="CityGeoTools")
print(city_model.city_crs)