import { useState, useEffect } from 'react';
import { api } from '@/api/endpoints';
import { Project, Site, MetricsSummary } from '@/types';

export const useProjects = () => {
  const [data, setData] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    api.projects.getProjects().then(setData).catch(setError).finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
};

export const useSites = (projectId: string) => {
  const [data, setData] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (projectId) {
      api.sites.getSites(projectId).then(setData).finally(() => setLoading(false));
    }
  }, [projectId]);

  return { data, loading };
};

export const useMetrics = (siteId: string) => {
  const [summary, setSummary] = useState<MetricsSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (siteId) {
      api.metrics.getSiteMetricsSummary(siteId).then(setSummary).finally(() => setLoading(false));
    }
  }, [siteId]);

  return { summary, loading };
};
