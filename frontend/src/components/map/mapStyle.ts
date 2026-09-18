import mapboxgl from 'mapbox-gl';

const PLACEHOLDER = 'your-mapbox-token';

function configuredToken(): string {
  return String(import.meta.env.VITE_MAPBOX_TOKEN ?? '').trim();
}

export function hasMapboxToken(): boolean {
  const token = configuredToken();
  return token.startsWith('pk.') && !token.includes(PLACEHOLDER);
}

export function applyMapboxToken(): void {
  mapboxgl.accessToken = hasMapboxToken() ? configuredToken() : 'pk.local';
}

/** Mapbox satellite style when a key is set; otherwise Esri imagery (no key). */
export function basemapStyle(): mapboxgl.StyleSpecification | string {
  if (hasMapboxToken()) {
    return 'mapbox://styles/mapbox/satellite-streets-v12';
  }
  return {
    version: 8,
    sources: {
      satellite: {
        type: 'raster',
        tiles: [
          'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        ],
        tileSize: 256,
        attribution: 'Tiles © Esri',
        maxzoom: 19,
      },
    },
    layers: [{ id: 'satellite', type: 'raster', source: 'satellite' }],
  };
}
