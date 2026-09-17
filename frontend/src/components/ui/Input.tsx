import React from 'react';
import { cn } from './Button';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, ...props }, ref) => (
    <div className="w-full flex flex-col gap-1.5">
      {label && <label className="text-sm font-medium text-forest-green">{label}</label>}
      <input
        ref={ref}
        className={cn(
          "w-full rounded-lg border border-sage/30 px-3 py-2 bg-off-white text-charcoal placeholder:text-charcoal/50",
          "focus:outline-none focus:ring-2 focus:ring-sage focus:border-transparent smooth-transition",
          error && "border-earth-brown focus:ring-earth-brown",
          className
        )}
        {...props}
      />
      {error && <span className="text-xs text-earth-brown mt-1">{error}</span>}
    </div>
  )
);
Input.displayName = 'Input';
