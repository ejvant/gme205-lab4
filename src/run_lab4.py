import json
from shapely.geometry import box
from spatial import Parcel, SpatialObject
from analysis import development_candidates, intersecting_parcels

# Load parcel data
with open("data/parcels_shapely_ready.json", "r") as file:
    records = json.load(file)

all_parcels = []

for record in records:
    parcel = Parcel.from_dict(record)
    all_parcels.append(parcel)

# Analysis parameters
MIN_AREA = 5000.0
ALLOWED_ZONES = {"Residential", "Commercial"}

# Define study area
study_area = SpatialObject(
    box(121.050, 14.648, 121.060, 14.658)
)

# Find development candidates
candidates = development_candidates(
    all_parcels,
    min_area=MIN_AREA,
    allowed_zones=ALLOWED_ZONES
)

# Find candidates that intersect the study area
inside_study_area = intersecting_parcels(
    candidates,
    study_area
)

# Display result
print("Development candidates:", len(candidates))
print(
    "Development candidates inside study area:",
    len(inside_study_area)
)

for parcel in inside_study_area:
    print(
        "Parcel ID:", parcel.parcel_id,
        "| Zone:", parcel.zone,
        "| Area:", parcel.area_sqm
    )