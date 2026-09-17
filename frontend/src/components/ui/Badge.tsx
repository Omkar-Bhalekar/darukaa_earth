import React from 'react';
import { cn } from './Button';

export const Badge: React.FC<{ type: 'carbon' | 'biodiversity'; className?: string }> = ({ type, className }) => {
  const isCarbon = type === 'carbon';
  return (
    <span className={cn(
      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
      isCarbon ? "bg-forest-green/10 text-forest-green" : "bg-sand-warm/20 text-earth-brown",
      className
    )}>
      {isCarbon ? 'Carbon' : 'Biodiversity'}
    </span>
  );
};
