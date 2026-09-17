import uuid

from geoalchemy2 import Geography
from sqlalchemy import Date, DateTime, Float, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    geom = mapped_column(Geography(geometry_type="POLYGON", srid=4326), nullable=False)
    area_hectares: Mapped[float] = mapped_column(Float, nullable=False)
    ecosystem_type: Mapped[str] = mapped_column(String(100), nullable=False)
    monitoring_start_date = mapped_column(Date, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=text("now()"))

    project = relationship("Project", back_populates="sites")
    metrics = relationship("SiteMetric", back_populates="site", cascade="all, delete")
