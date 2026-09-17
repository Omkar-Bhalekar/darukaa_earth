import { useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN ?? '';

interface MapViewProps {
  geojson?: GeoJSON.FeatureCollection | GeoJSON.Feature | GeoJSON.Geometry;
  onPolygonClick?: (id: string) => void;
  className?: string;
  center?: [number, number];
  zoom?: number;
}

export function MapView({ geojson, onPolygonClick, className, center = [0, 20], zoom = 1.5 }: MapViewProps) {
  const container = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map>();
  const currentGeojson = useRef<GeoJSON.FeatureCollection | GeoJSON.Feature | GeoJSON.Geometry>(geojson ?? { type: 'FeatureCollection', features: [] });
  currentGeojson.current = geojson ?? { type: 'FeatureCollection', features: [] };

  useEffect(() => {
    if (!container.current || map.current) return;
    const instance = new mapboxgl.Map({ container: container.current, style: 'mapbox://styles/mapbox/satellite-streets-v12', center, zoom });
    map.current = instance;
    instance.on('load', () => {
      instance.addSource('sites', { type: 'geojson', data: currentGeojson.current });
      instance.addLayer({ id: 'sites-fill', type: 'fill', source: 'sites', paint: { 'fill-color': ['coalesce', ['get', 'color'], '#52796F'], 'fill-opacity': 0.5 } });
      instance.addLayer({ id: 'sites-outline', type: 'line', source: 'sites', paint: { 'line-color': '#FEFAE0', 'line-width': 2 } });
      instance.on('click', 'sites-fill', (event) => {
        const id = event.features?.[0]?.properties?.id;
        if (id) onPolygonClick?.(id);
      });
    });
    return () => { instance.remove(); map.current = undefined; };
  // The map is intentionally initialized once; subsequent geometry updates use the effect below.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const instance = map.current;
    if (!instance || !instance.isStyleLoaded() || !instance.getSource('sites')) return;
    (instance.getSource('sites') as mapboxgl.GeoJSONSource).setData(geojson ?? { type: 'FeatureCollection', features: [] });
  }, [geojson]);

  return <div ref={container} className={`map-container ${className ?? ''}`} aria-label="Interactive site map" />;
}
