interface PolygonThumbProps {
  geojson?: GeoJSON.Polygon | GeoJSON.MultiPolygon | GeoJSON.Geometry | null;
  className?: string;
}

function ringOf(geojson?: PolygonThumbProps['geojson']): number[][] {
  if (
    !geojson ||
    geojson.type !== 'Polygon' ||
    !geojson.coordinates?.[0]?.length
  ) {
    return [];
  }
  return geojson.coordinates[0];
}

export function PolygonThumb({ geojson, className }: PolygonThumbProps) {
  const ring = ringOf(geojson);
  if (ring.length < 3) {
    return (
      <div
        className={`flex h-32 items-center justify-center rounded-lg bg-sage-light/20 text-xs text-charcoal/50 ${className ?? ''}`}
      >
        No boundary preview
      </div>
    );
  }

  const lons = ring.map((point) => point[0]);
  const lats = ring.map((point) => point[1]);
  const minX = Math.min(...lons);
  const maxX = Math.max(...lons);
  const minY = Math.min(...lats);
  const maxY = Math.max(...lats);
  const pad = 8;
  const width = 120;
  const height = 80;
  const spanX = maxX - minX || 1;
  const spanY = maxY - minY || 1;
  const points = ring
    .map(([lon, lat]) => {
      const x = pad + ((lon - minX) / spanX) * (width - pad * 2);
      const y = pad + ((maxY - lat) / spanY) * (height - pad * 2);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(' ');

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      className={`h-32 w-full rounded-lg bg-[#1b4332] ${className ?? ''}`}
      aria-hidden
    >
      <polygon
        points={points}
        fill="#95d5b2"
        fillOpacity="0.55"
        stroke="#d8f3dc"
        strokeWidth="1.5"
      />
    </svg>
  );
}
