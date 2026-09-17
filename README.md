# GmE 205: Laboratory Exercise 4
**Spatial Algorithms and Structured Programming**
## Overview
*This laboratory exercise applies structured programming and object-oriented programming concepts to spatial analysis using Python and Shapely. It focuses on translating familiar GIS operations into clear and explicit algorithms using sequence, selection, repetition, and functions. The exercise also emphasizes the proper organization of spatial objects and analysis functions so that each component has a clear and specific responsibility. Through vector-based parcel analysis and raster-style data processing, the laboratory demonstrates how spatial decision-making can be implemented systematically without relying on high-level GIS libraries that hide the underlying computational logic.*

## How to set up the virtual environment
The steps to set up a virtual environment:
1. Open Visual Studio Code.
2. Under the VS Code Terminal tab, select "New Terminal".
3. In the Terminal, run:

   `py -m venv .venv`

   `.\.venv\Scripts\activate`

4. When successful, your terminal prompt should show `(.venv)`.

## Vector Analysis - Algorithm
*Inputs:*

- `data/parcels_shapely_ready.json`
- Chosen area threshold
- Study-area polygon

*Outputs:*

- Total area of active parcels
- Parcels meeting the area threshold
- Number of parcels per zone
- Development candidate parcels
- Parcels intersecting the study area

*Algorithm:*

1. Start
2. [SEQUENCE] Load `data/parcels_shapely_ready.json`.
3. [SEQUENCE] Convert each parcel record into a `Parcel` object.
4. [SEQUENCE] Store all `Parcel` objects in `all_parcels`.
5. [SELECTION] If no parcels were loaded:
    - Display "No parcels found".
    - Stop the analysis.
6. [SEQUENCE] Initialize:
    - `total_active_area` = 0
    - `parcels_above_threshold` = empty list
    - `count_by_zone` = empty dictionary
    - `development_candidates` = empty list
    - `intersecting_parcels` = empty list
7. [REPETITION] For each parcel in `all_parcels`:
    - [SELECTION] If the parcel is active:
        Add `parcel.area_sqm` to `total_active_area`.
    - [SELECTION] If `parcel.area_sqm` is greater than or equal to the chosen area threshold:
        Add the parcel to `parcels_above_threshold`.
    - [SELECTION] If the parcel's zone is not yet in `count_by_zone`:
        Create an entry for that zone with a count of 0.
        Increment `count_by_zone[parcel.zone]` by 1.
    - [SELECTION] If the parcel is active AND its zone is Residential or Commercial AND its area is at least 5,000 m²:
        Add the parcel to `development_candidates`.
    - [SELECTION] If the parcel intersects the study-area polygon:
        Add the parcel to `intersecting_parcels`.
8. [SEQUENCE] Return or report:
    - `total_active_area`
    - `parcels_above_threshold`
    - `count_by_zone`
    - `development_candidates`
    - `intersecting_parcels`
9. [SEQUENCE] Save the analysis results to `output/summary.json`
10. End

## Vector Analysis - Pseudocode

```text

BEGIN
    LOAD data/parcel.json

    IF parcel.json DOES NOT EXIST THEN
    PRINT "Error: File does not exist"
    STOP
    END IF

    CONVERT record INTO Parcel objects
    STORE IN all_parcels

    IF all_parcels IS EMPTY THEN
    PRINT "No parcels found"
    STOP
    END IF

    SET total_active_area = 0
    SET parcels_above_threshold = empty list
    SET count_by_zone = empty dictionary
    SET development_candidates = empty list
    SET intersecting_parcels = empty list

    FOR EACH parcel IN all_parcels
        IF parcel.is_active
            ADD parcel.area_sqm to total_active_area
        END IF

        IF parcel.area_sqm >= area_threshold
            ADD parcel to parcels_above_threshold
        END IF

        IF parcel.zone NOT IN count_by_zone
            SET count_by_zone[parcel.zone] = 0
        END IF

        INCREMENT count_by_zone[parcel.zone] BY 1

        IF parcel.is_active
            AND (parcel.zone is "Residential" OR parcel.zone is "Commercial")
            AND parcel.area_sqm >= 5000
            ADD parcel to development_candidates
        END IF

        IF parcel intersects study_area
            ADD parcel to intersecting_parcels
        END IF
    END FOR

    SAVE summary TO output/summary.json

    RETURN total_active_area, 
    parcels_above_threshold, 
    count_by_zone,
    development_candidates,
    intersecting_parcels

END
```

## Raster Analysis - Algorithm

*Inputs:*

- `slope_grid`
- `flood_grid`
- `max_slope`
- `max_flood`

*Outputs:*
- `suitability_grid`
- `suitable_cell_count`

*Algorithm:*

1. Start
2. [SEQUENCE] Load the slope and flood grids from `data/suitability_grid.json`.
3. [SELECTION] Verify that the `slope_grid` and `flood_grid` have the same number of rows and columns.
    - If their dimensions do not match, stop the analysis and report the mismatch.
4. [SEQUENCE] Create an empty `suitability_grid`.
5. [SEQUENCE] Set `suitable_cell_count` to 0.
6. [REPETITION] Repeat through every row of the grids.
7. [SEQUENCE] Create an empty output row for the current row.
8. [REPETITION] Repeat through every column in the current row.
9. [SEQUENCE] Get the slope and flood values of the current cell.
10. [SELECTION] If either input cell is `NoData`:
    - Write `null` to the corresponding output cell.
11. [SELECTION] Otherwise, check whether both suitability criteria are satisfied:
    - slope ≤ `max_slope`
    - flood ≤ `max_flood`
12. [SEQUENCE] If both criteria are satisfied:
    - Write `1` to the output cell.
    - Increase `suitable_cell_count` by 1.
13. [SEQUENCE] If the criteria are not satisfied:
    - Write `0` to the output cell.
14. [SEQUENCE] Add the completed output row to `suitability_grid`.
15. [SEQUENCE] Return `suitability_grid` and `suitable_cell_count`.
16. End

## Raster Analysis - Pseudocode

```text

BEGIN
    LOAD data/suitability_grid.json

    IF number of rows in slope_grid is NOT EQUAL to
       number of rows in flood_grid
        PRINT "Grid dimensions do not match"
        STOP
    END IF

    IF number of columns in slope_grid is NOT EQUAL to
       number of columns in flood_grid
        PRINT "Grid dimensions do not match"
        STOP
    END IF

    CREATE empty suitability_grid
    SET suitable_cell_count = 0

    FOR EACH row IN slope_grid
        CREATE empty output_row
        FOR EACH column IN row
            GET slope cell
            GET flood cell
            IF either cell is NoData
                WRITE null TO output_row
            ELSE IF slope cell <= max_slope
                AND flood cell <= max_flood
                WRITE 1 TO output_row
                INCREMENT suitable_cell_count
            ELSE
                WRITE 0 TO output_row
            END IF
        END FOR
        ADD output_row TO suitability_grid

    END FOR

    RETURN suitability_grid, suitable_cell_count

END
```