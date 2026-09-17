import math
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import shape

class SpatialObject:

    def __init__(self, geometry):
        self.geometry = geometry

    def bbox(self):
        return self.geometry.bounds

    def intersects(self, other):
        return self.geometry.intersects(other.geometry)

class Point(SpatialObject):
    def __init__(self, id, lon, lat, name=None, tag=None):
        # Coordinate validation
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        self.id = id
        geometry = ShapelyPoint(lon, lat)
        super().__init__(geometry)
        self.name = name
        self.tag = tag

class Parcel(SpatialObject):
    def __init__(self, parcel_id, geometry, attributes: dict):
        super().__init__(geometry)
        self.parcel_id = parcel_id
        self.attributes = attributes

    @property
    def area_sqm(self):
        return float(self.attributes["area_sqm"])

    @property
    def zone(self):
        return self.attributes["zone"]

    @property
    def is_active(self):
        return bool(self.attributes["is_active"])

    @classmethod
    def from_dict(cls, record):
        geometry = shape(record["geometry"])

        attributes = {
            "zone": record["zone"],
            "is_active": record["is_active"],
            "area_sqm": record["area_sqm"],
        }

        return cls(
            record["parcel_id"],
            geometry,
            attributes
        )