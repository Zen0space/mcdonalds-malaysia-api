'use client'

import { memo } from 'react'

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large'
  message?: string
  className?: string
}

/**
 * Reusable loading spinner component with customizable size and message.
 * Features McDonald's brand colors and smooth animations.
 * Optimized with React.memo for performance.
 * 
 * @param {LoadingSpinnerProps} props - Component props
 * @param {'small' | 'medium' | 'large'} props.size - Size variant of the spinner
 * @param {string} props.message - Optional loading message to display
 * @param {string} props.className - Additional CSS classes
 * @returns {JSX.Element} Loading spinner component
 * 
 * @example
 * ```tsx
 * <LoadingSpinner size="large" message="Loading outlets..." />
 * ```
 */
const LoadingSpinner = memo(function LoadingSpinner({ 
  size = 'medium', 
  message = 'Loading...', 
  className = '' 
}: LoadingSpinnerProps) {
  const sizeClasses = {
    small: 'w-4 h-4',
    medium: 'w-8 h-8',
    large: 'w-12 h-12'
  }

  return (
    <div className={`loading-spinner ${className}`}>
      <div className={`spinner ${sizeClasses[size]}`}></div>
      {message && <p className="loading-message">{message}</p>}
      <style jsx>{`
        .loading-spinner {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }
        .spinner {
          border: 3px solid #f3f3f3;
          border-top: 3px solid #dc2626;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        .loading-message {
          margin-top: 12px;
          color: #6c757d;
          font-size: 14px;
          text-align: center;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
})

export default LoadingSpinner 