import json

from spatial import Parcel


with open("data/parcels_shapely_ready.json", "r") as file:
    records = json.load(file)

parcel = Parcel.from_dict(records[1])

print("Parcel ID:", parcel.parcel_id)
print("Zone:", parcel.zone)
print("Active:", parcel.is_active)
print("Area (sqm):", parcel.area_sqm)
print("Geometry type:", parcel.geometry.geom_type)