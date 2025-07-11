"""
Chat Service with Function Calling

This module provides the main chat service that coordinates between
the Gemini client with function calling capabilities to provide intelligent responses.
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from .gemini_client import GeminiClient
from ..database.operations import DatabaseOperations

logger = logging.getLogger(__name__)

class ChatService:
    """
    Main chat service with function calling capabilities.
    
    This service handles:
    - Chat session management with function calling
    - Message processing and routing
    - Intelligent function selection via Gemini
    - Response generation with real-time data
    """
    
    def __init__(self, db_operations: DatabaseOperations, gemini_api_key: Optional[str] = None):
        """
        Initialize chat service with function calling.
        
        Args:
            db_operations: Database operations instance
            gemini_api_key: Optional Gemini API key
        """
        self.db = db_operations
        self.gemini_client = GeminiClient(gemini_api_key)
        
        # In-memory session storage (in production, use Redis or database)
        self.active_sessions: Dict[str, Dict] = {}
        self.session_timeout = timedelta(hours=24)
        
        logger.info("Initialized ChatService with function calling")
    
    async def create_session(self) -> Dict[str, Any]:
        """
        Create a new chat session with function calling capabilities.
        
        Returns:
            Session information dictionary
        """
        session_id = str(uuid.uuid4())
        
        try:
            # Create Gemini chat session with function calling tools
            gemini_session = self.gemini_client.create_chat_session(session_id, self.db)
            
            # Store session info
            session_info = {
                "session_id": session_id,
                "created_at": datetime.now(),
                "last_activity": datetime.now(),
                "message_count": 0,
                "gemini_session": gemini_session,
                "status": "active",
                "function_calling_enabled": True
            }
            
            self.active_sessions[session_id] = session_info
            
            logger.info(f"Created chat session with function calling: {session_id}")
            
            return {
                "session_id": session_id,
                "created_at": session_info["created_at"].isoformat(),
                "status": "active",
                "welcome_message": self._get_welcome_message()
            }
            
        except Exception as e:
            logger.error(f"Failed to create chat session: {str(e)}")
            raise
    
    async def send_message(self, session_id: str, message: str, user_location: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Send a message and get AI response with function calling.
        
        Args:
            session_id: Chat session ID
            message: User message
            user_location: Optional user location {"lat": float, "lng": float}
            
        Returns:
            Response dictionary with AI response and metadata
        """
        try:
            # Get or validate session
            session = await self._get_session(session_id)
            if not session:
                raise ValueError(f"Invalid session ID: {session_id}")
            
            # Check for special commands
            if message.lower() in ["/help", "help"]:
                return {
                    "response": self._get_help_text(),
                    "session_id": session_id,
                    "message_type": "help"
                }
            
            # Log location data for debugging
            if user_location:
                logger.info(f"✅ Received user location: {user_location}")
                logger.info(f"✅ Location keys: {list(user_location.keys()) if isinstance(user_location, dict) else 'Not a dict'}")
                logger.info(f"✅ Location type: {type(user_location)}")
            else:
                logger.info(f"❌ No user location provided (user_location is {user_location})")
            
            # Send message to Gemini with function calling (no manual context needed)
            ai_response = self.gemini_client.send_message(
                session["gemini_session"],
                message,
                user_location
            )
            
            # Update session activity
            session["last_activity"] = datetime.now()
            session["message_count"] += 1
            
            logger.info(f"Processed message with function calling in session {session_id}")
            
            return {
                "response": ai_response,
                "session_id": session_id,
                "message_type": "response",
                "context_used": "function_calling",
                "function_calling_enabled": True
            }
            
        except Exception as e:
            logger.error(f"Failed to process message: {str(e)}")
            return {
                "response": "I'm sorry, I encountered an error processing your message. Please try again.",
                "session_id": session_id,
                "message_type": "error",
                "error": str(e)
            }
    
    async def get_session_history(self, session_id: str) -> Dict[str, Any]:
        """
        Get chat history for a session.
        
        Args:
            session_id: Chat session ID
            
        Returns:
            Session history dictionary
        """
        try:
            session = await self._get_session(session_id)
            if not session:
                raise ValueError(f"Invalid session ID: {session_id}")
            
            return {
                "session_id": session_id,
                "created_at": session["created_at"].isoformat(),
                "last_activity": session["last_activity"].isoformat(),
                "message_count": session["message_count"],
                "messages": [],  # Simplified - no database storage for now
                "function_calling_enabled": session.get("function_calling_enabled", False)
            }
            
        except Exception as e:
            logger.error(f"Failed to get session history: {str(e)}")
            raise
    
    async def delete_session(self, session_id: str) -> Dict[str, Any]:
        """
        Delete a chat session.
        
        Args:
            session_id: Chat session ID
            
        Returns:
            Deletion result
        """
        try:
            # Remove from active sessions
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
            
            logger.info(f"Deleted chat session: {session_id}")
            
            return {
                "session_id": session_id,
                "status": "deleted",
                "message": "Chat session deleted successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to delete session: {str(e)}")
            raise
    
    async def cleanup_expired_sessions(self):
        """
        Clean up expired sessions from memory.
        """
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            if current_time - session["last_activity"] > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
            logger.info(f"Cleaned up expired session: {session_id}")
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    async def _get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get session from memory or database.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session dictionary or None
        """
        # Check memory first
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            
            # Check if expired
            if datetime.now() - session["last_activity"] > self.session_timeout:
                del self.active_sessions[session_id]
                return None
                
            return session
        
        return None
    
    def _get_welcome_message(self) -> str:
        """
        Get welcome message for new sessions.
        
        Returns:
            Welcome message string
        """
        return """🍟 Welcome to McDonald's Malaysia Assistant!

I can help you with:
• 📍 Finding nearby McDonald's outlets
• 🔍 Searching for specific locations  
• 🕐 Getting operating hours and details
• 🗺️ Providing directions and navigation
• 📊 Information about outlet coverage

Just ask me anything like:
• "Find McDonald's near me"
• "McDonald's in KLCC"
• "What time does McDonald's open?"
• "How many outlets are there?"

I have access to real-time data and can help in English or Bahasa Malaysia! 🚀"""
    
    def _get_help_text(self) -> str:
        """
        Get help text for the chatbot.
        
        Returns:
            Help text string
        """
        return """🤖 McDonald's Malaysia Assistant Help

**What I can do:**
• Find nearby McDonald's outlets using your location
• Search for specific outlets by name or area
• Get detailed information about outlets (hours, address, directions)
• Provide database statistics and coverage information
• Help with navigation using Waze links

**How to use:**
• **Location queries**: "Find McDonald's near me", "McDonald's within 2km"
• **Search queries**: "McDonald's KLCC", "McDonald's in Pavilion"
• **Details**: "What time does McDonald's open?", "Get directions to McDonald's"
• **General**: "How many outlets are there?", "What areas do you cover?"

**Features:**
• Real-time data access through intelligent functions
• Support for both English and Bahasa Malaysia
• Distance calculations and sorting
• Waze navigation integration
• Fast responses with function calling

**Tips:**
• Share your location for better nearby results
• Be specific with outlet names for better search results
• Ask follow-up questions for more details

Need more help? Just ask! 🍟"""
    
    def get_service_info(self) -> Dict[str, Any]:
        """
        Get service information and statistics.
        
        Returns:
            Service information dictionary
        """
        return {
            "service_name": "McDonald's Malaysia Chat Assistant",
            "version": "2.0.0",
            "function_calling_enabled": True,
            "features": [
                "Real-time outlet data access",
                "Intelligent function calling",
                "Location-based search",
                "Multi-language support",
                "Fast response times"
            ],
            "active_sessions": len(self.active_sessions),
            "gemini_model": self.gemini_client.get_model_info(),
            "available_functions": [
                "find_nearby_outlets",
                "search_outlets",
                "get_outlet_details", 
                "get_outlet_stats",
                "get_api_health"
            ]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.
        
        Returns:
            Health check result
        """
        try:
            # Check Gemini client
            gemini_health = self.gemini_client.health_check()
            
            # Check database
            db_health = await self.db.health_check()
            
            # Overall status
            overall_healthy = (
                gemini_health.get("status") == "healthy" and
                db_health.get("status") == "healthy"
            )
            
            return {
                "status": "healthy" if overall_healthy else "unhealthy",
                "service": "McDonald's Malaysia Chat Service",
                "function_calling_enabled": True,
                "gemini": gemini_health,
                "database": db_health,
                "active_sessions": len(self.active_sessions),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "service": "McDonald's Malaysia Chat Service",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            } 