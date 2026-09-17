import json
from shapely.geometry import box
from matplotlib import pyplot as plt
from spatial import Parcel, SpatialObject
from analysis import (
    total_active_area,
    parcels_above_threshold,
    count_by_zone,
    development_candidates,
    intersecting_parcels,
    classify_suitability_grid,
    count_suitable_cells
)

# Visualization

def create_vector_preview(parcels, candidates, study_area):
    plt.figure()

    candidate_ids = {
        parcel.parcel_id
        for parcel in candidates
    }

    other_label_added = False
    candidate_label_added = False

    for parcel in parcels:
        x, y = parcel.geometry.exterior.xy

        if parcel.parcel_id in candidate_ids:
            if not candidate_label_added:
                plt.plot(
                    x, y,
                    linewidth=2,
                    label="Development candidates"
                )
                candidate_label_added = True
            else:
                plt.plot(x, y, linewidth=2)
        else:
            if not other_label_added:
                plt.plot(
                    x, y,
                    linewidth=1,
                    label="Other parcels"
                )
                other_label_added = True
            else:
                plt.plot(x, y, linewidth=1)

    x, y = study_area.geometry.exterior.xy

    plt.plot(
        x, y,
        linewidth=3,
        label="Study area"
    )

    plt.title("Development Candidates and Study Area")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.axis("equal")
    plt.legend()

    plt.savefig(
        "output/lab4_vector_preview.png",
        dpi=150
    )

    plt.close()

def create_raster_preview(suitability_grid):
    display_grid = []

    for row in suitability_grid:
        display_row = []

        for cell in row:
            if cell is None:
                display_row.append(float("nan"))
            else:
                display_row.append(cell)

        display_grid.append(display_row)

    plt.figure()

    plt.imshow(
        display_grid,
        interpolation="nearest"
    )

    plt.title("Raster Suitability Classification")
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.colorbar(
    label="Suitability",
    ticks=[0, 1]
)

    plt.savefig(
        "output/lab4_raster_preview.png",
        dpi=150
    )

    plt.close()

def main():

    # 1. Load external parcel data
    with open("data/parcels_shapely_ready.json", "r") as file:
        parcel_records = json.load(file)

    # 2. Construct Parcel objects
    all_parcels = []

    for record in parcel_records:
        parcel = Parcel.from_dict(record)
        all_parcels.append(parcel)

    # 3. Validate required parcel input
    if not all_parcels:
        print("No valid parcels were loaded.")
        return

    # 4. Define analysis parameters
    MIN_AREA = 5000.0
    ALLOWED_ZONES = {"Residential", "Commercial"}

    study_area = SpatialObject(
        box(121.050, 14.648, 121.060, 14.658)
    )

    # 5. Call vector-analysis functions
    active_area = total_active_area(all_parcels)

    above_threshold = parcels_above_threshold(
        all_parcels,
        MIN_AREA
    )

    zone_counts = count_by_zone(all_parcels)

    candidates = development_candidates(
        all_parcels,
        min_area=MIN_AREA,
        allowed_zones=ALLOWED_ZONES
    )

    study_area_candidates = intersecting_parcels(
        candidates,
        study_area
    )

    # 6. Load raster data
    with open("data/suitability_grid.json", "r") as file:
        raster_data = json.load(file)

    slope_grid = raster_data["slope_deg"]
    flood_grid = raster_data["flood_m"]

    max_slope = raster_data["criteria"]["max_slope_deg"]
    max_flood = raster_data["criteria"]["max_flood_m"]

    suitability_grid = classify_suitability_grid(
        slope_grid,
        flood_grid,
        max_slope,
        max_flood
    )

    suitable_cell_count = count_suitable_cells(
        suitability_grid
    )

    # 7. Assemble JSON-ready report
    report = {
        "vector": {
            "parcel_count": len(all_parcels),
            "total_active_area_sqm": active_area,
            "zone_counts": zone_counts,
            "above_threshold_ids": [
                parcel.parcel_id
                for parcel in above_threshold
            ],
            "candidate_ids": [
                parcel.parcel_id
                for parcel in candidates
            ],
            "study_area_candidate_ids": [
                parcel.parcel_id
                for parcel in study_area_candidates
            ]
        },
        "raster": {
            "rows": len(suitability_grid),
            "cols": len(suitability_grid[0]),
            "suitable_cell_count": suitable_cell_count,
            "suitability_grid": suitability_grid
        }
    }

    # 8. Write report
    with open("output/lab4_report.json", "w") as file:
        json.dump(report, file, indent=4)

    # Create visual evidence
    create_vector_preview(
        all_parcels,
        candidates,
        study_area
    )

    create_raster_preview(
        suitability_grid
    )

    print("Lab 4 report created.")
    print("Vector preview created.")
    print("Raster preview created.")

if __name__ == "__main__":
    main()