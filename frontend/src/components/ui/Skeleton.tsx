import React from 'react';
import { cn } from './Button';

export const Skeleton: React.FC<{ className?: string }> = ({ className }) => (
  <div className={cn("skeleton rounded-lg", className)} />
);
