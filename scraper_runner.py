#!/usr/bin/env python3
"""
McDonald's Malaysia Scraper Runner
Production runner for the McDonald's Malaysia outlet scraper.
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend" / "src"
sys.path.insert(0, str(backend_path))

from scraper.mcdonald_scraper import McDonaldMalaysiaScraper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def run_production_scraper():
    """Run the production McDonald's scraper."""
    print("🚀 McDonald's Malaysia Production Scraper v1.0")
    print("⚡ Production Ready - Efficient Data Extraction")
    print("=" * 80)
    
    # Create production scraper with optimized settings
    scraper = McDonaldMalaysiaScraper(
        headless=True,           # Run in background
        debug=False,            # Production mode - clean logs
        database_integration=True  # Save to database
    )
    
    try:
        # Run scraper for Kuala Lumpur
        print("🎯 Target: Kuala Lumpur McDonald's outlets")
        print("⚡ Starting production scraping...")
        
        result = await scraper.scrape_outlets("Kuala Lumpur")
        
        # Display results
        stats = result['statistics']
        print(f"\n🎉 PRODUCTION SCRAPING COMPLETE!")
        print(f"📊 Results Summary:")
        print(f"   🏪 Unique outlets found: {stats['unique_outlets']}")
        print(f"   🔄 Duplicates skipped: {stats['duplicates_skipped']}")
        print(f"   💾 Successfully saved to database: {stats['successfully_saved']}")
        print(f"   ❌ Database errors: {stats['database_errors']}")
        print(f"   🔗 Waze links extracted: {stats.get('waze_coordinates_extracted', 0)}")
        print(f"   🗺️  Geocoding successful: {stats.get('geocoding_successful', 0)}")
        print(f"   ⏱️ Total runtime: {stats['total_runtime']:.1f} seconds")
        print(f"   ⚡ Processing efficiency: {stats['unique_outlets'] / max(stats['total_runtime'], 1):.1f} outlets/second")
        
        # Show Waze link success rate
        waze_success_rate = (stats.get('waze_coordinates_extracted', 0) / max(stats['unique_outlets'], 1)) * 100
        print(f"   📍 Waze link success rate: {waze_success_rate:.1f}%")
        
        print(f"\n✅ Session ID: {stats['session_id']}")
        print("🚀 Production scraping completed successfully!")
        
        return result
        
    except Exception as e:
        print(f"❌ Production scraping failed: {e}")
        return None

def main():
    """Main entry point."""
    try:
        result = asyncio.run(run_production_scraper())
        if result:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure
    except KeyboardInterrupt:
        print("\n⚠️ Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 