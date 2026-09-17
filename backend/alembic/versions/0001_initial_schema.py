"""Create the initial Darukaa.Earth schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-09-17
"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography
from sqlalchemy.dialects import postgresql

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.create_table("users", sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True), sa.Column("email", sa.String(255), nullable=False, unique=True), sa.Column("hashed_password", sa.String(255), nullable=False), sa.Column("name", sa.String(255), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")))
    op.create_table("projects", sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True), sa.Column("owner_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False), sa.Column("name", sa.String(255), nullable=False), sa.Column("description", sa.Text()), sa.Column("project_type", sa.String(50), nullable=False), sa.Column("tags", postgresql.ARRAY(sa.String()), nullable=False, server_default="{}"), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")), sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")))
    op.create_table("sites", sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True), sa.Column("project_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("projects.id"), nullable=False), sa.Column("name", sa.String(255), nullable=False), sa.Column("geom", Geography(geometry_type="POLYGON", srid=4326), nullable=False), sa.Column("area_hectares", sa.Float(), nullable=False), sa.Column("ecosystem_type", sa.String(100), nullable=False), sa.Column("monitoring_start_date", sa.Date(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")))
    op.create_table("site_metrics", sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True), sa.Column("site_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sites.id"), nullable=False), sa.Column("recorded_date", sa.Date(), nullable=False), sa.Column("canopy_cover_pct", sa.Float()), sa.Column("ndvi", sa.Float()), sa.Column("carbon_tco2e", sa.Float()), sa.Column("biodiversity_index", sa.Float()))


def downgrade() -> None:
    op.drop_table("site_metrics")
    op.drop_table("sites")
    op.drop_table("projects")
    op.drop_table("users")
