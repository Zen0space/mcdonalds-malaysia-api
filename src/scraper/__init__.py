"""
McDonald's Malaysia Web Scraper Package - Production Ready
"""

from .mcdonald_scraper import McDonaldMalaysiaScraper
from .base_scraper import BaseScraper

__version__ = "1.0.0"  # Production release
__author__ = "McDonald's Scraper Project"

# Export main production scraper
__all__ = ["McDonaldMalaysiaScraper", "BaseScraper"] 