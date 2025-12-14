"""
Enhanced logging configuration for BudgetIQ backend
"""
import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Configure logging
log_filename = os.path.join(LOGS_DIR, f'budgetiq_{datetime.now().strftime("%Y%m%d")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_request(method, path, status_code):
    """Log API requests"""
    logger.info(f"{method} {path} - Status: {status_code}")

def log_error(error_type, error_message, context=None):
    """Log errors with context"""
    context_str = f" - Context: {context}" if context else ""
    logger.error(f"{error_type}: {error_message}{context_str}")

def log_info(message):
    """Log info messages"""
    logger.info(message)
