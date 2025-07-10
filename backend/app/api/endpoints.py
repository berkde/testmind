from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..models.schemas import UserInputSchema
from ..services.handler import TestMindHandler
import os

router = APIRouter()

@router.post("/generate-matrix")
async def generate_matrix(user_input: UserInputSchema):
    try:
        handler = TestMindHandler(timeout=300)
        result = await handler.run(user_input.text)

        status = result.get('status', 'success' if result.get('matrix_data') else 'unknown')
        summary = result.get('summary', 'No summary available')
        recommendations = result.get('recommendations', None)
        matrix_data = result.get('matrix_data', {})

        response = {
            "status": status,
            "summary": summary,
            "recommendations": recommendations,
            "matrix_data": matrix_data,
        }
        if status == 'error':
            response["error_message"] = result.get('message', 'Unknown error occurred')
        return JSONResponse(content=response)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={
            "status": "error",
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }, status_code=500)