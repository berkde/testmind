from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..models.schemas import UserInputSchema
from ..services.handler import TestMindHandler
import os

router = APIRouter()

@router.post("/mind")
async def conversation(user_input: UserInputSchema):
    """
    Single endpoint for all TestMind interactions.
    
    This endpoint processes user input through the conversation agent to determine
    whether to continue the conversation or trigger matrix generation. It serves
    as the unified interface for all user interactions with the TestMind system.
    """
    try:
        handler = TestMindHandler(timeout=300)
        result = await handler.run(user_input.text)

        status = result.get('status', 'unknown')
        
        if status == 'conversation':
            response = {
                "status": "conversation",
                "response": result.get('response', 'No response available'),
                "conversation_context": result.get('conversation_context', {})
            }
        elif status == 'success':
            response = {
                "status": "success",
                "summary": result.get('summary', 'No summary available'),
                "recommendations": result.get('recommendations', None),
                "matrix_data": result.get('matrix_data', {})
            }
        else:
            response = {
                "status": status,
                "error_message": result.get('message', 'Unknown error occurred')
            }
            
        return JSONResponse(content=response)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={
            "status": "error",
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }, status_code=500)