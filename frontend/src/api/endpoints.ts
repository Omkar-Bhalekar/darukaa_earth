import client from './client';
import { User, Project, Site, SiteMetric, MetricsSummary } from '@/types';

type Credentials = { email: string; password: string };
type Registration = Credentials & { name: string };
type ProjectInput = Pick<Project, 'name' | 'description' | 'project_type' | 'tags'>;

export const api = {
  auth: {
    register: (data: Registration) => client.post('/api/auth/register', data),
    login: (data: Credentials) => client.post('/api/auth/login', data),
    logout: () => client.post('/api/auth/logout'),
    getMe: () => client.get<User>('/api/auth/me').then(r => r.data),
    refreshToken: () => client.post('/api/auth/refresh'),
  },
  projects: {
    getProjects: () => client.get<Project[]>('/api/projects').then(r => r.data),
    getProject: (id: string) => client.get<Project>(`/api/projects/${id}`).then(r => r.data),
    createProject: (data: ProjectInput) => client.post<Project>('/api/projects', data).then(r => r.data),
    updateProject: (id: string, data: Partial<ProjectInput>) => client.put<Project>(`/api/projects/${id}`, data).then(r => r.data),
    deleteProject: (id: string) => client.delete(`/api/projects/${id}`),
  },
  sites: {
    getSites: (projectId: string) => client.get<Site[]>(`/api/projects/${projectId}/sites`).then(r => r.data),
    getSite: (id: string) => client.get<Site>(`/api/sites/${id}`).then(r => r.data),
    createSite: (projectId: string, data: SiteCreate) => client.post<Site>(`/api/projects/${projectId}/sites`, data).then(r => r.data),
    deleteSite: (id: string) => client.delete(`/api/sites/${id}`),
    getAllSitesGeoJSON: () => client.get<GeoJSON.FeatureCollection>('/api/sites/all-geojson').then(r => r.data),
  },
  metrics: {
    getSiteMetrics: (siteId: string, start?: string, end?: string) => 
      client.get<SiteMetric[]>(`/api/sites/${siteId}/metrics`, { params: { start_date: start, end_date: end } }).then(r => r.data),
    getSiteMetricsSummary: (siteId: string) => client.get<MetricsSummary>(`/api/sites/${siteId}/metrics/summary`).then(r => r.data),
  }
};

export interface SiteCreate {
  name: string;
  geojson: GeoJSON.Polygon;
  ecosystem_type: string;
  monitoring_start_date: string;
}
