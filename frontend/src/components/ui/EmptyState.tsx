import React from 'react';
import { Button } from './Button';
import { LucideIcon } from 'lucide-react';

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ icon: Icon, title, description, actionLabel, onAction }) => (
  <div className="flex flex-col items-center justify-center text-center p-12 bg-white rounded-xl border border-dashed border-sage/30">
    <div className="h-16 w-16 bg-sage-light/20 text-forest-green rounded-full flex items-center justify-center mb-4">
      <Icon size={32} />
    </div>
    <h3 className="text-xl font-heading font-semibold text-forest-green mb-2">{title}</h3>
    <p className="text-charcoal/70 mb-6 max-w-md">{description}</p>
    {actionLabel && onAction && (
      <Button onClick={onAction}>{actionLabel}</Button>
    )}
  </div>
);
