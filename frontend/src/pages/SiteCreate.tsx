import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { PageShell } from '@/components/layout';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { DrawingTool } from '@/components/map/DrawingTool';
import { api } from '@/api/endpoints';
import { apiErrorMessage } from '@/api/errors';

export function SiteCreate() {
  const { id: projectId } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [polygon, setPolygon] = useState<GeoJSON.Polygon>();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const save = async () => {
    if (!projectId) {
      setError('Missing project.');
      return;
    }
    if (!name.trim() || !polygon) {
      setError('Provide a site name and draw its boundary.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const site = await api.sites.createSite(projectId, {
        name: name.trim(),
        geojson: polygon,
        ecosystem_type: 'Forest',
        monitoring_start_date: new Date().toISOString().slice(0, 10),
      });
      navigate(`/sites/${site.id}`);
    } catch (err) {
      setError(apiErrorMessage(err, 'Could not save the site. Try again.'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageShell>
      <div className="mx-auto max-w-3xl">
        <h1 className="mb-2 text-2xl">Add a site</h1>
        <p className="mb-6 text-sm text-charcoal/70">
          Name the site and draw its boundary on the map.
        </p>
        <Card>
          {error && (
            <p className="mb-4 rounded bg-red-50 p-3 text-sm text-red-700">
              {error}
            </p>
          )}
          <div className="space-y-4">
            <Input
              label="Site name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              required
            />
            <DrawingTool onComplete={setPolygon} />
            {polygon && (
              <p className="text-sm text-sage">Boundary ready to save.</p>
            )}
            <div className="flex justify-between">
              <Button
                variant="outline"
                onClick={() => navigate(`/projects/${projectId}`)}
              >
                Cancel
              </Button>
              <Button onClick={save} isLoading={loading}>
                Save site
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </PageShell>
  );
}
