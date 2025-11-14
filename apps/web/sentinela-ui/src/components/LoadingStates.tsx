import { ReactNode } from 'react';

export const Skeleton = () => (
  <div className="animate-pulse">
    <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
    <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
    <div className="h-4 bg-gray-200 rounded w-5/6"></div>
  </div>
);

export const TableSkeleton = ({ rows = 5 }: { rows?: number }) => (
  <div className="space-y-4">
    {[...Array(rows)].map((_, i) => (
      <div key={i} className="animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-2/3"></div>
      </div>
    ))}
  </div>
);

export const CardSkeleton = () => (
  <div className="animate-pulse bg-white rounded-lg shadow-sm border border-gray-200 p-4">
    <div className="h-6 bg-gray-200 rounded w-3/4 mb-3"></div>
    <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
    <div className="h-4 bg-gray-200 rounded w-5/6 mb-3"></div>
    <div className="flex gap-2">
      <div className="h-6 bg-gray-200 rounded w-16"></div>
      <div className="h-6 bg-gray-200 rounded w-20"></div>
    </div>
  </div>
);

export const GridSkeleton = ({ cols = 3, rows = 2 }: { cols?: number; rows?: number }) => (
  <div className={`grid grid-cols-1 md:grid-cols-${cols} gap-4`}>
    {[...Array(cols * rows)].map((_, i) => (
      <CardSkeleton key={i} />
    ))}
  </div>
);

export const Spinner = ({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-8 w-8'
  };

  return (
    <svg
      className={`animate-spin ${sizeClasses[size]} text-indigo-600`}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      ></circle>
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
  );
};

interface LoadingButtonProps {
  loading: boolean;
  children: ReactNode;
  disabled?: boolean;
  className?: string;
  [key: string]: any;
}

export const LoadingButton = ({
  loading,
  children,
  disabled = false,
  className = '',
  ...props
}: LoadingButtonProps) => (
  <button
    disabled={loading || disabled}
    className={`${className} disabled:opacity-50 disabled:cursor-not-allowed`}
    {...props}
  >
    {loading ? <Spinner size="sm" /> : children}
  </button>
);

export const PageLoader = () => (
  <div className="flex justify-center items-center h-64">
    <Spinner size="lg" />
  </div>
);

export const InlineLoader = () => (
  <div className="flex justify-center items-center py-8">
    <Spinner size="md" />
  </div>
);