#!/usr/bin/env python3
"""
Base Scraper Class - Phase 2: Basic Scraper
Provides common functionality for web scraping operations.
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime

class BaseScraper(ABC):
    """Abstract base class for web scrapers."""
    
    def __init__(self, base_url: str, delay: float = 1.0):
        """
        Initialize the base scraper.
        
        Args:
            base_url: The base URL for the website
            delay: Delay between requests in seconds (default: 1.0)
        """
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.logger = self._setup_logging()
        
        # Set realistic headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self.logger.info(f"Initialized {self.__class__.__name__} for {base_url}")
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the scraper."""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        
        # Create console handler if not already exists
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def get_page(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        """
        Fetch a web page and return BeautifulSoup object.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            self.logger.info(f"Fetching: {url}")
            
            # Add delay to be respectful
            time.sleep(self.delay)
            
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            self.logger.info(f"✅ Successfully fetched {url} (Status: {response.status_code})")
            self.logger.info(f"📏 Page size: {len(response.text):,} characters")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
            
        except requests.RequestException as e:
            self.logger.error(f"❌ Error fetching {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error parsing {url}: {e}")
            return None
    
    def find_elements_by_class(self, soup: BeautifulSoup, tag: str, class_name: str) -> List[Any]:
        """
        Find elements by tag and class name.
        
        Args:
            soup: BeautifulSoup object
            tag: HTML tag name
            class_name: CSS class name
            
        Returns:
            List of found elements
        """
        elements = soup.find_all(tag, class_=class_name)
        self.logger.debug(f"Found {len(elements)} elements with tag '{tag}' and class '{class_name}'")
        return elements
    
    def find_element_by_id(self, soup: BeautifulSoup, element_id: str) -> Optional[Any]:
        """
        Find element by ID.
        
        Args:
            soup: BeautifulSoup object
            element_id: Element ID
            
        Returns:
            Found element or None
        """
        element = soup.find(id=element_id)
        if element:
            self.logger.debug(f"Found element with ID '{element_id}'")
        else:
            self.logger.warning(f"Element with ID '{element_id}' not found")
        return element
    
    def extract_text_safely(self, element: Any, default: str = "") -> str:
        """
        Safely extract text from an element.
        
        Args:
            element: BeautifulSoup element
            default: Default value if extraction fails
            
        Returns:
            Extracted text or default value
        """
        try:
            if element:
                return element.get_text(strip=True)
            return default
        except Exception as e:
            self.logger.warning(f"Error extracting text: {e}")
            return default
    
    def extract_attribute_safely(self, element: Any, attribute: str, default: str = "") -> str:
        """
        Safely extract attribute from an element.
        
        Args:
            element: BeautifulSoup element
            attribute: Attribute name
            default: Default value if extraction fails
            
        Returns:
            Attribute value or default value
        """
        try:
            if element:
                return element.get(attribute, default)
            return default
        except Exception as e:
            self.logger.warning(f"Error extracting attribute '{attribute}': {e}")
            return default
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Main scraping method to be implemented by subclasses.
        
        Returns:
            List of scraped data dictionaries
        """
        pass
    
    def get_scraping_stats(self) -> Dict[str, Any]:
        """
        Get basic scraping statistics.
        
        Returns:
            Dictionary with scraping stats
        """
        return {
            'scraper_class': self.__class__.__name__,
            'base_url': self.base_url,
            'delay': self.delay,
            'timestamp': datetime.now().isoformat()
        } 