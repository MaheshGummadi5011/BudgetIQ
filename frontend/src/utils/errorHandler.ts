/**
 * Error handling utility for API calls and general error management
 */

export interface ApiError {
  message: string;
  status?: number;
  details?: string;
}

/**
 * Handle API errors gracefully
 */
export const handleApiError = (error: unknown): ApiError => {
  if (error instanceof Error) {
    return {
      message: error.message,
      details: error.stack
    };
  }

  if (typeof error === 'object' && error !== null) {
    const errorObj = error as any;
    
    // Handle Axios errors
    if (errorObj.response) {
      return {
        message: errorObj.response.data?.message || errorObj.response.statusText,
        status: errorObj.response.status,
        details: JSON.stringify(errorObj.response.data)
      };
    }

    // Handle other object errors
    if (errorObj.message) {
      return {
        message: errorObj.message,
        details: JSON.stringify(errorObj)
      };
    }
  }

  return {
    message: 'An unexpected error occurred',
    details: String(error)
  };
};

/**
 * User-friendly error messages
 */
export const getErrorMessage = (error: ApiError): string => {
  switch (error.status) {
    case 400:
      return 'Invalid request. Please check your input.';
    case 401:
      return 'Unauthorized. Please log in again.';
    case 403:
      return 'Access denied.';
    case 404:
      return 'Resource not found.';
    case 500:
      return 'Server error. Please try again later.';
    case 503:
      return 'Service temporarily unavailable.';
    default:
      return error.message || 'Something went wrong. Please try again.';
  }
};

/**
 * Retry logic for failed requests
 */
export const retryRequest = async <T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  delayMs: number = 1000
): Promise<T> => {
  let lastError: Error;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      
      if (attempt < maxRetries - 1) {
        const delay = delayMs * Math.pow(2, attempt); // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  throw lastError!;
};
