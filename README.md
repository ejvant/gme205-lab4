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

## Change the Policy Without Rewriting the Algorithm (Challenge 1)

The `development_candidates()` function was run using two different policy settings without changing its implementation.

| Policy | Minimum Area | Allowed Zones | Result |
|---|---:|---|---:|
| Policy 1 | 5,000 m² | Residential, Commercial | 45 candidates |
| Policy 2 | 7,000 m² | Residential, Commercial | 34 candidates |

The same algorithm produced different results because the policy parameters were changed rather than the function itself. Increasing the minimum area from 5,000 m² to 7,000 m² reduced the number of qualifying parcels from 45 to 34.

## Compose, Do Not Duplicate (Challenge 2)

The development candidates inside the study area were obtained by composing two existing analysis functions. First, `development_candidates()` applies the active, zone, and minimum-area rules. Its result is then passed to `intersecting_parcels()`, which applies the spatial intersection rule.

## Bad vs Good Refactor (Challenge 3)

An earlier version placed all development-candidate rules directly inside the loop:
```text
for parcel in parcels:
    if (
        parcel.is_active
        and parcel.zone in allowed_zones
        and parcel.area_sqm >= min_area
    ):
        candidates.append(parcel)
```
The cleaner version separates the decision rule into a helper function:
```text
def is_development_candidate(parcel, min_area, allowed_zones):
    if not parcel.is_active:
        return False
    if parcel.zone not in allowed_zones:
        return False
    if parcel.area_sqm < min_area:
        return False
    return True
```
The `is_development_candidate()` function is responsible for evaluating one parcel, while `development_candidates()` is responsible for iterating through the collection and collecting the results. This separation makes the logic easier to read, test, and extend without repeating the same conditions in other parts of the program.

## Transfer the Algorithmic Pattern (Challenge 4)

The parcel analysis and raster classification use different data representations, but they follow the same structure pattern.

For parcel analysis, the algorithm repeats over a collection of Parcel objects:
```text
FOR EACH parcel
    CHECK conditions
    SELECT or exclude the parcel
END FOR
```
For raster classification, the algorithm repeats through rows and columns:
```text
FOR EACH row
    FOR EACH column
        CHECK slope and flood conditions
        ASSIGN 1, 0, or NoData
    END FOR
END FOR
```
These specific parts are for data access and spatial rules. Parcel analysis uses object properties such as `is_active`, `zone`, and `area_sqm`, while raster classification accesses values using row and column positions and handles `NoData`.

The structure idea is the same: sequence executes steps in order, selection evaluates conditions, and repetition processes multiple records or cells. Both algorithms also keep the analysis logic separate from data loading and visualization.

## Reflection

1. *Algorithm:* I chose the development-candidate analysis as the vector-analysis question. Writing first the algorithm and pseudocode helped me to separate the decision rules from the process of iterating through parcels. Instead of writing one large loop, I identified the required conditions first: the parcel must be active, must belong to an allowed zone, and must meet the minimum area. This led to a design where `is_development_candidate()` evaluates the rules for one parcel while `development_candidates()` handles the collection. The organized implementation makes the analysis easier to test, and the policy can be changed through parameters without rewriting the algorithm.

2. *Control flow:* Sequence is present in the overall workflow. Specifically in loading the input data, constructing spatial objects, performing the analysis, and writing the results and visual outputs. Selection appears in the development-candidate rules and in the raster classification, where conditions must be met for a parcel or cell to be qualified. Repetition appears in the loops that process each parcel and in the nested row and column loops. These control structures in the algorithm helped the implementation traceable and predictable. 

3. *Responsibility:* Spatial geometry behavior, such as checking whether two spatial objects intersect, is a behavior that belongs to `Parcel` or `SpatialObject`. This keeps geometry operations with the objects that own the geometry. A rule that belongs to `analysis.py` is determining whether a parcel is a development candidate. This is a decision involving a collection of parcels and policy parameters rather than an inherent property of a parcel itself. Separating these responsibilities makes the system easier to modify. 

4. *Conditional Structure:* The specific design choice that prevents the development-candidate logic from becoming nested conditional chaos is the `is_development_candidate()` helper function. Each condition is checked separately with an early return when a parcel fails a requirement. This avoids repeating the same active, zone, and area conditions and keeps the main iteration easy to read.

5. *Area Meaning:* The exercise uses `area_sqm` because the parcel geometry is represented using geographic coordinate system (longitude and latitude in decimal degrees) and not projected metric coordinate system. `geometry.area` computes area in the geometry's native coordinate units and would produce an area in coordinate-system units rather than a reliable value in square meters. The provided `area_sqm` attribute already represents the intended metric area of each parcel. Using it therefore preserves its correct meaning.

6. *Vector vs Raster:* Repetition differs because vector processing iterates through a collection of individual `Parcel` objects, while raster processing uses two-dimensional repetition through rows and columns of cells. Each parcel is treated as an object with attributes and geometry. On the other hand, a raster cell is accessed through its row and column position and its corresponding value. However, both use the same structured pattern: repeat over a set of spatial elements, evaluate conditions for each element, and produce a result. he representation changes, but the structured-programming concepts of sequence, selection, and repetition remain the same.

7. *Scale:* If the dataset increased to one million parcels or a 10,000 × 10,000 raster, the separation between the spatial objects, analysis functions, and workflow would still be useful. However, the current approach would become slower and more demanding in terms of memory. For one million parcels, I could use a spatial database or indexing. Processing the data in smaller batches is also beneficial. For a very large raster, using arrays and processing the data in chunks would be more efficient. he main idea of separating the data, analysis rules, and workflow would stay the same, while the way the data is stored and processed would be adapted for larger datasets.

## Author
Enoch Joshua V. Antonio  
MS Geomatics Engineering

## References

- Python Documentation — More Control Flow Tools: https://docs.python.org/3/tutorial/controlflow.html
- W3Schools — Python Tutorials: https://www.w3schools.com/python/
- Python Documentation — `json` Module: https://docs.python.org/3/library/json.html
- Shapely Documentation — `shape()`: https://shapely.readthedocs.io/
- Shapely Documentation — Spatial Predicates and `intersects()`: https://shapely.readthedocs.io/
- Matplotlib Documentation: https://matplotlib.org/stable/

Edited on GitHub web interface and VS Code