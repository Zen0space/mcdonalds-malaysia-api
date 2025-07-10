#!/usr/bin/env python3
"""
McDonald's Malaysia Production Scraper
Production-ready scraper with database integration and advanced deduplication.
"""

import asyncio
import json
import os
import re
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

try:
    # Import database operations
    from ..database.operations import OutletDatabase
    from ..database.models import Outlet, validate_outlet_data
    # Import geocoding module
    from ..geocoding import McDonaldGeocoder
except ImportError:
    # For direct execution
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from database.operations import OutletDatabase
    from database.models import Outlet, validate_outlet_data
    from geocoding import McDonaldGeocoder

class McDonaldMalaysiaScraper:
    """Clean, optimized McDonald's Malaysia scraper - no inheritance, no redundancy."""
    
    def __init__(self, 
                 headless: bool = True, 
                 delay: float = 2.0,
                 debug: bool = False,
                 database_integration: bool = True):
        """Initialize optimized scraper."""
        self.headless = headless
        self.delay = delay
        self.debug = debug
        self.database_integration = database_integration
        
        # URLs
        self.base_url = "https://www.mcdonalds.com.my"
        self.locate_url = f"{self.base_url}/locate-us"
        
        # Browser instances
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # Database
        self.db_operations = None
        
        # Geocoding
        self.geocoder = None
        
        # Deduplication - track processed outlets to prevent redundancy
        self.processed_outlets: Set[str] = set()
        
        # Stats
        self.stats = {
            'session_id': f"mcd_optimized_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'start_time': None,
            'end_time': None,
            'total_runtime': 0,
            'total_found': 0,
            'unique_outlets': 0,
            'duplicates_skipped': 0,
            'successfully_saved': 0,
            'database_errors': 0,
            'method_used': 'optimized_single_pass_with_geocoding',
            # Geocoding stats
            'geocoding_enabled': True,
            'geocoding_successful': 0,
            'geocoding_failed': 0,
            'geocoding_time': 0,
            # Waze link stats
            'waze_links_extracted': 0,
            'waze_links_matched': 0,
            'waze_coordinates_extracted': 0
        }
        
        # Setup logging
        self._setup_logging()
        
        # Initialize database
        if self.database_integration:
            self._initialize_database()
        
        # Initialize geocoding
        self._initialize_geocoding()
    
    def _setup_logging(self):
        """Setup clean logging."""
        os.makedirs('logs', exist_ok=True)
        log_filename = f"logs/optimized_scraper_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - OPTIMIZED - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🚀 Optimized scraper initialized - Session: {self.stats['session_id']}")
    
    def _initialize_database(self):
        """Initialize database connection."""
        try:
            self.db_operations = OutletDatabase()
            self.logger.info("✅ Database connection initialized")
        except Exception as e:
            self.logger.error(f"❌ Database initialization failed: {e}")
            self.database_integration = False
    
    def _initialize_geocoding(self):
        """Initialize geocoding service."""
        try:
            self.geocoder = McDonaldGeocoder()
            self.logger.info("✅ Geocoding service initialized")
        except Exception as e:
            self.logger.error(f"❌ Geocoding initialization failed: {e}")
            self.stats['geocoding_enabled'] = False
            self.geocoder = None
    
    async def scrape_outlets(self, target_state: str = "Kuala Lumpur") -> Dict[str, Any]:
        """
        Main optimized scraping method - single pass, no redundancy.
        """
        self.stats['start_time'] = datetime.now()
        
        self.logger.info("🚀 Starting OPTIMIZED McDonald's Malaysia Scraping")
        self.logger.info(f"🎯 Target: {target_state}")
        self.logger.info("⚡ Method: Single-pass optimized extraction")
        
        outlets = []
        
        try:
            # Single-pass scraping
            outlets = await self._single_pass_scrape(target_state)
            
            # Single-pass database integration
            if self.database_integration and outlets:
                await self._save_to_database(outlets)
            
            # Generate results
            await self._generate_report(outlets)
            
        except Exception as e:
            self.logger.error(f"❌ Optimized scraping failed: {e}")
        
        finally:
            # Cleanup
            await self._cleanup()
            
            self.stats['end_time'] = datetime.now()
            if self.stats['start_time']:
                self.stats['total_runtime'] = (
                    self.stats['end_time'] - self.stats['start_time']
                ).total_seconds()
        
        return {
            'outlets': outlets,
            'statistics': self.stats,
            'session_id': self.stats['session_id']
        }
    
    async def _single_pass_scrape(self, target_state: str) -> List[Dict[str, Any]]:
        """Single-pass scraping - no redundancy."""
        
        # Step 1: Initialize browser
        await self._init_browser()
        
        # Step 2: Navigate and setup
        await self._navigate_and_setup()
        
        # Step 3: Apply filter
        await self._apply_filter(target_state)
        
        # Step 4: Extract all data in ONE pass
        outlets = await self._extract_all_data()
        
        return outlets
    
    async def _init_browser(self):
        """Initialize browser efficiently."""
        self.logger.info("🌐 Initializing Brave browser...")
        
        playwright = await async_playwright().start()
        
        # Try to find Brave browser executable
        brave_paths = [
            "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",  # Windows
            "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",  # Windows x86
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",  # macOS
            "/usr/bin/brave-browser",  # Linux
            "/snap/bin/brave",  # Linux Snap
            "/opt/brave.com/brave/brave-browser"  # Linux alternative
        ]
        
        brave_path = None
        for path in brave_paths:
            if os.path.exists(path):
                brave_path = path
                break
        
        if brave_path:
            self.logger.info(f"🦁 Using Brave browser: {brave_path}")
            self.browser = await playwright.chromium.launch(
                executable_path=brave_path,
                headless=self.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-blink-features=AutomationControlled']
            )
        else:
            self.logger.warning("⚠️ Brave browser not found, falling back to Chromium")
            self.browser = await playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
        
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        self.page = await self.context.new_page()
        
        # Set up navigation interception to capture Waze URLs
        await self._setup_navigation_interception()
        
        self.logger.info("✅ Browser ready")
    
    async def _setup_navigation_interception(self):
        """Set up navigation interception to capture Waze URLs."""
        self.captured_urls = []
        
        async def handle_route(route):
            url = route.request.url
            if 'waze.com' in url or 'waze://' in url:
                if self.debug:
                    self.logger.info(f"🎯 Captured Waze URL: {url}")
                self.captured_urls.append(url)
            
            # Continue with the request
            await route.continue_()
                
        await self.page.route('**/*', handle_route)
    
    async def _navigate_and_setup(self):
        """Navigate and wait for page to be ready."""
        self.logger.info(f"📍 Loading {self.locate_url}")
        
        try:
            await self.page.goto(self.locate_url, wait_until='load', timeout=60000)
        except Exception as e:
            self.logger.warning(f"⚠️ Navigation timeout, trying with domcontentloaded: {e}")
            await self.page.goto(self.locate_url, wait_until='domcontentloaded', timeout=30000)
        
        # Wait for Vue.js app and form elements
        await self.page.wait_for_selector('#app', timeout=15000)
        await self.page.wait_for_selector('#states', timeout=15000)
        await self.page.wait_for_selector('#search-now', timeout=15000)
        
        await asyncio.sleep(self.delay)
        self.logger.info("✅ Page ready")
    
    async def _apply_filter(self, target_state: str):
        """Apply state filter efficiently."""
        self.logger.info(f"🎯 Filtering for {target_state}")
        
        # Select state
        await self.page.select_option('#states', value=target_state)
        await asyncio.sleep(1)
        
        # Click search
        await self.page.click('#search-now')
        await asyncio.sleep(self.delay * 2)  # Wait longer for results to load
        
        # Wait for results container (more flexible)
        try:
            await self.page.wait_for_selector('#results', timeout=20000)
            self.logger.info("✅ Results container loaded")
        except:
            # Try alternative result selectors
            try:
                await self.page.wait_for_function(
                    "document.querySelector('#results') && document.querySelector('#results').children.length > 0",
                    timeout=15000
                )
                self.logger.info("✅ Results populated")
            except:
                self.logger.warning("⚠️ Results container not found, proceeding anyway")
        
        await asyncio.sleep(3)  # Allow all results to fully load
        self.logger.info("✅ Filter applied, waiting for data")
    
    async def _extract_all_data(self) -> List[Dict[str, Any]]:
        """Extract ALL outlet data using sequential processing."""
        self.logger.info("📊 Extracting outlet data (sequential approach)...")
        
        # Try the new sequential approach first
        outlets = await self._extract_outlets_sequentially()
        
        if outlets:
            self.logger.info(f"✅ Sequential extraction successful: {len(outlets)} outlets")
            return outlets
        
        # Fallback to the old text-splitting approach if sequential fails
        self.logger.warning("⚠️ Sequential extraction failed, falling back to text splitting...")
        
        outlets = []
        
        # Try to get the results container content
        try:
            results_container = await self.page.query_selector('#results')
            if results_container:
                results_html = await results_container.inner_html()
                self.logger.info(f"📋 Results container HTML length: {len(results_html)} characters")
        except:
            pass
        
        # Get all potential outlet elements with more comprehensive selectors
        outlet_selectors = [
            # Primary selectors
            '.restaurant', '.outlet', '.store-item', '.location-item',
            # Container-based selectors
            '#results > div', '#results > *', 
            # Class-based selectors  
            '[class*="restaurant"]', '[class*="outlet"]', '[class*="store"]', '[class*="location"]',
            # Generic content selectors
            'div[style*="margin"]', 'div[style*="padding"]',
            # Vue component selectors
            '[data-v-]'
        ]
        
        outlet_elements = []
        selected_selector = None
        
        for selector in outlet_selectors:
            try:
                elements = await self.page.query_selector_all(selector)
                if elements:
                    outlet_elements.extend(elements)
                    selected_selector = selector
                    self.logger.info(f"🔍 Selector '{selector}': Found {len(elements)} elements")
                    break  # Use first working selector
            except:
                continue
        
        if self.debug and selected_selector:
            self.logger.info(f"🎯 Using selector: {selected_selector}")
        
        # Remove duplicates while preserving order - IMPROVED DEDUPLICATION
        seen_elements = set()
        unique_elements = []
        
        for i, element in enumerate(outlet_elements):
            try:
                # Use element's outer HTML hash for better deduplication
                element_html = await element.outer_html()
                element_hash = hash(element_html[:500])  # Use first 500 chars to create hash
                
                if element_hash not in seen_elements:
                    seen_elements.add(element_hash)
                    unique_elements.append(element)
                    if self.debug:
                        self.logger.info(f"  ✅ Element {i+1}: Added (hash: {element_hash})")
                else:
                    if self.debug:
                        self.logger.info(f"  🔄 Element {i+1}: DUPLICATE ELEMENT SKIPPED (hash: {element_hash})")
            except:
                # Fallback to string representation
                element_handle = str(element)
                if element_handle not in seen_elements:
                    seen_elements.add(element_handle)
                    unique_elements.append(element)
        
        outlet_elements = unique_elements
        self.logger.info(f"🔍 Found {len(outlet_elements)} unique potential outlet elements")
        
        # Track outlet processing for debugging
        element_outlet_count = 0
        
        for i, element in enumerate(outlet_elements):
            try:
                # Get text content to check if this element contains multiple outlets
                text_content = await element.text_content()
                
                if not text_content or len(text_content.strip()) < 10:
                    continue
                
                if self.debug:
                    self.logger.info(f"\n🔍 PROCESSING ELEMENT {i+1}:")
                    self.logger.info(f"  📝 Text length: {len(text_content)} characters")
                    self.logger.info(f"  📝 Text preview: {text_content[:200]}...")
                
                # Check if this element contains multiple outlets
                outlet_blocks = self._split_multiple_outlets(text_content)
                
                if self.debug:
                    self.logger.info(f"  🔪 Split into {len(outlet_blocks)} outlet blocks")
                
                if len(outlet_blocks) > 1:
                    self.logger.info(f"🔍 Element {i+1} contains {len(outlet_blocks)} outlet blocks - parsing multiple outlets")
                    
                    # Process each outlet block separately
                    for block_idx, outlet_block in enumerate(outlet_blocks):
                        try:
                            if self.debug:
                                self.logger.info(f"    📋 Processing block {block_idx+1}:")
                                self.logger.info(f"      📝 Block text: {outlet_block[:150]}...")
                            
                            outlet_data = self._extract_outlet_from_text(outlet_block)
                            
                            if outlet_data and self._is_valid_outlet(outlet_data):
                                                    # Skip old Waze link mapping - using sequential approach now  
                    # outlet_data = self._add_waze_link_from_map(outlet_data, waze_links_map)
                                
                                # Add geocoding to outlet data (this will use Waze link coordinates if available)
                                outlet_data = await self._add_geocoding(outlet_data)
                                
                                # Check for duplicates using name+address combination
                                outlet_key = f"{outlet_data.get('name', '')}-{outlet_data.get('address', '')}"
                                
                                if self.debug:
                                    self.logger.info(f"      🔑 Dedup key: {outlet_key}")
                                
                                if outlet_key not in self.processed_outlets:
                                    self.processed_outlets.add(outlet_key)
                                    outlets.append(outlet_data)
                                    self.stats['unique_outlets'] += 1
                                    element_outlet_count += 1
                                    
                                    # Show geocoding status in log
                                    coords_info = ""
                                    if outlet_data.get('latitude') and outlet_data.get('longitude'):
                                        coords_info = f" 📍 {outlet_data['latitude']:.4f},{outlet_data['longitude']:.4f}"
                                    
                                    self.logger.info(f"      📍 ✅ ADDED: {outlet_data.get('name', 'Unknown')}{coords_info}")
                                else:
                                    self.stats['duplicates_skipped'] += 1
                                    self.logger.info(f"      📍 🔄 DUPLICATE SKIPPED: {outlet_data.get('name', 'Unknown')}")
                                    
                        except Exception as e:
                            if self.debug:
                                self.logger.warning(f"⚠️ Error parsing outlet block {block_idx+1}: {e}")
                else:
                    # Single outlet in this element - use existing logic
                    if self.debug:
                        self.logger.info(f"  📋 Processing as single outlet")
                    
                    outlet_data = await self._extract_complete_outlet_data(element)
                    
                    if outlet_data and self._is_valid_outlet(outlet_data):
                        # Skip old Waze link mapping - using sequential approach now
                        # outlet_data = self._add_waze_link_from_map(outlet_data, waze_links_map)
                        
                        # Add geocoding to outlet data (this will use Waze link coordinates if available)
                        outlet_data = await self._add_geocoding(outlet_data)
                        
                        # Check for duplicates using name+address combination
                        outlet_key = f"{outlet_data.get('name', '')}-{outlet_data.get('address', '')}"
                        
                        if self.debug:
                            self.logger.info(f"    🔑 Dedup key: {outlet_key}")
                        
                        if outlet_key not in self.processed_outlets:
                            self.processed_outlets.add(outlet_key)
                            outlets.append(outlet_data)
                            self.stats['unique_outlets'] += 1
                            element_outlet_count += 1
                            
                            # Show geocoding status in log
                            coords_info = ""
                            if outlet_data.get('latitude') and outlet_data.get('longitude'):
                                coords_info = f" 📍 {outlet_data['latitude']:.4f},{outlet_data['longitude']:.4f}"
                            
                            self.logger.info(f"    📍 ✅ ADDED: {outlet_data.get('name', 'Unknown')}{coords_info}")
                        else:
                            self.stats['duplicates_skipped'] += 1
                            self.logger.info(f"    📍 🔄 DUPLICATE SKIPPED: {outlet_data.get('name', 'Unknown')}")
                
                if self.debug:
                    self.logger.info(f"  📊 Element {i+1} contributed {element_outlet_count - (self.stats['unique_outlets'] - element_outlet_count)} outlets\n")
                        
            except Exception as e:
                if self.debug:
                    self.logger.warning(f"⚠️ Error parsing element {i+1}: {e}")
        
        self.stats['total_found'] = len(outlets)
        self.logger.info(f"✅ Extracted {len(outlets)} unique outlets (skipped {self.stats['duplicates_skipped']} duplicates)")
        
        # Debug summary
        if self.debug:
            self.logger.info(f"\n📊 EXTRACTION SUMMARY:")
            self.logger.info(f"  🔍 Elements processed: {len(outlet_elements)}")
            self.logger.info(f"  📍 Unique outlets: {self.stats['unique_outlets']}")
            self.logger.info(f"  🔄 Duplicates skipped: {self.stats['duplicates_skipped']}")
            self.logger.info(f"  📋 Processed outlets set size: {len(self.processed_outlets)}")
        
        return outlets
    
    async def _extract_outlets_sequentially(self) -> List[Dict[str, Any]]:
        """Extract outlets sequentially - one container at a time with immediate Waze clicking."""
        self.logger.info("🔄 Starting sequential outlet extraction...")
        
        outlets = []
        
        # Try different selectors to find individual outlet containers
        selectors_to_try = [
            '#results > div > div',  # One level deeper
            '#results .restaurant-item',
            '#results .outlet-item', 
            '#results .location-item',
            '#results [class*="restaurant"]',
            '#results [class*="outlet"]',
            '#results [data-v-] > div',  # Vue components
            '#results > div > *',  # Any direct children of results > div
        ]
        
        outlet_containers = []
        selected_selector = None
        
        for selector in selectors_to_try:
            try:
                containers = await self.page.query_selector_all(selector)
                if containers and len(containers) > 10:  # Should find ~50 containers
                    outlet_containers = containers
                    selected_selector = selector
                    self.logger.info(f"✅ Found {len(containers)} individual containers with selector: {selector}")
                    break
            except:
                continue
        
        if not outlet_containers:
            self.logger.warning("❌ Could not find individual outlet containers, falling back to text splitting")
            return []
        
        self.logger.info(f"🎯 Processing {len(outlet_containers)} outlets sequentially...")
        
        # Wait for all Waze buttons to be ready before starting sequential processing
        self.logger.info("⏳ Ensuring all Waze buttons are ready...")
        try:
            # Wait for at least one Waze button to be present and clickable
            await self.page.wait_for_selector('a:has-text("Waze"), a[href*="waze"], a[href*="navigate"]', timeout=10000)
            
            # Wait for page to be fully interactive (important for first outlet)
            await self.page.wait_for_load_state('networkidle', timeout=15000)
            await asyncio.sleep(5)  # Longer buffer to ensure all buttons are fully interactive
            self.logger.info("✅ Waze buttons ready")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not verify Waze buttons readiness: {e}")
            # Fallback: just wait longer
            await asyncio.sleep(8)
        
        for i, container in enumerate(outlet_containers):
            try:
                self.logger.info(f"\n📍 Processing outlet {i+1}/{len(outlet_containers)}")
                
                # Special handling for first outlet - give it extra time
                if i == 0:
                    self.logger.info("🎯 First outlet - adding extra wait time for stability")
                    await asyncio.sleep(3)
                
                # Extract basic data from this container
                outlet_data = await self._extract_data_from_container(container)
                
                if not outlet_data or not outlet_data.get('name'):
                    self.logger.warning(f"⚠️ Skipping container {i+1} - no valid data")
                    continue
                
                # Find and click Waze button in this specific container
                waze_url = await self._click_waze_in_container(container, outlet_data['name'])
                
                if waze_url:
                    outlet_data['waze_link'] = waze_url
                    self.logger.info(f"✅ {outlet_data['name']}: Got Waze link")
                else:
                    self.logger.warning(f"❌ {outlet_data['name']}: No Waze link")
                
                # Add geocoding
                outlet_data = await self._add_geocoding(outlet_data)
                
                # Check for duplicates
                outlet_key = f"{outlet_data.get('name', '')}-{outlet_data.get('address', '')}"
                
                if outlet_key not in self.processed_outlets:
                    self.processed_outlets.add(outlet_key)
                    outlets.append(outlet_data)
                    self.stats['unique_outlets'] += 1
                    
                    coords_info = ""
                    if outlet_data.get('latitude') and outlet_data.get('longitude'):
                        coords_info = f" 📍 {outlet_data['latitude']:.4f},{outlet_data['longitude']:.4f}"
                    
                    self.logger.info(f"✅ ADDED: {outlet_data.get('name', 'Unknown')}{coords_info}")
                else:
                    self.stats['duplicates_skipped'] += 1
                    self.logger.info(f"🔄 DUPLICATE SKIPPED: {outlet_data.get('name', 'Unknown')}")
                
            except Exception as e:
                self.logger.warning(f"❌ Error processing container {i+1}: {e}")
                continue
        
        self.logger.info(f"🎉 Sequential extraction completed: {len(outlets)} outlets processed")
        return outlets
    
    async def _extract_data_from_container(self, container) -> Optional[Dict[str, Any]]:
        """Extract basic outlet data from a single container."""
        try:
            # Get text content from container
            text_content = await container.text_content()
            inner_html = await container.inner_html()
            
            if not text_content or len(text_content.strip()) < 10:
                return None
            
            # Extract data using existing methods
            outlet_data = {
                'name': self._extract_name(text_content),
                'address': self._extract_address(text_content),
                'operating_hours': self._extract_hours(text_content, inner_html),
                'phone': self._extract_phone(text_content),
                'features': self._extract_features(text_content, inner_html)
            }
            
            return outlet_data
            
        except Exception as e:
            if self.debug:
                self.logger.warning(f"⚠️ Error extracting data from container: {e}")
            return None
    
    async def _click_waze_in_container(self, container, outlet_name: str) -> Optional[str]:
        """Find and click Waze button in this specific container."""
        try:
            # Find Waze button in this container
            waze_button = await container.query_selector('a:has-text("Waze")')
            
            if not waze_button:
                # Try alternative selectors
                waze_selectors = [
                    'a[href*="waze"]',
                    'a[href*="navigate"]', 
                    '.waze-link',
                    '[class*="waze"]'
                ]
                
                for selector in waze_selectors:
                    waze_button = await container.query_selector(selector)
                    if waze_button:
                        break
            
            if not waze_button:
                if self.debug:
                    self.logger.warning(f"❌ No Waze button found in container for {outlet_name}")
                return None
            
            # Clear previous captured URLs
            self.captured_urls = []
            
            # Click the Waze button with extra wait for first outlet
            await waze_button.click()
            
            # Wait longer for URL to be generated (especially important for first outlet)
            await asyncio.sleep(4)  # Increased from 2 to 4 seconds
            
            # Check for captured URLs from navigation interception
            if self.captured_urls:
                captured_url = self.captured_urls[-1]
                if self.debug:
                    self.logger.info(f"🎯 Captured URL: {captured_url}")
                return captured_url
            
            # Check if a new tab opened
            pages = self.context.pages
            if len(pages) > 1:
                new_page = pages[-1]
                url = new_page.url
                await new_page.close()  # Close the new tab immediately
                
                if 'waze.com' in url or 'waze://' in url:
                    if self.debug:
                        self.logger.info(f"🎯 New tab URL: {url}")
                    return url
            
            # Check if current page URL changed
            current_url = self.page.url
            if 'waze.com' in current_url:
                # Navigate back to results
                await self.page.go_back()
                await asyncio.sleep(1)
                if self.debug:
                    self.logger.info(f"🎯 Page navigation URL: {current_url}")
                return current_url
            
        except Exception as e:
            if self.debug:
                self.logger.warning(f"❌ Error clicking Waze for {outlet_name}: {e}")
        
        return None
    
    def _split_multiple_outlets(self, text: str) -> List[str]:
        """Split text content that contains multiple outlet data into individual blocks."""
        # Count McDonald's mentions to detect multiple outlets
        mcd_count = text.lower().count("mcdonald's")
        
        if self.debug:
            self.logger.info(f"    🔍 McDonald's mentions found: {mcd_count}")
        
        if mcd_count <= 1:
            if self.debug:
                self.logger.info(f"    📋 Single outlet detected, returning original text")
            return [text]  # Single outlet
        
        # Split on McDonald's patterns, keeping the McDonald's prefix
        import re
        
        if self.debug:
            self.logger.info(f"    🔪 Attempting to split {mcd_count} outlets...")
        
        # IMPROVED SPLITTING LOGIC - More precise pattern
        # Look for: newline + whitespace + "McDonald's" at start of line
        # This avoids splitting on McDonald's mentions within addresses or descriptions
        split_pattern = r'\n\s*(?=McDonald\'s\s+[A-Z])'
        
        blocks = re.split(split_pattern, text, flags=re.IGNORECASE)
        
        if self.debug:
            self.logger.info(f"    🔪 Primary split resulted in {len(blocks)} blocks")
        
        # Clean and filter blocks - IMPROVED VALIDATION
        clean_blocks = []
        for i, block in enumerate(blocks):
            block = block.strip()
            
            # More strict validation for outlet blocks
            if (block and 
                "mcdonald's" in block.lower() and 
                len(block) > 50 and  # Increased minimum length
                # Must have address-like content (contains "jalan", street names, or Malaysia)
                any(keyword in block.lower() for keyword in ['jalan', 'road', 'street', 'malaysia', 'kuala lumpur', 'kl'])):
                
                clean_blocks.append(block)
                if self.debug:
                    self.logger.info(f"      ✅ Block {i+1}: Valid (length: {len(block)})")
                    # Show outlet name from block
                    lines = block.split('\n')
                    for line in lines[:3]:  # Check first 3 lines for outlet name
                        if "mcdonald's" in line.lower():
                            self.logger.info(f"          📍 Contains: {line.strip()[:80]}...")
                            break
            else:
                if self.debug and len(block) > 10:  # Only log non-empty invalid blocks
                    has_mcdonalds = "mcdonald's" in block.lower()
                    has_address = any(keyword in block.lower() for keyword in ['jalan', 'road', 'street', 'malaysia'])
                    self.logger.info(f"      ❌ Block {i+1}: Invalid (length: {len(block)}, has McDonald's: {has_mcdonalds}, has address: {has_address})")
        
        if len(clean_blocks) > 1:
            if self.debug:
                self.logger.info(f"    ✅ Successfully split into {len(clean_blocks)} valid outlet blocks")
            return clean_blocks
        
        # Fallback: Try splitting on outlet boundary patterns
        if self.debug:
            self.logger.info(f"    🔄 Primary split failed, trying boundary-based splitting...")
        
        # Look for patterns that indicate outlet boundaries:
        # "Waze" followed by whitespace and then "McDonald's"
        boundary_pattern = r'(?<=Waze)\s*\n\s*(?=McDonald\'s)'
        blocks = re.split(boundary_pattern, text, flags=re.IGNORECASE)
        
        if self.debug:
            self.logger.info(f"    🔪 Boundary split resulted in {len(blocks)} blocks")
        
        clean_blocks = []
        for i, block in enumerate(blocks):
            block = block.strip()
            if (block and 
                "mcdonald's" in block.lower() and 
                len(block) > 50 and
                any(keyword in block.lower() for keyword in ['jalan', 'road', 'street', 'malaysia', 'kuala lumpur'])):
                
                clean_blocks.append(block)
                if self.debug:
                    self.logger.info(f"      ✅ Boundary Block {i+1}: Valid (length: {len(block)})")
            else:
                if self.debug and len(block) > 10:
                    self.logger.info(f"      ❌ Boundary Block {i+1}: Invalid")
        
        # Final result - limit to reasonable number of outlets
        final_blocks = clean_blocks if len(clean_blocks) > 1 and len(clean_blocks) <= 100 else [text]
        
        if self.debug:
            self.logger.info(f"    📋 Final result: {len(final_blocks)} blocks")
            
            # Check for potential duplicate outlet names across blocks
            if len(final_blocks) > 1:
                outlet_names = []
                for i, block in enumerate(final_blocks):
                    lines = block.split('\n')
                    for line in lines[:5]:  # Check first 5 lines for outlet name
                        if "mcdonald's" in line.lower():
                            clean_name = line.strip().replace('"', '').replace(',', '')
                            outlet_names.append(clean_name)
                            break
                
                # Check for duplicates in outlet names
                seen_names = set()
                for name in outlet_names:
                    if name in seen_names:
                        self.logger.warning(f"    ⚠️ POTENTIAL DUPLICATE DETECTED: {name}")
                    else:
                        seen_names.add(name)
        
        return final_blocks
    
    async def _extract_dynamic_waze_links(self) -> Dict[str, str]:
        """Extract Waze links by clicking the Waze buttons dynamically."""
        self.logger.info("🔗 Extracting dynamic Waze links...")
        
        waze_links_map = {}
        
        try:
            # Find all outlet containers first (like in the working extract_waze_links.py)
            outlet_containers = await self.page.query_selector_all('#results > div')
            self.logger.info(f"Found {len(outlet_containers)} outlet containers")
            
            # Find all Waze links
            waze_links = await self.page.query_selector_all('a:has-text("Waze")')
            self.logger.info(f"Found {len(waze_links)} Waze links to process")
            
            # Skip container matching - it's broken for single-container layouts
            # Go directly to sequential clicking to get all 50 Waze links
            self.logger.info(f"🎯 Skipping container matching (broken for single container)")
            self.logger.info(f"🎯 Using sequential clicking to extract all {len(waze_links)} Waze links...")
            
            waze_links_map = await self._extract_by_sequential_clicking(waze_links)
            
            self.logger.info(f"📊 Sequential clicking extracted {len(waze_links_map)}/{len(waze_links)} Waze links")
                        
        except Exception as e:
            self.logger.error(f"❌ Error extracting dynamic Waze links: {e}")
            
        return waze_links_map
    
    async def _extract_by_container_matching(self, outlet_containers, waze_links) -> Dict[str, str]:
        """Extract by matching outlet containers with Waze links (from working extract_waze_links.py)."""
        
        self.logger.info("🎯 Method 1: Matching outlets with Waze links by container...")
        
        outlets_with_waze = {}
        
        for i, container in enumerate(outlet_containers):
            try:
                # Extract outlet name from container
                outlet_name = await self._extract_outlet_name_from_container(container)
                
                if not outlet_name:
                    continue
                
                # Find Waze link within this container
                waze_link = await container.query_selector('a:has-text("Waze")')
                
                if waze_link:
                    # Click the Waze link and capture URL
                    waze_url = await self._click_and_capture_waze_url(waze_link, outlet_name)
                    
                    if waze_url:
                        outlets_with_waze[outlet_name] = waze_url
                        
                        if self.debug:
                            self.logger.info(f"✅ {outlet_name}: {waze_url}")
                    else:
                        if self.debug:
                            self.logger.info(f"❌ Failed to extract Waze URL for {outlet_name}")
                else:
                    if self.debug:
                        self.logger.info(f"❌ No Waze link found in container for {outlet_name}")
                    
            except Exception as e:
                if self.debug:
                    self.logger.warning(f"❌ Error processing container {i}: {e}")
                
        return outlets_with_waze
    
    async def _extract_by_sequential_clicking(self, waze_links) -> Dict[str, str]:
        """Extract by clicking each Waze link sequentially (from working extract_waze_links.py)."""
        
        self.logger.info("🎯 Method 2: Sequential clicking of Waze links...")
        
        outlets_with_waze = {}
        
        for i, waze_link in enumerate(waze_links):
            try:
                # Find the outlet name associated with this Waze link
                outlet_name = await self._find_outlet_name_for_waze_link(waze_link)
                
                if outlet_name:
                    # Click the Waze link and capture URL
                    waze_url = await self._click_and_capture_waze_url(waze_link, outlet_name)
                    
                    if waze_url:
                        outlets_with_waze[outlet_name] = waze_url
                        
                        if self.debug:
                            self.logger.info(f"✅ {outlet_name}: {waze_url}")
                    else:
                        if self.debug:
                            self.logger.info(f"❌ Failed to extract Waze URL for {outlet_name}")
                else:
                    if self.debug:
                        self.logger.info(f"❌ Could not find outlet name for Waze link {i}")
                    
            except Exception as e:
                if self.debug:
                    self.logger.warning(f"❌ Error processing Waze link {i}: {e}")
        
        self.logger.info(f"🎯 Sequential clicking completed, extracted {len(outlets_with_waze)} links")        
        return outlets_with_waze
    
    async def _extract_outlet_name_from_container(self, container) -> Optional[str]:
        """Extract outlet name from container element (from working extract_waze_links.py)."""
        try:
            # Try different selectors for outlet name
            selectors = [
                'h3', 'h4', 'h5',  # Header tags
                '.outlet-name', '.restaurant-name',  # Class names
                '[class*="name"]', '[class*="title"]'  # Partial class matches
            ]
            
            for selector in selectors:
                name_element = await container.query_selector(selector)
                if name_element:
                    name = await name_element.text_content()
                    if name and "McDonald's" in name:
                        return name.strip()
            
            # Fallback: extract from text content
            text_content = await container.text_content()
            if text_content:
                # Look for McDonald's in the text
                lines = text_content.split('\n')
                for line in lines:
                    if "McDonald's" in line and len(line.strip()) < 100:
                        return line.strip()
                        
        except Exception as e:
            if self.debug:
                self.logger.warning(f"❌ Error extracting outlet name: {e}")
            
        return None
    
    async def _find_outlet_name_for_waze_link(self, waze_link) -> Optional[str]:
        """Find the outlet name associated with a Waze link."""
        try:
            # Navigate up the DOM to find the outlet container
            parent = waze_link
            for _ in range(10):  # Try up to 10 levels up
                parent = await parent.evaluate('el => el.parentElement')
                if not parent:
                    break
                    
                # Check if this parent contains outlet information
                text_content = await parent.text_content()
                if text_content and "McDonald's" in text_content:
                    # Extract outlet name from this container
                    lines = text_content.split('\n')
                    for line in lines:
                        if "McDonald's" in line and len(line.strip()) < 100:
                            return line.strip()
                            
        except Exception as e:
            if self.debug:
                self.logger.warning(f"Error finding outlet name for Waze link: {e}")
            
        return None
    
    async def _click_and_capture_waze_url(self, waze_link, outlet_name: str) -> Optional[str]:
        """Click Waze link and capture the URL it navigates to."""
        try:
            # Clear previous captured URLs
            self.captured_urls = []
            
            # Click the Waze link
            await waze_link.click()
            
            # Wait a moment for the navigation to trigger
            await asyncio.sleep(2)
            
            # Check if we captured any URLs
            if self.captured_urls:
                return self.captured_urls[-1]  # Return the last captured URL
            
            # Alternative: Try to detect if a new tab was opened
            pages = self.context.pages
            if len(pages) > 1:
                # A new tab was opened, get its URL
                new_page = pages[-1]
                url = new_page.url
                await new_page.close()  # Close the new tab
                
                if 'waze.com' in url or 'waze://' in url:
                    return url
                    
        except Exception as e:
            if self.debug:
                self.logger.warning(f"❌ Error clicking Waze link for {outlet_name}: {e}")
            
        return None
    
    def _add_waze_link_from_map(self, outlet_data: Dict[str, Any], waze_links_map: Dict[str, str]) -> Dict[str, Any]:
        """Add Waze link to outlet data from the extracted Waze links map."""
        outlet_name = outlet_data.get('name', '')
        
        # Try exact match first
        if outlet_name in waze_links_map:
            outlet_data['waze_link'] = waze_links_map[outlet_name]
            self.stats['waze_links_matched'] += 1
            if self.debug:
                self.logger.info(f"    🔗 Added Waze link (exact match): {outlet_name}")
            return outlet_data
        
        # Try partial match (in case name cleaning differs)
        for waze_name, waze_url in waze_links_map.items():
            # Extract the key part of the name for comparison
            outlet_key = outlet_name.replace("McDonald's", "").strip()
            waze_key = waze_name.replace("McDonald's", "").strip()
            
            if outlet_key and waze_key and (outlet_key in waze_key or waze_key in outlet_key):
                outlet_data['waze_link'] = waze_url
                self.stats['waze_links_matched'] += 1
                if self.debug:
                    self.logger.info(f"    🔗 Added Waze link (partial match): {outlet_name} -> {waze_name}")
                return outlet_data
        
        # No match found
        if self.debug:
            self.logger.warning(f"    ❌ No Waze link found for: {outlet_name}")
        
        return outlet_data
    
    def _extract_outlet_from_text(self, text_block: str) -> Optional[Dict[str, Any]]:
        """Extract outlet data from a single text block."""
        try:
            if not text_block or len(text_block.strip()) < 10:
                return None
            
            # Extract all data in one pass
            outlet_data = {
                'name': self._extract_name(text_block),
                'address': self._extract_address(text_block),
                'operating_hours': self._extract_hours(text_block, ''),
                'phone': self._extract_phone(text_block),
                'waze_link': self._extract_waze_link_from_text(text_block),  # Now extract from text too
                'features': self._extract_features(text_block, '')
            }
            
            return outlet_data
            
        except Exception as e:
            if self.debug:
                self.logger.warning(f"⚠️ Error extracting outlet from text block: {e}")
            return None
    
    async def _extract_complete_outlet_data(self, element) -> Optional[Dict[str, Any]]:
        """Extract complete outlet data from a single element efficiently."""
        try:
            # Get all text content at once
            text_content = await element.text_content()
            inner_html = await element.inner_html()
            
            if not text_content or len(text_content.strip()) < 10:
                return None
            
            # Extract all data in one pass
            outlet_data = {
                'name': self._extract_name(text_content),
                'address': self._extract_address(text_content),
                'operating_hours': self._extract_hours(text_content, inner_html),
                'phone': self._extract_phone(text_content),
                'waze_link': self._extract_waze_link(inner_html),
                'features': self._extract_features(text_content, inner_html)
            }
            
            return outlet_data
            
        except Exception as e:
            if self.debug:
                self.logger.warning(f"⚠️ Error extracting outlet data: {e}")
            return None
    
    def _extract_name(self, text: str) -> str:
        """Extract outlet name efficiently."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines:
            # Clean line of JSON-like syntax
            clean_line = re.sub(r'"[^"]*":\s*"', '', line)  # Remove JSON key-value patterns
            clean_line = re.sub(r'[{}",]', '', clean_line)  # Remove JSON characters
            clean_line = re.sub(r'\s+', ' ', clean_line).strip()
            
            if "McDonald's" in clean_line and len(clean_line) < 100 and clean_line:
                # Ensure it starts with McDonald's
                if not clean_line.startswith("McDonald's"):
                    cleaned_text = clean_line.replace("McDonald's", "").strip()
                    clean_line = f"McDonald's {cleaned_text}"
                return clean_line
        
        # Fallback: look for any mention of McDonald's
        for line in lines:
            if "McDonald's" in line:
                # Extract just the McDonald's part
                match = re.search(r"McDonald's[^,\n]*", line)
                if match:
                    return match.group(0).strip()
        
        return "McDonald's Unknown"
    
    def _extract_address(self, text: str) -> str:
        """Extract address efficiently with improved filtering."""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Clean lines of JSON-like syntax
        clean_lines = []
        for line in lines:
            clean_line = re.sub(r'"[^"]*":\s*"', '', line)  # Remove JSON key-value patterns
            clean_line = re.sub(r'[{}",]', '', clean_line)  # Remove JSON characters
            clean_line = re.sub(r'\s+', ' ', clean_line).strip()
            if clean_line and len(clean_line) > 5:
                clean_lines.append(clean_line)
        
        # Filter out lines that contain phone/fax/contact information
        address_lines = []
        for line in clean_lines:
            # Skip lines that contain phone numbers, fax, email, or other contact info
            if any(contact_keyword in line.lower() for contact_keyword in ['tel:', 'fax:', 'phone:', 'email:', '@']):
                continue
            # Skip lines that are mostly phone numbers
            if re.search(r'\b03-\d{8}\b', line) or re.search(r'\b\d{3}-\d{8}\b', line):
                continue
            # Skip lines that contain "McDonald's" (restaurant names)
            if "McDonald's" in line:
                continue
            # Keep lines that look like addresses
            if any(keyword in line.lower() for keyword in ['jalan', 'jln', 'road', 'street', 'avenue', 'lot', 'ground floor', 'level', 'mall', 'complex', 'kuala lumpur', 'kl', 'malaysia']):
                address_lines.append(line)
        
        # If we have address lines, join the first 1-2 that contain location information
        if address_lines:
            # Take the first address line that contains street/location info
            primary_address = address_lines[0]
            
            # Check if we should add a second line (but be selective)
            if len(address_lines) > 1:
                second_line = address_lines[1]
                # Only add if it adds meaningful location info and isn't too long
                if (len(second_line) < 50 and 
                    any(keyword in second_line.lower() for keyword in ['kuala lumpur', 'kl', 'malaysia', 'selangor', 'wilayah']) and
                    not any(skip_keyword in second_line.lower() for skip_keyword in ['tel', 'fax', 'phone', 'email'])):
                    primary_address = f"{primary_address}, {second_line}"
            
            # Final cleaning
            address = re.sub(r'\s+', ' ', primary_address).strip()
            return address
        
        # Fallback: look for any line with location keywords
        for line in clean_lines:
            if (any(keyword in line.lower() for keyword in ['jalan', 'jln', 'road', 'street', 'kuala lumpur', 'malaysia']) and
                not any(skip_keyword in line.lower() for skip_keyword in ['tel:', 'fax:', 'phone:', 'email:', '@']) and
                "McDonald's" not in line):
                return re.sub(r'\s+', ' ', line).strip()
        
        # Final fallback: take the longest clean line that looks like an address
        address_candidates = [line for line in clean_lines if len(line) > 20 and "McDonald's" not in line.lower() and not re.search(r'\b03-\d{8}\b', line)]
        if address_candidates:
            best_address = max(address_candidates, key=len)
            return re.sub(r'\s+', ' ', best_address).strip()
        
        return "Address not available"
    
    def _extract_hours(self, text: str, html: str) -> str:
        """Extract operating hours efficiently."""
        # Look for time patterns
        time_patterns = [
            r'\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\s*-\s*\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?',
            r'\d{1,2}\.\d{2}\s*(?:AM|PM|am|pm)?\s*-\s*\d{1,2}\.\d{2}\s*(?:AM|PM|am|pm)?',
            r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun).*?\d{1,2}:\d{2}',
            r'24\s*(?:hours|hrs)',
            r'Open\s+24\s+hours'
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0]
        
        # Check for "24 Hours" indicators
        if any(indicator in text.lower() for indicator in ['24 hours', '24hrs', 'open 24', '24/7']):
            return "24 Hours"
        
        return "Hours not available"
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number efficiently."""
        # Malaysian phone patterns
        phone_patterns = [
            r'03-\d{8}',
            r'03-\d{4}\s*\d{4}',
            r'\+60\s*3-?\d{8}',
            r'03\s*\d{8}'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        
        return ""
    
    def _extract_waze_link(self, html: str) -> str:
        """Extract Waze link efficiently."""
        waze_patterns = [
            r'https://waze\.com/ul[^"\'>\s]+',
            r'https://www\.waze\.com/ul[^"\'>\s]+',
            r'waze\.com/ul[^"\'>\s]+'
        ]
        
        for pattern in waze_patterns:
            matches = re.findall(pattern, html)
            if matches:
                link = matches[0]
                if not link.startswith('http'):
                    link = f"https://{link}"
                return link
        
        return ""
    
    def _extract_waze_link_from_text(self, text: str) -> str:
        """Extract Waze link from text content (for text-based extraction)."""
        # Look for Waze links in plain text
        waze_patterns = [
            r'https://waze\.com/ul[^\s]+',
            r'https://www\.waze\.com/ul[^\s]+',
            r'waze\.com/ul[^\s]+',
            # Sometimes Waze links appear without protocol
            r'(?:^|\s)(waze\.com/ul[^\s]+)',
        ]
        
        for pattern in waze_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                link = matches[0]
                # Handle tuple results from capturing groups
                if isinstance(link, tuple):
                    link = link[0] if link[0] else link[1]
                
                if not link.startswith('http'):
                    link = f"https://{link}"
                return link
        
        return ""
    
    def _extract_features(self, text: str, html: str) -> List[str]:
        """Extract features efficiently."""
        features = []
        
        feature_keywords = {
            '24 Hours': ['24 hours', '24hrs', 'open 24'],
            'Drive-Thru': ['drive-thru', 'drive thru', 'drivethrough'],
            'McCafe': ['mccafe', 'mc cafe'],
            'PlayPlace': ['playplace', 'play place'],
            'WiFi': ['wifi', 'wi-fi', 'wireless'],
            'Delivery': ['delivery', 'mcdelivery'],
            'Parking': ['parking', 'car park']
        }
        
        text_lower = text.lower()
        for feature, keywords in feature_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                features.append(feature)
        
        return features
    
    def _is_valid_outlet(self, outlet: Dict[str, Any]) -> bool:
        """Check if outlet data is valid."""
        name = outlet.get('name', '')
        address = outlet.get('address', '')
        
        # Must have name and address
        if not name or not address:
            return False
        
        # Must contain McDonald's
        if "McDonald's" not in name:
            return False
        
        # Address should be reasonable length
        if len(address) < 10:
            return False
        
        return True
    
    async def _add_geocoding(self, outlet_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add geocoding to outlet data."""
        if not self.geocoder or not self.stats['geocoding_enabled']:
            return outlet_data
        
        try:
            geocoding_start = time.time()
            
            # Get coordinates (synchronous call)
            enhanced_outlet = self.geocoder.geocode_outlet(outlet_data)
            
            geocoding_time = time.time() - geocoding_start
            self.stats['geocoding_time'] += geocoding_time
            
            # Check if geocoding was successful
            if enhanced_outlet.get('geocoding', {}).get('status') == 'success':
                self.stats['geocoding_successful'] += 1
                
                # Track if coordinates came from Waze link
                if enhanced_outlet.get('geocoding', {}).get('location_type') == 'waze_link':
                    self.stats['waze_coordinates_extracted'] += 1
                
                if self.debug:
                    lat = enhanced_outlet.get('latitude', 0)
                    lng = enhanced_outlet.get('longitude', 0)
                    location_type = enhanced_outlet.get('geocoding', {}).get('location_type', 'unknown')
                    self.logger.info(f"  🗺️  Geocoded: {lat:.4f},{lng:.4f} ({geocoding_time:.2f}s) via {location_type}")
                
                return enhanced_outlet
            else:
                self.stats['geocoding_failed'] += 1
                if self.debug:
                    reason = enhanced_outlet.get('geocoding', {}).get('reason', 'Unknown')
                    self.logger.warning(f"  🗺️  Geocoding failed for {outlet_data.get('name', 'Unknown')}: {reason}")
                
                return outlet_data
                    
        except Exception as e:
            self.stats['geocoding_failed'] += 1
            self.logger.error(f"  ❌ Geocoding error for {outlet_data.get('name', 'Unknown')}: {e}")
        
        return outlet_data
    
    async def _save_to_database(self, outlets: List[Dict[str, Any]]):
        """Save outlets to database efficiently with improved duplicate handling."""
        self.logger.info(f"💾 Saving {len(outlets)} outlets to database...")
        
        for outlet in outlets:
            try:
                # Validate data
                clean_data = validate_outlet_data(outlet)
                
                # Double-check for duplicates at database level (more reliable)
                existing_outlet = self._check_outlet_exists_in_db(clean_data['name'])
                
                if not existing_outlet:
                    try:
                        outlet_id = self.db_operations.insert_outlet(clean_data)
                        if outlet_id:
                            self.stats['successfully_saved'] += 1
                            if self.debug:
                                self.logger.info(f"💾 Saved: {clean_data['name']}")
                        else:
                            self.stats['database_errors'] += 1
                    except Exception as db_error:
                        # Handle unique constraint violations gracefully
                        if "UNIQUE constraint failed" in str(db_error):
                            self.stats['duplicates_skipped'] += 1
                            if self.debug:
                                self.logger.info(f"🔄 Skipped duplicate: {clean_data['name']}")
                        else:
                            self.stats['database_errors'] += 1
                            self.logger.error(f"❌ Database error for {clean_data['name']}: {db_error}")
                else:
                    self.stats['duplicates_skipped'] += 1
                    if self.debug:
                        self.logger.info(f"🔄 Already exists: {clean_data['name']}")
                        
            except Exception as e:
                self.logger.error(f"❌ Validation error for {outlet.get('name', 'Unknown')}: {e}")
                self.stats['database_errors'] += 1
        
        self.logger.info(f"✅ Database save complete: {self.stats['successfully_saved']} saved, {self.stats['duplicates_skipped']} duplicates skipped, {self.stats['database_errors']} errors")
    
    def _check_outlet_exists_in_db(self, outlet_name: str) -> bool:
        """Check if outlet already exists in database by name."""
        try:
            from database.connection import get_db_client
            db = get_db_client()
            result = db.execute("SELECT COUNT(*) FROM outlets WHERE name = ?", (outlet_name,))
            count = result.rows[0][0] if result.rows else 0
            return count > 0
        except Exception as e:
            if self.debug:
                self.logger.warning(f"⚠️ Error checking outlet existence: {e}")
            return False
    
    async def _generate_report(self, outlets: List[Dict[str, Any]]):
        """Generate final report."""
        self.logger.info("=" * 80)
        self.logger.info("📊 OPTIMIZED SCRAPING COMPLETE")
        self.logger.info("=" * 80)
        self.logger.info(f"🏪 Total unique outlets: {self.stats['unique_outlets']}")
        self.logger.info(f"🔄 Duplicates skipped: {self.stats['duplicates_skipped']}")
        self.logger.info(f"💾 Successfully saved: {self.stats['successfully_saved']}")
        self.logger.info(f"❌ Database errors: {self.stats['database_errors']}")
        
        # Waze link statistics
        self.logger.info(f"🔗 Waze links extracted: {self.stats['waze_links_extracted']}")
        self.logger.info(f"🔗 Waze links matched: {self.stats['waze_links_matched']}")
        self.logger.info(f"🔗 Waze coordinates extracted: {self.stats['waze_coordinates_extracted']}")
        
        # Geocoding statistics
        if self.stats['geocoding_enabled']:
            self.logger.info(f"🗺️  Geocoding successful: {self.stats['geocoding_successful']}")
            self.logger.info(f"🗺️  Geocoding failed: {self.stats['geocoding_failed']}")
            self.logger.info(f"🗺️  Geocoding time: {self.stats['geocoding_time']:.1f}s")
            if self.stats['geocoding_successful'] > 0:
                avg_geocoding_time = self.stats['geocoding_time'] / self.stats['geocoding_successful']
                self.logger.info(f"🗺️  Average geocoding time: {avg_geocoding_time:.2f}s per outlet")
        
        self.logger.info(f"⏱️ Total runtime: {self.stats['total_runtime']:.1f}s")
        self.logger.info(f"⚡ Efficiency: {self.stats['unique_outlets'] / max(self.stats['total_runtime'], 1):.1f} outlets/second")
        self.logger.info("✅ Optimized scraping with geocoding completed!")
    
    async def _cleanup(self):
        """Cleanup browser resources."""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

async def main():
    """Run optimized scraper."""
    scraper = McDonaldMalaysiaScraper(
        headless=True,
        debug=True,
        database_integration=True
    )
    
    result = await scraper.scrape_outlets("Kuala Lumpur")
    
    print(f"\n🎉 Optimized scraping completed!")
    print(f"📊 Unique outlets found: {result['statistics']['unique_outlets']}")
    print(f"⏱️ Total time: {result['statistics']['total_runtime']:.1f}s")
    print(f"⚡ Efficiency: No redundancy, single-pass extraction!")

if __name__ == "__main__":
    asyncio.run(main()) 