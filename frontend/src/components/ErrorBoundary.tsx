'use client'

import React, { Component, ErrorInfo, ReactNode } from 'react'
import { logger } from '../utils/logger'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
  errorInfo?: ErrorInfo
}

/**
 * Error boundary component that catches JavaScript errors anywhere in the child component tree.
 * Provides a fallback UI and logs errors for debugging.
 * Implements React's error boundary pattern for graceful error handling.
 * 
 * @class ErrorBoundary
 * @extends {Component<Props, State>}
 * 
 * @example
 * ```tsx
 * <ErrorBoundary fallback={<div>Custom error UI</div>}>
 *   <MyComponent />
 * </ErrorBoundary>
 * ```
 */
export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  /**
   * Static method called when an error is thrown in a child component.
   * Updates state to trigger error UI rendering.
   * 
   * @param {Error} error - The error that was thrown
   * @returns {State} New state with error information
   */
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  /**
   * Lifecycle method called when an error is caught.
   * Logs the error and updates component state with error details.
   * 
   * @param {Error} error - The error that was thrown
   * @param {ErrorInfo} errorInfo - Additional error information from React
   */
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    logger.error('Error caught by boundary:', { error, errorInfo })
    this.setState({ errorInfo })
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <div className="error-boundary">
          <div className="error-content">
            <h2>🚨 Something went wrong</h2>
            <p>We&apos;re sorry, but something unexpected happened.</p>
            <details style={{ whiteSpace: 'pre-wrap' }}>
              <summary>Error Details</summary>
              <p><strong>Error:</strong> {this.state.error?.message}</p>
              <p><strong>Stack:</strong> {this.state.error?.stack}</p>
              {this.state.errorInfo && (
                <p><strong>Component Stack:</strong> {this.state.errorInfo.componentStack}</p>
              )}
            </details>
            <button
              onClick={() => window.location.reload()}
              className="retry-button"
            >
              Reload Page
            </button>
          </div>
          <style jsx>{`
            .error-boundary {
              display: flex;
              align-items: center;
              justify-content: center;
              min-height: 400px;
              padding: 20px;
              background: #f8f9fa;
              border: 1px solid #dee2e6;
              border-radius: 8px;
              margin: 20px;
            }
            .error-content {
              text-align: center;
              max-width: 600px;
            }
            .error-content h2 {
              color: #dc3545;
              margin-bottom: 16px;
            }
            .error-content p {
              color: #6c757d;
              margin-bottom: 16px;
            }
            .error-content details {
              text-align: left;
              background: #fff;
              padding: 16px;
              border-radius: 4px;
              border: 1px solid #dee2e6;
              margin: 16px 0;
            }
            .retry-button {
              background: #007bff;
              color: white;
              border: none;
              padding: 12px 24px;
              border-radius: 4px;
              cursor: pointer;
              font-size: 16px;
            }
            .retry-button:hover {
              background: #0056b3;
            }
          `}</style>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary 