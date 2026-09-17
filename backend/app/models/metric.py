import uuid
from sqlalchemy import Float, Date, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.database import Base

class SiteMetric(Base):
    __tablename__ = "site_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    site_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False)
    recorded_date = mapped_column(Date, nullable=False)
    canopy_cover_pct: Mapped[float] = mapped_column(Float, nullable=True)
    ndvi: Mapped[float] = mapped_column(Float, nullable=True)
    carbon_tco2e: Mapped[float] = mapped_column(Float, nullable=True)
    biodiversity_index: Mapped[float] = mapped_column(Float, nullable=True)

    site = relationship("Site", back_populates="metrics")
