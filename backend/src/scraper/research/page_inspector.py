#!/usr/bin/env python3
"""
McDonald's Malaysia Page Inspector - Phase 1 Research
Simple script to analyze the website structure without complex scraping.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin
import os
from datetime import datetime

class McDonaldsPageInspector:
    """Simple page inspector for McDonald's Malaysia website research."""
    
    def __init__(self):
        self.base_url = "https://www.mcdonalds.com.my"
        self.locate_url = "https://www.mcdonalds.com.my/locate-us"
        self.session = requests.Session()
        
        # Set a realistic user agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Create samples directory
        self.samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
        os.makedirs(self.samples_dir, exist_ok=True)
    
    def inspect_main_page(self):
        """Inspect the main locate-us page."""
        print("🔍 Inspecting main locate-us page...")
        
        try:
            response = self.session.get(self.locate_url, timeout=10)
            response.raise_for_status()
            
            # Save raw HTML for analysis
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_file = os.path.join(self.samples_dir, f'locate_us_page_{timestamp}.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"✅ Page loaded successfully (Status: {response.status_code})")
            print(f"📄 HTML saved to: {html_file}")
            print(f"📏 Page size: {len(response.text):,} characters")
            
            return response.text
            
        except requests.RequestException as e:
            print(f"❌ Error loading page: {e}")
            return None
    
    def analyze_page_structure(self, html_content):
        """Analyze the HTML structure of the page."""
        print("\n🔬 Analyzing page structure...")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Basic page analysis
        analysis = {
            'title': soup.title.string if soup.title else 'No title',
            'meta_description': '',
            'scripts': [],
            'forms': [],
            'select_elements': [],
            'outlet_containers': [],
            'javascript_hints': [],
            'ajax_hints': []
        }
        
        # Check meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            analysis['meta_description'] = meta_desc.get('content', '')
        
        # Find all script tags
        scripts = soup.find_all('script')
        for script in scripts:
            src = script.get('src', '')
            if src:
                analysis['scripts'].append(src)
            # Check for inline JavaScript that might load data
            script_content = script.string or ''
            if any(keyword in script_content.lower() for keyword in ['ajax', 'fetch', 'api', 'outlet', 'location']):
                analysis['javascript_hints'].append(script_content[:200] + '...' if len(script_content) > 200 else script_content)
        
        # Find forms (might be used for filtering)
        forms = soup.find_all('form')
        for form in forms:
            form_info = {
                'action': form.get('action', ''),
                'method': form.get('method', 'GET'),
                'inputs': [inp.get('name') for inp in form.find_all('input') if inp.get('name')]
            }
            analysis['forms'].append(form_info)
        
        # Find select elements (dropdowns for filtering)
        selects = soup.find_all('select')
        for select in selects:
            select_info = {
                'name': select.get('name', ''),
                'id': select.get('id', ''),
                'options': [opt.get_text(strip=True) for opt in select.find_all('option')]
            }
            analysis['select_elements'].append(select_info)
        
        # Look for potential outlet containers
        # Common patterns: divs with classes like 'outlet', 'location', 'store', etc.
        potential_containers = soup.find_all(['div', 'article', 'section'], 
                                           class_=lambda x: x and any(keyword in x.lower() 
                                           for keyword in ['outlet', 'location', 'store', 'restaurant', 'shop']))
        
        for container in potential_containers[:5]:  # Limit to first 5 for analysis
            container_info = {
                'tag': container.name,
                'class': container.get('class', []),
                'id': container.get('id', ''),
                'text_preview': container.get_text(strip=True)[:100] + '...' if len(container.get_text(strip=True)) > 100 else container.get_text(strip=True)
            }
            analysis['outlet_containers'].append(container_info)
        
        return analysis
    
    def check_javascript_requirements(self, html_content):
        """Check if JavaScript is required to load outlet data."""
        print("\n🔍 Checking JavaScript requirements...")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for signs that data is loaded via JavaScript
        js_indicators = {
            'empty_containers': 0,
            'loading_indicators': 0,
            'api_endpoints': [],
            'ajax_patterns': 0
        }
        
        # Check for empty containers that might be populated by JS
        potential_data_containers = soup.find_all(['div', 'ul', 'ol'], 
                                                 class_=lambda x: x and any(keyword in ' '.join(x).lower() 
                                                 for keyword in ['outlet', 'location', 'store', 'list', 'container']))
        
        for container in potential_data_containers:
            if not container.get_text(strip=True):
                js_indicators['empty_containers'] += 1
        
        # Look for loading indicators
        loading_elements = soup.find_all(text=lambda text: text and any(keyword in text.lower() 
                                        for keyword in ['loading', 'please wait', 'fetching']))
        js_indicators['loading_indicators'] = len(loading_elements)
        
        # Check script content for API endpoints
        scripts = soup.find_all('script')
        for script in scripts:
            script_content = script.string or ''
            # Look for API endpoints
            if '/api/' in script_content or 'fetch(' in script_content or 'xhr' in script_content.lower():
                js_indicators['ajax_patterns'] += 1
                # Try to extract API endpoints
                import re
                api_matches = re.findall(r'["\']([^"\']*api[^"\']*)["\']', script_content)
                js_indicators['api_endpoints'].extend(api_matches)
        
        return js_indicators
    
    def look_for_kuala_lumpur_data(self, html_content):
        """Look for Kuala Lumpur specific data or filtering options."""
        print("\n🏙️ Looking for Kuala Lumpur data and filtering...")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        kl_findings = {
            'kl_mentions': 0,
            'state_options': [],
            'filtering_mechanism': None,
            'outlet_previews': []
        }
        
        # Count KL mentions
        page_text = soup.get_text().lower()
        kl_keywords = ['kuala lumpur', 'kl', 'selangor', 'wilayah persekutuan']
        for keyword in kl_keywords:
            kl_findings['kl_mentions'] += page_text.count(keyword)
        
        # Look for state/location filtering options
        selects = soup.find_all('select')
        for select in selects:
            options = [opt.get_text(strip=True) for opt in select.find_all('option')]
            if any('kuala lumpur' in opt.lower() or 'selangor' in opt.lower() for opt in options):
                kl_findings['state_options'] = options
                kl_findings['filtering_mechanism'] = {
                    'type': 'select_dropdown',
                    'name': select.get('name', ''),
                    'id': select.get('id', '')
                }
                break
        
        # Look for any visible outlet data
        text_content = soup.get_text()
        if 'mcdonald' in text_content.lower() and any(keyword in text_content.lower() for keyword in ['jalan', 'street', 'mall', 'plaza']):
            # Try to find outlet-like text patterns
            import re
            outlet_patterns = re.findall(r'[A-Z][^.!?]*(?:jalan|street|mall|plaza|avenue)[^.!?]*', text_content)
            kl_findings['outlet_previews'] = outlet_patterns[:3]  # First 3 matches
        
        return kl_findings
    
    def save_analysis_report(self, analysis, js_check, kl_findings):
        """Save the complete analysis report."""
        print("\n📝 Saving analysis report...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = {
            'analysis_timestamp': timestamp,
            'url_analyzed': self.locate_url,
            'page_structure': analysis,
            'javascript_requirements': js_check,
            'kuala_lumpur_findings': kl_findings,
            'recommendations': self.generate_recommendations(analysis, js_check, kl_findings)
        }
        
        # Save as JSON
        report_file = os.path.join(self.samples_dir, f'analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Analysis report saved to: {report_file}")
        
        # Also create a markdown report
        self.create_markdown_report(report)
        
        return report
    
    def generate_recommendations(self, analysis, js_check, kl_findings):
        """Generate recommendations based on the analysis."""
        recommendations = []
        
        # Check if requests + BeautifulSoup will work
        if js_check['empty_containers'] > 2 or js_check['ajax_patterns'] > 0:
            recommendations.append("⚠️ JavaScript may be required - consider Playwright if requests fails")
        else:
            recommendations.append("✅ requests + BeautifulSoup likely sufficient")
        
        # Filtering recommendations
        if kl_findings['filtering_mechanism']:
            recommendations.append(f"✅ State filtering available via {kl_findings['filtering_mechanism']['type']}")
        else:
            recommendations.append("⚠️ No obvious filtering mechanism found - may need to scrape all and filter")
        
        # Data availability
        if kl_findings['outlet_previews']:
            recommendations.append("✅ Outlet data appears to be present in HTML")
        else:
            recommendations.append("⚠️ Outlet data may be loaded dynamically")
        
        return recommendations
    
    def create_markdown_report(self, report):
        """Create a human-readable markdown report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        md_file = os.path.join(self.samples_dir, f'research_report_{timestamp}.md')
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"""# McDonald's Malaysia Website Analysis Report

**Analysis Date**: {report['analysis_timestamp']}
**URL Analyzed**: {report['url_analyzed']}

## 🎯 Key Findings

### JavaScript Requirements
- Empty containers: {report['javascript_requirements']['empty_containers']}
- AJAX patterns detected: {report['javascript_requirements']['ajax_patterns']}
- Loading indicators: {report['javascript_requirements']['loading_indicators']}

### Kuala Lumpur Data
- KL mentions found: {report['kuala_lumpur_findings']['kl_mentions']}
- Filtering mechanism: {report['kuala_lumpur_findings']['filtering_mechanism']}
- Outlet previews found: {len(report['kuala_lumpur_findings']['outlet_previews'])}

## 📋 Recommendations

""")
            for rec in report['recommendations']:
                f.write(f"- {rec}\n")
            
            f.write(f"""
## 🔍 Detailed Analysis

### Page Structure
- Title: {report['page_structure']['title']}
- Scripts found: {len(report['page_structure']['scripts'])}
- Forms found: {len(report['page_structure']['forms'])}
- Select elements: {len(report['page_structure']['select_elements'])}

### State Options Found
""")
            for option in report['kuala_lumpur_findings']['state_options']:
                f.write(f"- {option}\n")
            
            f.write(f"""
### Sample Outlet Text
""")
            for preview in report['kuala_lumpur_findings']['outlet_previews']:
                f.write(f"- {preview}\n")
        
        print(f"📄 Markdown report saved to: {md_file}")
    
    def run_full_inspection(self):
        """Run the complete page inspection process."""
        print("🚀 Starting McDonald's Malaysia Page Inspection")
        print("=" * 50)
        
        # Step 1: Load the page
        html_content = self.inspect_main_page()
        if not html_content:
            print("❌ Failed to load page. Inspection aborted.")
            return None
        
        # Step 2: Analyze structure
        analysis = self.analyze_page_structure(html_content)
        
        # Step 3: Check JavaScript requirements
        js_check = self.check_javascript_requirements(html_content)
        
        # Step 4: Look for KL data
        kl_findings = self.look_for_kuala_lumpur_data(html_content)
        
        # Step 5: Save report
        report = self.save_analysis_report(analysis, js_check, kl_findings)
        
        # Step 6: Print summary
        self.print_summary(report)
        
        return report
    
    def print_summary(self, report):
        """Print a summary of findings."""
        print("\n" + "=" * 50)
        print("📊 INSPECTION SUMMARY")
        print("=" * 50)
        
        print(f"🌐 Page Title: {report['page_structure']['title']}")
        print(f"📜 Scripts Found: {len(report['page_structure']['scripts'])}")
        print(f"📝 Forms Found: {len(report['page_structure']['forms'])}")
        print(f"🔽 Select Elements: {len(report['page_structure']['select_elements'])}")
        print(f"🏙️ KL Mentions: {report['kuala_lumpur_findings']['kl_mentions']}")
        
        print("\n🎯 KEY RECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"  {rec}")
        
        print(f"\n📁 Files saved in: {self.samples_dir}")
        print("✅ Phase 1 Research Complete!")

def main():
    """Main function to run the page inspection."""
    inspector = McDonaldsPageInspector()
    inspector.run_full_inspection()

if __name__ == "__main__":
    main() 