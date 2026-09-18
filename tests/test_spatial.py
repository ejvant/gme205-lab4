import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shapely.geometry import Polygon
from spatial import Parcel


def test_parcel_from_dict():
    record = {
        "parcel_id": 101,
        "zone": "Residential",
        "is_active": True,
        "area_sqm": 2500.0,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [121.050, 14.650],
                [121.051, 14.650],
                [121.051, 14.651],
                [121.050, 14.651],
                [121.050, 14.650]
            ]]
        }
    }

    parcel = Parcel.from_dict(record)

    assert parcel.parcel_id == 101
    assert parcel.zone == "Residential"
    assert parcel.is_active is True
    assert parcel.area_sqm == 2500.0
    assert isinstance(parcel.geometry, Polygon)