import json
from analysis import total_active_area, parcels_above_threshold, count_by_zone, development_candidates, intersecting_parcels
from spatial import Parcel, SpatialObject
from shapely.geometry import box

with open("data/parcels_shapely_ready.json", "r") as file:
    records = json.load(file)

# Check data

parcel = Parcel.from_dict(records[0])

print("Parcel ID:", parcel.parcel_id)
print("Zone:", parcel.zone)
print("Active:", parcel.is_active)
print("Area (sqm):", parcel.area_sqm)
print("Geometry type:", parcel.geometry.geom_type)

# Total active area

all_parcels = []

for record in records:
    parcel = Parcel.from_dict(record)
    all_parcels.append(parcel)

result = total_active_area(all_parcels)

print("Total active parcel area:", result, "sqm")

# Parcels above threshold

threshold = 5000.0

selected = parcels_above_threshold(all_parcels, threshold)

print("Parcels with area >=", threshold, "sqm:", len(selected))

for parcel in selected:
    print(
        "Parcel ID:", parcel.parcel_id,
        "| Area:", parcel.area_sqm
    )

# Count parcels by zone

zone_counts = count_by_zone(all_parcels)

print("Parcel count by zone:")

for zone, count in zone_counts.items():
    print(zone, ":", count)

# Development candidates

ALLOWED_ZONES = {"Residential", "Commercial"}
MIN_AREA = 5000.0

candidates = development_candidates(all_parcels, allowed_zones = ALLOWED_ZONES, min_area = MIN_AREA)

print("Development candidates:", len(candidates))

for parcel in candidates:
    print(
        "Parcel ID:", parcel.parcel_id,
        "| Zone:", parcel.zone,
        "| Active:", parcel.is_active,
        "| Area:", parcel.area_sqm
    )

# Intersecting parcels

study_area = SpatialObject(
    box(121.050, 14.648, 121.060, 14.658)
)

intersecting = intersecting_parcels(
    all_parcels,
    study_area
)

print("Parcels intersecting study area:", len(intersecting))

for parcel in intersecting:
    print(
        "Parcel ID:", parcel.parcel_id,
        "| Zone:", parcel.zone,
        "| Area:", parcel.area_sqm
    )