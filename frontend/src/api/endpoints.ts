import client from './client';
import { User, Project, Site, SiteMetric, MetricsSummary } from '@/types';

type Credentials = { email: string; password: string };
type Registration = Credentials & { name: string };
type ProjectInput = Pick<Project, 'name' | 'description' | 'project_type' | 'tags'>;

export const api = {
  auth: {
    register: (data: Registration) => client.post('/auth/register', data),
    login: (data: Credentials) => client.post('/auth/login', data),
    logout: () => client.post('/auth/logout'),
    getMe: () => client.get<User>('/auth/me').then(r => r.data),
    refreshToken: () => client.post('/auth/refresh'),
  },
  projects: {
    getProjects: () => client.get<Project[]>('/projects').then(r => r.data),
    getProject: (id: string) => client.get<Project>(`/projects/${id}`).then(r => r.data),
    createProject: (data: ProjectInput) => client.post<Project>('/projects', data).then(r => r.data),
    updateProject: (id: string, data: Partial<ProjectInput>) => client.put<Project>(`/projects/${id}`, data).then(r => r.data),
    deleteProject: (id: string) => client.delete(`/projects/${id}`),
  },
  sites: {
    getSites: (projectId: string) => client.get<Site[]>(`/projects/${projectId}/sites`).then(r => r.data),
    getSite: (id: string) => client.get<Site>(`/sites/${id}`).then(r => r.data),
    createSite: (projectId: string, data: SiteCreate) => client.post<Site>(`/projects/${projectId}/sites`, data).then(r => r.data),
    deleteSite: (id: string) => client.delete(`/sites/${id}`),
    getAllSitesGeoJSON: () => client.get<GeoJSON.FeatureCollection>('/sites/all-geojson').then(r => r.data),
  },
  metrics: {
    getSiteMetrics: (siteId: string, start?: string, end?: string) => 
      client.get<SiteMetric[]>(`/sites/${siteId}/metrics`, { params: { start_date: start, end_date: end } }).then(r => r.data),
    getSiteMetricsSummary: (siteId: string) => client.get<MetricsSummary>(`/sites/${siteId}/metrics/summary`).then(r => r.data),
  }
};

export interface SiteCreate {
  name: string;
  geojson: GeoJSON.Polygon;
  ecosystem_type: string;
  monitoring_start_date: string;
}
