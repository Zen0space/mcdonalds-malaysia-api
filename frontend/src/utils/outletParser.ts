export interface OutletInfo {
  name: string;
  address: string;
  distance: string;
  operatingHours: string;
  wazeLink: string;
}

export function parseOutletInfo(content: string): OutletInfo[] | null {
  // Check if this looks like outlet information
  if (!content.includes('**McDonald\'s') || !content.includes('**Address:**')) {
    return null;
  }

  const outlets: OutletInfo[] = [];
  
  // Split by outlet entries starting with **McDonald's
  const outletBlocks = content.split(/(?=\*\*McDonald's)/);
  
  for (const block of outletBlocks) {
    if (!block.trim() || !block.includes('**McDonald\'s')) continue;
    
    try {
      // Extract name (line with **McDonald's)
      const nameMatch = block.match(/\*\*(McDonald's[^*]+)\*\*/);
      const name = nameMatch ? nameMatch[1].trim() : '';
      
      // Extract address (after **Address:**)
      const addressMatch = block.match(/\*\*Address:\*\*\s*([^\n*]+(?:\n[^*\n]+)*)/);
      const address = addressMatch ? addressMatch[1].trim().replace(/\n/g, ' ') : '';
      
      // Extract distance (after **Distance:**)
      const distanceMatch = block.match(/\*\*Distance:\*\*\s*([^\n*]+)/);
      const distance = distanceMatch ? distanceMatch[1].trim() : '';
      
      // Extract operating hours (after **Operating Hours:**)
      const hoursMatch = block.match(/\*\*Operating Hours:\*\*\s*([^\n*]+)/);
      const operatingHours = hoursMatch ? hoursMatch[1].trim() : '';
      
      // Extract Waze link (after **Waze Link:**)
      const wazeMatch = block.match(/\*\*Waze Link:\*\*\s*(https?:\/\/[^\s]+)/);
      const wazeLink = wazeMatch ? wazeMatch[1].trim() : '';
      
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
  
  return outlets.length > 0 ? outlets : null;
}

export function isOutletMessage(content: string): boolean {
  return content.includes('**McDonald\'s') && content.includes('**Address:**');
} 