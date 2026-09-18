import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shapely.geometry import box
from spatial import Parcel, SpatialObject
from analysis import (
    total_active_area,
    parcels_above_threshold,
    count_by_zone,
    development_candidates,
    intersecting_parcels,
    classify_suitability_grid,
    count_suitable_cells,
)


def make_parcel(parcel_id, zone, active, area, geometry=None):
    if geometry is None:
        geometry = box(121.0, 14.0, 121.001, 14.001)

    return Parcel(
        parcel_id,
        geometry,
        {
            "zone": zone,
            "is_active": active,
            "area_sqm": area,
        },
    )


def test_total_active_area_excludes_inactive():
    parcels = [
        make_parcel(1, "Residential", True, 1000.0),
        make_parcel(2, "Commercial", False, 2000.0),
    ]

    assert total_active_area(parcels) == 1000.0


def test_parcels_above_threshold_includes_exact_threshold():
    parcels = [
        make_parcel(1, "Residential", True, 5000.0),
        make_parcel(2, "Residential", True, 4999.0),
    ]

    result = parcels_above_threshold(parcels, 5000.0)

    assert [parcel.parcel_id for parcel in result] == [1]


def test_count_by_zone():
    parcels = [
        make_parcel(1, "Residential", True, 1000.0),
        make_parcel(2, "Residential", True, 2000.0),
        make_parcel(3, "Commercial", True, 3000.0),
        make_parcel(4, "Industrial", True, 4000.0),
    ]

    result = count_by_zone(parcels)

    assert result == {
        "Residential": 2,
        "Commercial": 1,
        "Industrial": 1,
    }


def test_development_candidates_rejects_each_reason():
    allowed_zones = {"Residential", "Commercial"}

    parcels = [
        make_parcel(1, "Residential", False, 6000.0),
        make_parcel(2, "Industrial", True, 6000.0),
        make_parcel(3, "Residential", True, 4999.0),
        make_parcel(4, "Commercial", True, 5000.0),
    ]

    result = development_candidates(
        parcels,
        min_area=5000.0,
        allowed_zones=allowed_zones,
    )

    result_ids = [parcel.parcel_id for parcel in result]

    assert 1 not in result_ids
    assert 2 not in result_ids
    assert 3 not in result_ids
    assert 4 in result_ids


def test_intersecting_parcels():
    inside = make_parcel(
        1,
        "Residential",
        True,
        5000.0,
        box(2, 2, 4, 4),
    )

    outside = make_parcel(
        2,
        "Residential",
        True,
        5000.0,
        box(20, 20, 22, 22),
    )

    parcels = [inside, outside]

    study_area = SpatialObject(
        box(0, 0, 10, 10)
    )

    result = intersecting_parcels(parcels, study_area)

    result_ids = [parcel.parcel_id for parcel in result]

    assert 1 in result_ids
    assert 2 not in result_ids


def test_classify_suitability_grid():
    slope_grid = [
        [10, 20],
        [None, 15],
    ]

    flood_grid = [
        [0.3, 0.2],
        [0.1, 0.5],
    ]

    result = classify_suitability_grid(
        slope_grid,
        flood_grid,
        max_slope=15.0,
        max_flood=0.5,
    )

    assert result == [
        [1, 0],
        [None, 1],
    ]


def test_count_suitable_cells_ignores_zero_and_nodata():
    suitability_grid = [
        [1, 0, None],
        [0, 1, None],
    ]

    result = count_suitable_cells(suitability_grid)

    assert result == 2

## Invariants

def test_count_by_zone_invariant():
    parcels = [
        make_parcel(1, "Residential", True, 1000.0),
        make_parcel(2, "Residential", True, 2000.0),
        make_parcel(3, "Commercial", True, 3000.0),
        make_parcel(4, "Industrial", False, 4000.0),
    ]

    zone_counts = count_by_zone(parcels)

    assert sum(zone_counts.values()) == len(parcels)

def test_study_area_candidates_are_subset_of_candidates():
    allowed_zones = {"Residential", "Commercial"}
    min_area = 5000.0

    inside_candidate = make_parcel(
        1,
        "Residential",
        True,
        6000.0,
        box(2, 2, 4, 4),
    )

    outside_candidate = make_parcel(
        2,
        "Commercial",
        True,
        7000.0,
        box(20, 20, 22, 22),
    )

    not_candidate = make_parcel(
        3,
        "Industrial",
        True,
        8000.0,
        box(3, 3, 5, 5),
    )

    parcels = [
        inside_candidate,
        outside_candidate,
        not_candidate,
    ]

    candidates = development_candidates(
        parcels,
        min_area=min_area,
        allowed_zones=allowed_zones,
    )

    study_area = SpatialObject(
        box(0, 0, 10, 10)
    )

    study_area_candidates = intersecting_parcels(
        candidates,
        study_area,
    )

    assert all(
        parcel in candidates
        for parcel in study_area_candidates
    )


def test_raster_output_dimensions_match_input():
    slope_grid = [
        [10, 20, 5],
        [15, 12, 8],
    ]

    flood_grid = [
        [0.2, 0.6, 0.3],
        [0.5, 0.4, 0.1],
    ]

    result = classify_suitability_grid(
        slope_grid,
        flood_grid,
        max_slope=15.0,
        max_flood=0.5,
    )

    assert len(result) == len(slope_grid)

    assert all(
        len(result[row]) == len(slope_grid[row])
        for row in range(len(slope_grid))
    )