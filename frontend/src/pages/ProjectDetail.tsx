import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MapPin } from 'lucide-react';
import { PageShell } from '@/components/layout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Skeleton } from '@/components/ui/Skeleton';
import { EmptyState } from '@/components/ui/EmptyState';
import { PolygonThumb } from '@/components/map/PolygonThumb';
import { useSites } from '@/hooks';
import { api } from '@/api/endpoints';
import { Project } from '@/types';

export const ProjectDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project | null>(null);
  const { data: sites, loading: sitesLoading } = useSites(id!);

  useEffect(() => {
    if (id) {
      api.projects.getProject(id).then(setProject);
    }
  }, [id]);

  if (!project) {
    return (
      <PageShell>
        <Skeleton className="h-64 w-full" />
      </PageShell>
    );
  }

  const goAddSite = () => navigate(`/projects/${id}/sites/new`);

  return (
    <PageShell>
      <div className="mb-8">
        <div className="flex justify-between items-start gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl">{project.name}</h1>
              <Badge type={project.project_type} />
            </div>
            <p className="text-charcoal/70 max-w-3xl">{project.description}</p>
          </div>
          <Button onClick={goAddSite}>Add Site</Button>
        </div>
      </div>

      <h2 className="text-xl mb-4">Sites ({sites.length})</h2>
      {sitesLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Skeleton className="h-48 w-full" />
          <Skeleton className="h-48 w-full" />
        </div>
      ) : sites.length === 0 ? (
        <EmptyState
          icon={MapPin}
          title="No sites yet"
          description="Draw a boundary on the map to add the first site for this project."
          actionLabel="Add Site"
          onAction={goAddSite}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sites.map((site) => (
            <Card
              key={site.id}
              className="cursor-pointer"
              onClick={() => navigate(`/sites/${site.id}`)}
            >
              <h3 className="text-lg font-medium text-forest-green mb-1">
                {site.name}
              </h3>
              <p className="text-sm text-charcoal/60 mb-2">
                Area: {site.area_hectares.toFixed(1)} ha
              </p>
              <PolygonThumb geojson={site.geojson} />
            </Card>
          ))}
        </div>
      )}
    </PageShell>
  );
};
