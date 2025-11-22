from typing import Annotated

from fastapi import HTTPException, Query

from app.models.bounding_box import BoundingBox


def parse_bbox(
    bbox: Annotated[
        str,
        Query(
            description="Bounding box: min_lng,min_lat,max_lng,max_lat",
            example="19.0,51.9,19.1,52.0",
        ),
    ],
) -> BoundingBox:
    """Parse and validate bbox string parameter"""
    try:
        return BoundingBox.from_string(bbox)
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid bbox parameter: {e}"
        ) from e
