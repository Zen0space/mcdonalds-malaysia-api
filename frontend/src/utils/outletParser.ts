export interface OutletInfo {
  name: string;
  address: string;
  distance: string;
  operatingHours: string;
  wazeLink: string;
}

export function parseOutletInfo(content: string): OutletInfo[] | null {
  // Check if this looks like outlet information
  if (!content.includes('**McDonald\'s') || (!content.includes('**Address:**') && !content.includes('Address:'))) {
    return null;
  }

  console.log('🔍 Parsing outlet content:', content);

  const outlets: OutletInfo[] = [];
  
  // Split by outlet entries starting with **McDonald's or numbered items
  const outletBlocks = content.split(/(?=\d+\.\s*\*\*McDonald's|(?=\*\*McDonald's))/);
  
  for (const block of outletBlocks) {
    if (!block.trim() || !block.includes('**McDonald\'s')) continue;
    
    console.log('🏪 Processing block:', block);
    
    try {
      // Extract name (line with **McDonald's) - handle both formats
      const nameMatch = block.match(/\*\*(McDonald's[^*]+)\*\*/) || 
                       block.match(/\d+\.\s*\*\*(McDonald's[^*]+)\*\*/);
      const name = nameMatch ? nameMatch[1].trim() : '';
      
      // Extract distance from name line if present (e.g., "(0.84 km away)")
      const distanceFromName = block.match(/\([^)]*km[^)]*\)/);
      const distanceFromNameText = distanceFromName ? distanceFromName[0] : '';
      
      // Extract address (after **Address:** or Address:)
      const addressMatch = block.match(/\*\*Address:\*\*\s*([^\n*]+(?:\n[^*\n]+)*)/) || 
                          block.match(/Address:\s*([^\n]+(?:\n[^\n]*Operating|[^\n]*Waze|[^\n]*$)*)/);
      let address = addressMatch ? addressMatch[1].trim().replace(/\n/g, ' ') : '';
      
      // Clean up address - remove Operating Hours and Waze Link if they got included
      address = address.replace(/Operating Hours:.*$/i, '').replace(/Waze Link:.*$/i, '').trim();
      
      // Extract distance (after **Distance:** or use distance from name)
      const distanceMatch = block.match(/\*\*Distance:\*\*\s*([^\n*]+)/);
      const distance = distanceMatch ? distanceMatch[1].trim() : distanceFromNameText;
      
      // Extract operating hours (after **Operating Hours:** or Operating Hours:)
      const hoursMatch = block.match(/\*\*Operating Hours:\*\*\s*([^\n*]+)/) || 
                        block.match(/Operating Hours:\s*([^\n]*(?:not available|[^\n]*Waze|[^\n]*$))/);
      let operatingHours = hoursMatch ? hoursMatch[1].trim() : '';
      
      // Clean up operating hours - remove Waze Link if it got included
      operatingHours = operatingHours.replace(/Waze Link:.*$/i, '').trim();
      
      // Extract Waze link - more flexible patterns
      const wazeMatch = block.match(/\*\*Waze Link:\*\*\s*(https?:\/\/[^\s]+)/) || 
                       block.match(/Waze Link:\s*(https?:\/\/[^\s]+)/) ||
                       block.match(/(https?:\/\/(?:www\.)?waze\.com[^\s]*)/i) ||
                       block.match(/(https?:\/\/[^\s]*waze[^\s]*)/i);
      const wazeLink = wazeMatch ? wazeMatch[1].trim() : '';
      
      console.log('🔗 Extracted data:', { name, address, distance, operatingHours, wazeLink });
      
      // Only add if we have at least name and address
      if (name && address) {
        outlets.push({
          name,
          address,
          distance,
          operatingHours,
          wazeLink
        });
      }
    } catch (error) {
      console.warn('Error parsing outlet block:', error);
      continue;
    }
  }
  
  console.log('📋 Final outlets:', outlets);
  return outlets.length > 0 ? outlets : null;
}

export function isOutletMessage(content: string): boolean {
  return content.includes('**McDonald\'s') && 
         (content.includes('**Address:**') || content.includes('Address:'));
} 