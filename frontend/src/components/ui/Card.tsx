import React from 'react';
import { cn } from './Button';

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => (
  <div className={cn("bg-white rounded-xl shadow-sm hover:shadow-md smooth-transition p-6 border border-sage-light/20", className)} {...props}>
    {children}
  </div>
);
