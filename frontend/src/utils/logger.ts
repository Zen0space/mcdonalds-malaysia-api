/**
 * Logger utility for production-ready logging with environment-aware output.
 * Provides structured logging with different levels and development/production modes.
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error'

/**
 * Logger class providing structured logging functionality.
 * Automatically detects environment and adjusts logging behavior.
 */
class Logger {
  private isDevelopment: boolean

  constructor() {
    this.isDevelopment = process.env.NODE_ENV === 'development'
  }

  /**
   * Internal logging method that handles environment-specific output.
   * 
   * @private
   * @param {LogLevel} level - Log level
   * @param {string} message - Log message
   * @param {unknown} data - Optional data to log
   */
  private log(level: LogLevel, message: string, data?: unknown): void {
    // In development, log to console
    if (this.isDevelopment) {
      const consoleMethod = level === 'debug' ? 'log' : level
      if (data) {
        // eslint-disable-next-line no-console
        console[consoleMethod](`[${level.toUpperCase()}] ${message}`, data)
      } else {
        // eslint-disable-next-line no-console
        console[consoleMethod](`[${level.toUpperCase()}] ${message}`)
      }
    }

    // In production, you could send to a logging service
    // Example: this.sendToLoggingService({ level, message, timestamp: new Date().toISOString(), data })
  }

  /**
   * Log debug message (development only).
   * 
   * @param {string} message - Debug message
   * @param {unknown} data - Optional data to log
   */
  debug(message: string, data?: unknown): void {
    this.log('debug', message, data)
  }

  /**
   * Log informational message.
   * 
   * @param {string} message - Info message
   * @param {unknown} data - Optional data to log
   */
  info(message: string, data?: unknown): void {
    this.log('info', message, data)
  }

  /**
   * Log warning message.
   * 
   * @param {string} message - Warning message
   * @param {unknown} data - Optional data to log
   */
  warn(message: string, data?: unknown): void {
    this.log('warn', message, data)
  }

  /**
   * Log error message.
   * 
   * @param {string} message - Error message
   * @param {unknown} data - Optional data to log
   */
  error(message: string, data?: unknown): void {
    this.log('error', message, data)
  }

  /**
   * Start performance timer (development only).
   * 
   * @param {string} label - Timer label
   */
  time(label: string): void {
    if (this.isDevelopment) {
      // eslint-disable-next-line no-console
      console.time(label)
    }
  }

  /**
   * End performance timer and log duration (development only).
   * 
   * @param {string} label - Timer label
   */
  timeEnd(label: string): void {
    if (this.isDevelopment) {
      // eslint-disable-next-line no-console
      console.timeEnd(label)
    }
  }
}

/**
 * Default logger instance for application use.
 * Automatically configured based on environment.
 */
export const logger = new Logger()

/**
 * Default export of the logger instance.
 */
export default logger 