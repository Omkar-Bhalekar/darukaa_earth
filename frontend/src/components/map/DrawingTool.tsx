import { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import MapboxDraw from '@mapbox/mapbox-gl-draw';
import '@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import { applyMapboxToken, basemapStyle } from './mapStyle';

applyMapboxToken();

export function DrawingTool({
  onComplete,
}: {
  onComplete: (geojson: GeoJSON.Polygon) => void;
}) {
  const container = useRef<HTMLDivElement>(null);
  const mapRef = useRef<mapboxgl.Map>();
  const draw = useRef<MapboxDraw>();
  const [error, setError] = useState('');
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!container.current) return;
    applyMapboxToken();
    const map = new mapboxgl.Map({
      container: container.current,
      style: basemapStyle(),
      center: [78.9629, 20.5937],
      zoom: 4,
    });
    const control = new MapboxDraw({
      displayControlsDefault: false,
      controls: {},
    });
    draw.current = control;
    mapRef.current = map;
    map.on('load', () => {
      map.addControl(control);
      map.resize();
    });
    const resize = () => map.resize();
    window.addEventListener('resize', resize);
    const timer = window.setTimeout(resize, 250);
    return () => {
      window.clearTimeout(timer);
      window.removeEventListener('resize', resize);
      map.remove();
      mapRef.current = undefined;
    };
  }, []);

  const startDraw = () => {
    setError('');
    setReady(false);
    draw.current?.changeMode('draw_polygon');
  };

  const clear = () => {
    draw.current?.deleteAll();
    setReady(false);
    setError('');
  };

  const confirm = () => {
    const feature = draw.current?.getAll().features[0];
    if (!feature || feature.geometry.type !== 'Polygon') {
      setError(
        'Click Draw boundary, then place points on the map and double-click to finish.',
      );
      setReady(false);
      return;
    }
    onComplete(feature.geometry);
    setReady(true);
    setError('');
  };

  return (
    <div className="relative h-[420px] overflow-hidden rounded-xl">
      <div ref={container} className="h-full w-full" />
      <div className="absolute bottom-3 left-3 right-3 rounded-lg bg-white/95 p-3 shadow">
        <p className="mb-2 text-sm">
          Click <strong>Draw boundary</strong>, add points on the imagery, then
          double-click to close the shape.
        </p>
        {error && <p className="mb-2 text-sm text-red-700">{error}</p>}
        {ready && (
          <p className="mb-2 text-sm text-forest-green">Boundary captured.</p>
        )}
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={startDraw}
            className="rounded bg-forest-green px-3 py-2 text-sm text-white"
          >
            Draw boundary
          </button>
          <button
            type="button"
            onClick={clear}
            className="rounded border border-charcoal/20 px-3 py-2 text-sm"
          >
            Clear
          </button>
          <button
            type="button"
            onClick={confirm}
            className="rounded bg-sage px-3 py-2 text-sm text-white"
          >
            Confirm polygon
          </button>
        </div>
      </div>
    </div>
  );
}
