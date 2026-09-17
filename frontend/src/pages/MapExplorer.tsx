import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { PageShell } from '@/components/layout';
import { MapView } from '@/components/map/MapView';
import { api } from '@/api/endpoints';

export function MapExplorer() {
  const [data, setData] = useState<GeoJSON.FeatureCollection>({ type: 'FeatureCollection', features: [] }); const [selected, setSelected] = useState(''); const navigate = useNavigate();
  useEffect(() => { api.sites.getAllSitesGeoJSON().then(setData).catch(() => setData({ type: 'FeatureCollection', features: [] })); }, []);
  const sites = useMemo(() => data.features.map((feature) => ({ id: String(feature.properties?.id ?? ''), name: String(feature.properties?.name ?? 'Unnamed site'), project: String(feature.properties?.project_id ?? '') })), [data]);
  return <PageShell><div className="flex h-[calc(100vh-8rem)] overflow-hidden rounded-xl bg-white"><aside className="w-80 overflow-y-auto border-r p-4"><h1 className="mb-1 text-xl">Map Explorer</h1><p className="mb-4 text-sm text-charcoal/60">{sites.length} sites in your portfolio</p><div className="space-y-2">{sites.map((site) => <button key={site.id} onClick={() => setSelected(site.id)} className={`w-full rounded-lg p-3 text-left ${selected === site.id ? 'bg-sage/20' : 'hover:bg-sage/10'}`}><strong className="block">{site.name}</strong><span className="text-xs text-charcoal/60">Project {site.project.slice(0, 8)}</span>{selected === site.id && <span onClick={() => navigate(`/sites/${site.id}`)} className="mt-2 block text-sm text-forest-green underline">View details</span>}</button>)}</div></aside><MapView className="flex-1" geojson={data} onPolygonClick={setSelected} /></div></PageShell>;
}
