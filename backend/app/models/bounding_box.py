from typing import Self

from pydantic import BaseModel, Field, model_validator


class BoundingBox(BaseModel):
    """Bounding box model with validation"""

    min_lng: float = Field(..., ge=-180, le=180, description="Minimum longitude")
    min_lat: float = Field(..., ge=-90, le=90, description="Minimum latitude")
    max_lng: float = Field(..., ge=-180, le=180, description="Maximum longitude")
    max_lat: float = Field(..., ge=-90, le=90, description="Maximum latitude")

    @model_validator(mode="after")
    def check_lat_lng(self) -> Self:
        if self.max_lat <= self.min_lat:
            raise ValueError("max_lat must be greater than min_lat")
        if self.min_lng >= self.max_lng:
            raise ValueError("max_lng must be greater than min_lng")

        return self

    @classmethod
    def from_string(cls, bbox_string: str) -> "BoundingBox":
        """Parse bbox from comma-separated string"""
        try:
            coords = bbox_string.split(",")
            if len(coords) != 4:
                raise ValueError("bbox must have exactly 4 coordinates")

            return cls(
                min_lng=float(coords[0]),
                min_lat=float(coords[1]),
                max_lng=float(coords[2]),
                max_lat=float(coords[3]),
            )
        except (ValueError, IndexError) as e:
            raise ValueError(
                f"Failed to convert bbox string to BoundingBox: {e}"
            ) from e
