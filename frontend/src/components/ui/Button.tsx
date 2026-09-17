import React from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', isLoading, children, ...props }, ref) => {
    const variants = {
      primary: 'bg-forest-green text-off-white hover:bg-forest-green/90',
      secondary: 'bg-sage text-off-white hover:bg-sage/90',
      outline: 'border-2 border-forest-green text-forest-green hover:bg-forest-green/10',
      danger: 'bg-earth-brown text-off-white hover:bg-earth-brown/90',
    };
    const sizes = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg',
    };

    return (
      <button
        ref={ref}
        disabled={isLoading || props.disabled}
        className={cn(
          'inline-flex items-center justify-center rounded-lg font-medium smooth-transition disabled:opacity-50',
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      >
        {isLoading ? <span className="animate-spin mr-2 border-2 border-current border-t-transparent rounded-full h-4 w-4" /> : null}
        {children}
      </button>
    );
  }
);
Button.displayName = 'Button';
