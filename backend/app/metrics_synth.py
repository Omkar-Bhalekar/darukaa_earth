import math
import random
import uuid
from datetime import date

from dateutil.relativedelta import relativedelta

from app.models.metric import SiteMetric


def synthetic_monthly_metrics(
    site_id: uuid.UUID, start_date: date, months: int = 36
) -> list[SiteMetric]:
    """Restoration-style time series for charts when no field sensor feed exists.

    Canopy follows a logistic curve, NDVI a seasonal trend, carbon a linear ramp,
    and biodiversity a stepwise recovery. Values are mock but internally consistent
    so site analytics work immediately after a polygon is saved.
    """
    metrics: list[SiteMetric] = []
    for month in range(months):
        recorded = start_date + relativedelta(months=month)
        canopy = 85 / (1 + math.exp(-0.15 * (month - 18))) + random.gauss(0, 2)
        ndvi = (
            0.3
            + 0.4 * (month / max(months, 1))
            + 0.05 * math.sin(2 * math.pi * month / 12)
            + random.gauss(0, 0.03)
        )
        carbon = 5 + 10 * (month / max(months, 1)) + random.gauss(0, 0.5)
        bio = 0.3
        if month >= 18:
            bio = 0.7
        elif month >= 12:
            bio = 0.5
        elif month >= 6:
            bio = 0.4
        bio += random.gauss(0, 0.05)
        metrics.append(
            SiteMetric(
                site_id=site_id,
                recorded_date=recorded,
                canopy_cover_pct=max(0, min(100, canopy)),
                ndvi=max(0, min(1, ndvi)),
                carbon_tco2e=max(0, carbon),
                biodiversity_index=max(0, min(1, bio)),
            )
        )
    return metrics
