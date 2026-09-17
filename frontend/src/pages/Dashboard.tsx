import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useProjects } from '@/hooks';
import { PageShell } from '@/components/layout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { EmptyState } from '@/components/ui/EmptyState';
import { Skeleton } from '@/components/ui/Skeleton';
import { TreePine } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const { data: projects, loading } = useProjects();
  const navigate = useNavigate();

  return (
    <PageShell>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl">Your Projects</h1>
        <Button onClick={() => navigate('/projects/new')}>Create Project</Button>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => <Skeleton key={i} className="h-48 w-full" />)}
        </div>
      ) : projects.length === 0 ? (
        <EmptyState
          icon={TreePine}
          title="No projects yet"
          description="Create your first reforestation or biodiversity project to get started."
          actionLabel="Create Project"
          onAction={() => navigate('/projects/new')}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map(project => (
            <Card key={project.id} className="cursor-pointer" onClick={() => navigate(`/projects/${project.id}`)}>
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg text-forest-green truncate mr-2">{project.name}</h3>
                <Badge type={project.project_type} />
              </div>
              <p className="text-sm text-charcoal/70 line-clamp-2 mb-4">{project.description}</p>
              <div className="text-xs text-charcoal/50 flex justify-between">
                <span>{project.site_count} Sites</span>
                <span>{new Date(project.created_at).toLocaleDateString()}</span>
              </div>
            </Card>
          ))}
        </div>
      )}
    </PageShell>
  );
};
