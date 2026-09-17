export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  project_type: 'carbon' | 'biodiversity';
  tags: string[];
  site_count: number;
  created_at: string;
}

export interface Site {
  id: string;
  project_id: string;
  name: string;
  geojson: GeoJSON.Polygon;
  area_hectares: number;
  ecosystem_type: string;
  monitoring_start_date: string;
  created_at: string;
}

export interface SiteMetric {
  id: string;
  site_id: string;
  recorded_date: string;
  canopy_cover_pct: number;
  ndvi: number;
  carbon_tco2e: number;
  biodiversity_index: number;
}

export interface MetricsSummary {
  latest: SiteMetric | null;
  aggregates: {
    total_carbon_tco2e: number;
    avg_ndvi: number;
    avg_canopy_cover_pct: number;
    avg_biodiversity_index: number;
  };
}
