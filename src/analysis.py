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

def is_development_candidate(parcel, min_area, allowed_zones):
    if not parcel.is_active:
        return False
    if parcel.zone not in allowed_zones:
        return False
    if parcel.area_sqm < min_area:
        return False
    return True

def development_candidates(parcels, min_area, allowed_zones):
    candidates = []
    for parcel in parcels:
        if is_development_candidate(parcel, min_area, allowed_zones):
            candidates.append(parcel)
    return candidates

def intersecting_parcels(parcels, study_area):
    intersecting = []
    for parcel in parcels:
        if parcel.intersects(study_area):
            intersecting.append(parcel)
    return intersecting

def classify_suitability_grid(slope_grid, flood_grid, max_slope, max_flood):
    if len(slope_grid) != len(flood_grid):
        raise ValueError("Grid dimensions do not match")

    suitability_grid = []

    for row in range(len(slope_grid)):

        if len(slope_grid[row]) != len(flood_grid[row]):
            raise ValueError("Grid dimensions do not match")

        output_row = []

        for col in range(len(slope_grid[row])):

            slope = slope_grid[row][col]
            flood = flood_grid[row][col]

            if slope is None or flood is None:
                output_row.append(None)
                continue

            suitable = (
                slope <= max_slope
                and flood <= max_flood
            )

            output_row.append(1 if suitable else 0)

        suitability_grid.append(output_row)

    return suitability_grid

def count_suitable_cells(suitability_grid):

    suitable_count = 0

    for row in suitability_grid:

        for cell in row:

            if cell == 1:
                suitable_count += 1

    return suitable_count
