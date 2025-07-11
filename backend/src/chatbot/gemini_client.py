"""
Google Gemini 2.5 Flash Client with Function Calling

This module provides a client for interacting with Google's Gemini 2.5 Flash model
using the new Google Gen AI SDK (2025) with function calling capabilities.
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

try:
    import google.genai as genai
except ImportError:
    genai = None
    logging.warning("google-genai not installed. Please install: pip install google-genai")

# Import synchronous API functions for function calling
from .sync_api_functions import (
    sync_find_nearby_outlets,
    sync_search_outlets,
    sync_get_outlet_details,
    sync_get_outlet_stats,
    sync_get_api_health
)

logger = logging.getLogger(__name__)

@dataclass
class ChatMessage:
    """Represents a chat message"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[str] = None

class GeminiClient:
    """
    Client for Google Gemini 2.5 Flash model with function calling.
    
    This client handles:
    - Gemini API authentication
    - Chat session management with function calling tools
    - Message generation with intelligent function selection
    - Error handling and retries
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client with function calling capabilities.
        
        Args:
            api_key: Gemini API key. If None, reads from GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable or api_key parameter required")
        
        if genai is None:
            raise ImportError("google-genai package not installed. Please install: pip install google-genai")
        
        # Initialize the client
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"
        
        # McDonald's specific system instruction with function calling guidance
        self.system_instruction = """
You are a helpful McDonald's Malaysia assistant with access to real-time outlet data through intelligent functions.

🍟 AVAILABLE FUNCTIONS:
- find_nearby_outlets: Find outlets near GPS coordinates (use for location-based queries)
- search_outlets: Search by name/address (use for specific outlet searches)  
- get_outlet_details: Get specific outlet info (use for hours, details, directions)
- get_outlet_stats: Get general database info (use for coverage/total questions)
- get_api_health: Check system health (use for technical issues)

🎯 FUNCTION USAGE GUIDELINES:
- ALWAYS use functions to get current data instead of guessing
- When user location is provided in the message, IMMEDIATELY use find_nearby_outlets
- For "near me" queries: AUTOMATICALLY call find_nearby_outlets with provided coordinates
- For specific outlets: use search_outlets first, then get_outlet_details
- For "how many" questions: use get_outlet_stats
- For operating hours: use get_outlet_details with outlet ID
- For system issues: use get_api_health
- NEVER ask for location if coordinates are already provided in the message

📍 LOCATION HANDLING:
- If message contains "User location: X.XXXXX, Y.YYYYY" → IMMEDIATELY use those coordinates
- For "Find McDonald's near me" with location → call find_nearby_outlets(lat, lng, 2.0, 20)
- For "McDonald's within Xkm" with location → call find_nearby_outlets(lat, lng, X, 20)
- For "closest McDonald's" with location → call find_nearby_outlets(lat, lng, 2.0, 5)
- DO NOT ask user to provide location if it's already in the message

📋 FUNCTION PARAMETERS:
- find_nearby_outlets: Use radius=2.0 (default), limit=20 (default) unless user specifies
- search_outlets: Use limit=10 (default) unless user requests more
- When user says "near me" without radius: use radius=2.0
- When user says "within Xkm": use radius=X
- When user wants "closest" or "nearest": use limit=5
- When user wants specific number: use that as limit

🗣️ COMMUNICATION STYLE:
- Be friendly and customer service oriented
- Support both English and Bahasa Malaysia
- Provide helpful, accurate information about McDonald's Malaysia
- When functions fail, explain the issue and suggest alternatives
- Always prioritize user experience and helpfulness

🏪 OUTLET INFORMATION:
You have access to McDonald's outlets in Kuala Lumpur, Malaysia, including:
- Outlet names and addresses
- Operating hours
- GPS coordinates for distance calculations
- Waze navigation links
- Real-time availability data

Remember: Always call the appropriate function first to get current data, then provide helpful responses based on the results.
"""
        
        logger.info(f"Initialized Gemini client with function calling: {self.model_name}")
    
    def create_chat_session(self, session_id: str, db_ops: Any) -> Dict[str, Any]:
        """
        Create a new chat session with Gemini 2.5 Flash and function calling tools.
        
        Args:
            session_id: Unique identifier for the chat session
            db_ops: Database operations instance for function calling
            
        Returns:
            Dict containing chat session information
        """
        try:
            # Create synchronous bound functions with db_ops
            def bound_find_nearby_outlets(latitude: float, longitude: float, radius: float, limit: int) -> Dict[str, Any]:
                """Find McDonald's outlets near coordinates. Use for location-based queries like 'find McDonald's near me'."""
                logger.info(f"🎯 bound_find_nearby_outlets called with: lat={latitude}, lng={longitude}, radius={radius}, limit={limit}")
                try:
                    result = sync_find_nearby_outlets(db_ops, latitude, longitude, radius, limit)
                    logger.info(f"🎯 bound_find_nearby_outlets result: success={result.get('success')}")
                    return result
                except Exception as e:
                    import traceback
                    logger.error(f"bound_find_nearby_outlets error: {str(e)}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    return {"success": False, "error": f"Function execution error: {str(e)}"}
            
            def bound_search_outlets(search_query: str, limit: int) -> Dict[str, Any]:
                """Search McDonald's outlets by name or address. Use for specific outlet searches like 'McDonald's KLCC'."""
                try:
                    return sync_search_outlets(db_ops, search_query, limit)
                except Exception as e:
                    import traceback
                    logger.error(f"bound_search_outlets error: {str(e)}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    return {"success": False, "error": f"Function execution error: {str(e)}"}
            
            def bound_get_outlet_details(outlet_id: int) -> Dict[str, Any]:
                """Get detailed information for a specific outlet. Use when you need hours, address, or directions."""
                try:
                    return sync_get_outlet_details(db_ops, outlet_id)
                except Exception as e:
                    import traceback
                    logger.error(f"bound_get_outlet_details error: {str(e)}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    return {"success": False, "error": f"Function execution error: {str(e)}"}
            
            def bound_get_outlet_stats() -> Dict[str, Any]:
                """Get database statistics. Use for questions about total outlets or coverage."""
                try:
                    return sync_get_outlet_stats(db_ops)
                except Exception as e:
                    import traceback
                    logger.error(f"bound_get_outlet_stats error: {str(e)}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    return {"success": False, "error": f"Function execution error: {str(e)}"}
            
            def bound_get_api_health() -> Dict[str, Any]:
                """Check API health. Use for technical issues or system status."""
                try:
                    return sync_get_api_health(db_ops)
                except Exception as e:
                    import traceback
                    logger.error(f"bound_get_api_health error: {str(e)}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    return {"success": False, "error": f"Function execution error: {str(e)}"}
            
            # Test the synchronous bound functions to ensure they work
            logger.info("🧪 Testing synchronous bound functions...")
            try:
                test_result = bound_find_nearby_outlets(3.1570, 101.7123, 2.0, 5)
                logger.info(f"🧪 Sync bound function test result: {test_result.get('success', False)}")
                if test_result.get('success'):
                    logger.info(f"🧪 Test found {len(test_result.get('data', {}).get('outlets', []))} outlets")
                else:
                    logger.error(f"🧪 Sync bound function test failed: {test_result.get('error')}")
            except Exception as e:
                logger.error(f"🧪 Sync bound function test exception: {str(e)}")

            # Create chat session with function calling tools
            chat = self.client.chats.create(
                model=self.model_name,
                config=genai.types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.7,  # Balanced creativity and consistency
                    max_output_tokens=1500,  # Increased for function calling responses
                    tools=[
                        bound_find_nearby_outlets,
                        bound_search_outlets,
                        bound_get_outlet_details,
                        bound_get_outlet_stats,
                        bound_get_api_health
                    ]
                )
            )
            
            logger.info(f"Created chat session with function calling: {session_id}")
            
            return {
                "session_id": session_id,
                "chat": chat,
                "message_count": 0,
                "status": "active",
                "db_ops": db_ops,
                "function_calling_enabled": True
            }
            
        except Exception as e:
            logger.error(f"Failed to create chat session {session_id}: {str(e)}")
            raise
    
    def send_message(self, chat_session: Dict[str, Any], message: str, user_location: Optional[Dict] = None) -> str:
        """
        Send a message to Gemini with function calling support.
        
        Args:
            chat_session: Chat session from create_chat_session
            message: User message
            user_location: Optional user location {lat, lng}
            
        Returns:
            AI response string
        """
        try:
            chat = chat_session["chat"]
            
            # Add location context if provided
            enhanced_message = message
            if user_location:
                enhanced_message = f"User location: {user_location['lat']}, {user_location['lng']}\n\n{message}"
            
            # Send message to Gemini (functions will be called automatically)
            response = chat.send_message(enhanced_message)
            
            # Update message count
            chat_session["message_count"] += 1
            
            logger.info(f"Sent message to session {chat_session['session_id']}, got response with function calling")
            
            return response.text
            
        except Exception as e:
            logger.error(f"Failed to send message with function calling: {str(e)}")
            return "I'm sorry, I encountered an error while processing your request. Please try again or ask a different question."
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the Gemini model with function calling.
        
        Returns:
            Model information dictionary
        """
        return {
            "model_name": self.model_name,
            "provider": "Google Gemini",
            "version": "2.5 Flash",
            "function_calling": True,
            "features": [
                "Fast response times",
                "Cost-effective",
                "Multi-turn conversations",
                "Context awareness",
                "Multilingual support",
                "Function calling capabilities",
                "Real-time data access"
            ],
            "available_functions": [
                "find_nearby_outlets",
                "search_outlets", 
                "get_outlet_details",
                "get_outlet_stats",
                "get_api_health"
            ]
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if Gemini API is accessible with function calling.
        
        Returns:
            Health check result
        """
        try:
            # Try to create a simple chat session without functions
            test_chat = self.client.chats.create(
                model=self.model_name,
                config=genai.types.GenerateContentConfig(
                    system_instruction="You are a test assistant.",
                    max_output_tokens=10
                )
            )
            
            # Send a simple test message
            response = test_chat.send_message("Hello")
            
            return {
                "status": "healthy",
                "model": self.model_name,
                "response_received": bool(response.text),
                "api_accessible": True,
                "function_calling_ready": True
            }
            
        except Exception as e:
            logger.error(f"Gemini health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "model": self.model_name,
                "error": str(e),
                "api_accessible": False,
                "function_calling_ready": False
            } 