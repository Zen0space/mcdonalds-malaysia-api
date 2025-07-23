"""
Chat API Routes

This module provides FastAPI endpoints for the McDonald's Malaysia chatbot
using Google Gemini 2.5 Flash.
"""

import logging
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from ..chatbot.chat_service import ChatService
from ..chatbot.api_functions import find_nearby_outlets, search_outlets, get_outlet_details, get_outlet_stats
from ..database.operations import DatabaseOperations
from .dependencies import get_database_operations

logger = logging.getLogger(__name__)

# Router for chat endpoints
chat_router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

# Pydantic models for request/response validation
class ChatSessionRequest(BaseModel):
    """Request model for creating a chat session."""
    pass

class ChatSessionResponse(BaseModel):
    """Response model for chat session creation."""
    session_id: str = Field(..., description="Unique session identifier")
    created_at: str = Field(..., description="Session creation timestamp")
    status: str = Field(..., description="Session status")
    welcome_message: str = Field(..., description="Welcome message for the user")

class ChatMessageRequest(BaseModel):
    """Request model for sending a chat message."""
    message: str = Field(..., description="User message", min_length=1, max_length=1000)
    session_id: str = Field(..., description="Chat session ID")
    user_location: Optional[Dict[str, float]] = Field(None, description="Optional user location {lat, lng}")

class ChatMessageResponse(BaseModel):
    """Response model for chat message."""
    response: str = Field(..., description="AI response")
    session_id: str = Field(..., description="Chat session ID")
    message_type: str = Field(..., description="Type of message (response, help, error)")
    context_used: Optional[str] = Field(None, description="Type of context used")
    outlets_found: Optional[int] = Field(None, description="Number of outlets found")
    follow_up_suggestions: Optional[List[str]] = Field(None, description="Follow-up suggestions")

class ChatHistoryResponse(BaseModel):
    """Response model for chat history."""
    session_id: str = Field(..., description="Chat session ID")
    created_at: str = Field(..., description="Session creation timestamp")
    last_activity: str = Field(..., description="Last activity timestamp")
    message_count: int = Field(..., description="Total message count")
    messages: List[Dict[str, Any]] = Field(..., description="Message history")

class ChatDeleteResponse(BaseModel):
    """Response model for chat session deletion."""
    session_id: str = Field(..., description="Chat session ID")
    status: str = Field(..., description="Deletion status")
    message: str = Field(..., description="Deletion message")

class ChatHealthResponse(BaseModel):
    """Response model for chat service health check."""
    status: str = Field(..., description="Health status")
    service: str = Field(..., description="Service name")
    gemini: Dict[str, Any] = Field(..., description="Gemini API health")
    database: Dict[str, Any] = Field(..., description="Database health")
    active_sessions: int = Field(..., description="Number of active sessions")
    timestamp: str = Field(..., description="Health check timestamp")

class TestFunctionRequest(BaseModel):
    """Request model for testing API functions."""
    function_name: str = Field(..., description="Name of the function to test")
    parameters: Dict[str, Any] = Field(..., description="Function parameters")

class TestFunctionResponse(BaseModel):
    """Response model for function testing."""
    function_name: str = Field(..., description="Name of the tested function")
    success: bool = Field(..., description="Whether the function executed successfully")
    result: Optional[Dict[str, Any]] = Field(None, description="Function result")
    error: Optional[str] = Field(None, description="Error message if failed")

# Global chat service instance for session persistence
_chat_service_instance: Optional[ChatService] = None

# Dependency to get chat service
def get_chat_service(db_ops: DatabaseOperations = Depends(get_database_operations)) -> ChatService:
    """
    Get ChatService singleton instance with database operations.
    
    Args:
        db_ops: Database operations dependency
        
    Returns:
        ChatService singleton instance
    """
    global _chat_service_instance
    if _chat_service_instance is None:
        _chat_service_instance = ChatService(db_ops)
    return _chat_service_instance

@chat_router.post("/session", response_model=ChatSessionResponse)
async def create_chat_session(
    request: ChatSessionRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    🆕 Create a new chat session.
    
    Creates a new chat session with Google Gemini 2.5 Flash and returns
    session information along with a welcome message.
    
    **Returns:**
    - Session ID for subsequent messages
    - Welcome message with usage instructions
    - Session creation timestamp
    
    **Example Usage:**
    ```
    POST /api/v1/chat/session
    ```
    """
    try:
        session_info = await chat_service.create_session()
        return ChatSessionResponse(**session_info)
    except Exception as e:
        logger.error(f"Failed to create chat session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create chat session: {str(e)}"
        )

@chat_router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    request: ChatMessageRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    💬 Send a message to the McDonald's Malaysia chatbot.
    
    Send a message to the AI assistant and get intelligent responses about
    McDonald's outlets, locations, operating hours, and directions.
    
    **Features:**
    - Location-based outlet search
    - Operating hours information
    - Distance calculations
    - Waze navigation links
    - Multi-language support (English/Malay)
    
    **Special Commands:**
    - `help` or `/help` - Show help information
    
    **Example Messages:**
    - "Find nearest McDonald's"
    - "McDonald's near KLCC"
    - "24-hour McDonald's"
    - "What time does McDonald's open?"
    - "Directions to McDonald's"
    
    **Parameters:**
    - **message**: Your question or request
    - **session_id**: Chat session ID from `/session` endpoint
    - **user_location**: Optional location {lat: 3.139, lng: 101.6869}
    
    **Returns:**
    - AI response with outlet information
    - Context type used for the response
    - Number of outlets found
    - Follow-up suggestions
    """
    try:
        response = await chat_service.send_message(
            session_id=request.session_id,
            message=request.message,
            user_location=request.user_location
        )
        
        # Add follow-up suggestions if available
        if hasattr(chat_service, 'conversation_manager'):
            contextual_info = chat_service.conversation_manager.get_contextual_information(request.session_id)
            response["follow_up_suggestions"] = contextual_info.get("follow_up_suggestions", [])
        
        return ChatMessageResponse(**response)
    except ValueError as e:
        logger.warning(f"Invalid session ID: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to process message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )

@chat_router.get("/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    📝 Get chat history for a session.
    
    Retrieve the complete conversation history for a chat session,
    including timestamps, message counts, and session metadata.
    
    **Parameters:**
    - **session_id**: Chat session ID
    
    **Returns:**
    - Complete message history
    - Session metadata (created_at, last_activity, message_count)
    - Conversation statistics
    
    **Example Usage:**
    ```
    GET /api/v1/chat/history/{session_id}
    ```
    """
    try:
        history = await chat_service.get_session_history(session_id)
        return ChatHistoryResponse(**history)
    except ValueError as e:
        logger.warning(f"Invalid session ID: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to get chat history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat history: {str(e)}"
        )

@chat_router.delete("/session/{session_id}", response_model=ChatDeleteResponse)
async def delete_chat_session(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    🗑️ Delete a chat session.
    
    Permanently delete a chat session and all associated conversation history.
    This action cannot be undone.
    
    **Parameters:**
    - **session_id**: Chat session ID to delete
    
    **Returns:**
    - Deletion confirmation
    - Session status
    
    **Example Usage:**
    ```
    DELETE /api/v1/chat/session/{session_id}
    ```
    """
    try:
        result = await chat_service.delete_session(session_id)
        return ChatDeleteResponse(**result)
    except Exception as e:
        logger.error(f"Failed to delete session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}"
        )

@chat_router.get("/health", response_model=ChatHealthResponse)
async def chat_health_check(
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    🏥 Check chat service health.
    
    Perform a comprehensive health check on the chat service,
    including Gemini API connectivity, database status, and service metrics.
    
    **Returns:**
    - Overall service health status
    - Gemini API connectivity status
    - Database connectivity status
    - Active session count
    - Service metrics
    
    **Example Usage:**
    ```
    GET /api/v1/chat/health
    ```
    """
    try:
        health_status = await chat_service.health_check()
        return ChatHealthResponse(**health_status)
    except Exception as e:
        logger.error(f"Chat health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat health check failed: {str(e)}"
        )

@chat_router.get("/info")
async def get_chat_service_info(
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    ℹ️ Get chat service information.
    
    Get detailed information about the chat service capabilities,
    features, and current statistics.
    
    **Returns:**
    - Service information
    - Model details (Gemini 2.5 Flash)
    - Available features
    - Session statistics
    
    **Example Usage:**
    ```
    GET /api/v1/chat/info
    ```
    """
    try:
        service_info = chat_service.get_service_info()
        return {
            "🤖 McDonald's Malaysia Chatbot": service_info,
            "📖 Documentation": {
                "endpoints": [
                    "POST /api/v1/chat/session - Create new chat session",
                    "POST /api/v1/chat/message - Send message to chatbot",
                    "GET /api/v1/chat/history/{session_id} - Get chat history",
                    "DELETE /api/v1/chat/session/{session_id} - Delete session",
                    "GET /api/v1/chat/health - Health check",
                    "GET /api/v1/chat/info - Service information"
                ],
                "example_queries": [
                    "Find nearest McDonald's",
                    "McDonald's near KLCC",
                    "24-hour McDonald's",
                    "What time does McDonald's open?",
                    "Directions to McDonald's"
                ]
            }
        }
    except Exception as e:
        logger.error(f"Failed to get service info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get service info: {str(e)}"
        ) 

@chat_router.post("/test-function", response_model=TestFunctionResponse)
async def test_api_function(
    request: TestFunctionRequest,
    db_ops: DatabaseOperations = Depends(get_database_operations)
):
    """
    🧪 Test individual API functions.
    
    Test the chatbot's API functions individually for debugging and validation.
    This endpoint allows testing each function with specific parameters.
    
    **Available Functions:**
    - `find_nearby_outlets` - Find outlets near coordinates
    - `search_outlets` - Search outlets by query
    - `get_outlet_details` - Get details for specific outlet
    - `get_outlet_stats` - Get database statistics
    
    **Example Usage:**
    ```json
    {
        "function_name": "find_nearby_outlets",
        "parameters": {
            "latitude": 3.1570,
            "longitude": 101.7123,
            "radius": 2,
            "limit": 5
        }
    }
    ```
    
    **Returns:**
    - Function execution result
    - Success/failure status
    - Error details if failed
    """
    try:
        function_map = {
            'find_nearby_outlets': find_nearby_outlets,
            'search_outlets': search_outlets,
            'get_outlet_details': get_outlet_details,
            'get_outlet_stats': get_outlet_stats
        }
        
        if request.function_name not in function_map:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown function: {request.function_name}. Available: {list(function_map.keys())}"
            )
        
        function = function_map[request.function_name]
        
        # Call the function with the provided parameters (these are NOW async functions)
        result = await function(db_ops, **request.parameters)
        
        return TestFunctionResponse(
            function_name=request.function_name,
            success=True,
            result=result
        )
        
    except TypeError as e:
        logger.error(f"Invalid parameters for {request.function_name}: {str(e)}")
        return TestFunctionResponse(
            function_name=request.function_name,
            success=False,
            error=f"Invalid parameters: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error testing function {request.function_name}: {str(e)}")
        return TestFunctionResponse(
            function_name=request.function_name,
            success=False,
            error=str(e)
        ) 