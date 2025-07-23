"""
Conversation Manager

This module handles multi-turn conversation logic and context management
for the McDonald's Malaysia chatbot.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class ConversationManager:
    """
    Manages conversation flow and context for multi-turn conversations.
    
    This class handles:
    - Conversation state tracking
    - Context persistence across messages
    - Follow-up question handling
    - Conversation flow optimization
    """
    
    def __init__(self):
        """Initialize conversation manager."""
        self.conversation_states: Dict[str, Dict] = {}
        logger.info("Initialized ConversationManager")
    
    def initialize_conversation(self, session_id: str) -> Dict[str, Any]:
        """
        Initialize a new conversation state.
        
        Args:
            session_id: Chat session ID
            
        Returns:
            Initial conversation state
        """
        state = {
            "session_id": session_id,
            "current_context": None,
            "last_query_type": None,
            "user_location": None,
            "conversation_history": [],
            "follow_up_suggestions": [],
            "created_at": datetime.now(),
            "last_updated": datetime.now()
        }
        
        self.conversation_states[session_id] = state
        logger.info(f"Initialized conversation state for session: {session_id}")
        
        return state
    
    def update_conversation_state(self, session_id: str, message: str, response: str, 
                                context: Dict, user_location: Optional[Dict] = None):
        """
        Update conversation state after processing a message.
        
        Args:
            session_id: Chat session ID
            message: User message
            response: AI response
            context: Context used for the response
            user_location: Optional user location
        """
        if session_id not in self.conversation_states:
            self.initialize_conversation(session_id)
        
        state = self.conversation_states[session_id]
        
        # Update state
        state["current_context"] = context
        state["last_query_type"] = context.get("query_type")
        state["last_updated"] = datetime.now()
        
        # Update user location if provided
        if user_location:
            state["user_location"] = user_location
        
        # Add to conversation history
        state["conversation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "ai_response": response,
            "context_type": context.get("query_type"),
            "outlets_found": len(context.get("outlets", []))
        })
        
        # Keep only last 10 conversations for memory management
        if len(state["conversation_history"]) > 10:
            state["conversation_history"] = state["conversation_history"][-10:]
        
        # Generate follow-up suggestions
        state["follow_up_suggestions"] = self._generate_follow_up_suggestions(context, state)
        
        logger.info(f"Updated conversation state for session: {session_id}")
    
    def get_conversation_state(self, session_id: str) -> Optional[Dict]:
        """
        Get current conversation state.
        
        Args:
            session_id: Chat session ID
            
        Returns:
            Conversation state or None if not found
        """
        return self.conversation_states.get(session_id)
    
    def get_contextual_information(self, session_id: str) -> Dict[str, Any]:
        """
        Get contextual information for enhancing responses.
        
        Args:
            session_id: Chat session ID
            
        Returns:
            Contextual information dictionary
        """
        state = self.conversation_states.get(session_id)
        if not state:
            return {}
        
        return {
            "has_location": state.get("user_location") is not None,
            "user_location": state.get("user_location"),
            "last_query_type": state.get("last_query_type"),
            "conversation_length": len(state.get("conversation_history", [])),
            "follow_up_suggestions": state.get("follow_up_suggestions", [])
        }
    
    def _generate_follow_up_suggestions(self, context: Dict, state: Dict) -> List[str]:
        """
        Generate follow-up suggestions based on current context.
        
        Args:
            context: Current context
            state: Conversation state
            
        Returns:
            List of follow-up suggestions
        """
        suggestions = []
        query_type = context.get("query_type")
        outlets = context.get("outlets", [])
        
        if query_type == "nearby" and outlets:
            suggestions.extend([
                "Get directions to the nearest one",
                "Show me operating hours",
                "Find 24-hour McDonald's nearby"
            ])
        
        elif query_type == "location_search" and outlets:
            suggestions.extend([
                "Which one is closest to me?",
                "Show me all operating hours",
                "Get directions to any of these"
            ])
        
        elif query_type == "hours" and outlets:
            suggestions.extend([
                "Find the nearest one",
                "Show me 24-hour locations",
                "Get directions"
            ])
        
        elif query_type == "24_hours" and outlets:
            suggestions.extend([
                "Which one is closest to me?",
                "Get directions to the nearest 24-hour location",
                "Show me all 24-hour McDonald's"
            ])
        
        elif query_type == "general":
            suggestions.extend([
                "Find nearest McDonald's",
                "Show me 24-hour locations",
                "McDonald's near KLCC"
            ])
        
        # Add location-based suggestions if no location provided
        if not state.get("user_location"):
            suggestions.append("Share your location for better recommendations")
        
        # Remove duplicates and limit to 3 suggestions
        unique_suggestions = list(dict.fromkeys(suggestions))
        return unique_suggestions[:3]
    
    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Get a summary of the conversation.
        
        Args:
            session_id: Chat session ID
            
        Returns:
            Conversation summary
        """
        state = self.conversation_states.get(session_id)
        if not state:
            return {"error": "Session not found"}
        
        history = state.get("conversation_history", [])
        
        # Analyze conversation patterns
        query_types = [msg.get("context_type") for msg in history if msg.get("context_type")]
        most_common_query = max(set(query_types), key=query_types.count) if query_types else "general"
        
        total_outlets_found = sum(msg.get("outlets_found", 0) for msg in history)
        
        return {
            "session_id": session_id,
            "total_messages": len(history),
            "most_common_query_type": most_common_query,
            "total_outlets_found": total_outlets_found,
            "has_user_location": state.get("user_location") is not None,
            "session_duration": (datetime.now() - state["created_at"]).total_seconds() / 60,  # minutes
            "last_activity": state["last_updated"].isoformat(),
            "current_suggestions": state.get("follow_up_suggestions", [])
        }
    
    def cleanup_expired_sessions(self, timeout_hours: int = 24):
        """
        Clean up expired conversation sessions.
        
        Args:
            timeout_hours: Hours after which to consider sessions expired
        """
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, state in self.conversation_states.items():
            last_updated = state.get("last_updated", state.get("created_at"))
            if (current_time - last_updated).total_seconds() > (timeout_hours * 3600):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.conversation_states[session_id]
            logger.info(f"Cleaned up expired session: {session_id}")
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired conversation sessions")
    
    def get_active_sessions_count(self) -> int:
        """Get count of active conversation sessions."""
        return len(self.conversation_states)
    
    def reset_conversation(self, session_id: str) -> bool:
        """
        Reset conversation state for a session.
        
        Args:
            session_id: Chat session ID
            
        Returns:
            True if reset successful, False otherwise
        """
        if session_id in self.conversation_states:
            self.initialize_conversation(session_id)
            logger.info(f"Reset conversation state for session: {session_id}")
            return True
        return False 