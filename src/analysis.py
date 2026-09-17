from spatial import Parcel

def total_active_area(parcels):
    total = 0.0
    for parcel in parcels:
        if parcel.is_active:
            total += parcel.area_sqm
    return total

def parcels_above_threshold(parcels, threshold):
    selected_parcels =[]
    for parcel in parcels:
        if parcel.area_sqm >= threshold:
            selected_parcels.append(parcel)
    return selected_parcels

def count_by_zone(parcels):
    zone_counts ={}
    for parcel in parcels:
        if parcel.zone not in zone_counts:
            zone_counts[parcel.zone] = 0
        zone_counts[parcel.zone] += 1
    return zone_counts

def development_candidates(parcels, min_area, allowed_zones):
    candidates = []
    for parcel in parcels:
        if (
            parcel.is_active
            and parcel.zone in allowed_zones
            and parcel.area_sqm >= min_area
        ):
            candidates.append(parcel)
    return candidates

def intersecting_parcels(parcels, study_area):
    intersecting = []
    for parcel in parcels:
        if parcel.intersects(study_area):
            intersecting.append(parcel)
    return intersecting