from typing import Any

from fastapi import HTTPException, status


def polygon_from_geojson(raw: Any) -> dict:
    """Accept a Polygon, Feature, or FeatureCollection and return a closed Polygon."""
    if not isinstance(raw, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid GeoJSON payload"
        )

    geom = raw
    if raw.get("type") == "Feature":
        geom = raw.get("geometry") or {}
    elif raw.get("type") == "FeatureCollection":
        features = raw.get("features") or []
        if not features:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No polygon was drawn"
            )
        geom = features[0].get("geometry") or {}

    if geom.get("type") != "Polygon":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A polygon boundary is required",
        )

    coords = geom.get("coordinates") or []
    if not coords or not coords[0] or len(coords[0]) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Polygon needs at least three points",
        )

    ring = list(coords[0])
    if ring[0] != ring[-1]:
        ring.append(ring[0])
    return {"type": "Polygon", "coordinates": [ring, *coords[1:]]}
