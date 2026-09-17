import { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import MapboxDraw from '@mapbox/mapbox-gl-draw';
import '@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css';
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN ?? '';

export function DrawingTool({ onComplete }: { onComplete: (geojson: GeoJSON.Polygon) => void }) {
  const container = useRef<HTMLDivElement>(null);
  const draw = useRef<MapboxDraw>();
  const [error, setError] = useState('');
  useEffect(() => {
    if (!container.current) return;
    const map = new mapboxgl.Map({ container: container.current, style: 'mapbox://styles/mapbox/satellite-streets-v12', center: [78.9629, 20.5937], zoom: 3.5 });
    const control = new MapboxDraw({ displayControlsDefault: false, controls: { polygon: true, trash: true } });
    draw.current = control;
    map.addControl(control, 'top-left');
    return () => map.remove();
  }, []);
  const confirm = () => {
    const feature = draw.current?.getAll().features[0];
    if (!feature || feature.geometry.type !== 'Polygon') { setError('Draw a polygon before confirming.'); return; }
    onComplete(feature.geometry);
  };
  return <div className="relative h-[420px] overflow-hidden rounded-xl"><div ref={container} className="h-full" /><div className="absolute bottom-3 left-3 rounded-lg bg-white/95 p-3 shadow"><p className="mb-2 text-sm">Click the polygon tool, place points, then double-click to finish.</p>{error && <p className="mb-2 text-sm text-red-700">{error}</p>}<button type="button" onClick={confirm} className="rounded bg-forest-green px-3 py-2 text-sm text-white">Confirm polygon</button></div></div>;
}
