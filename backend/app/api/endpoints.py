from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from ..models.schemas import UserInputSchema, AudioTranscriptionResponse
from ..services.handler import TestMindHandler
import os
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the backend is running.
    """
    return JSONResponse(content={
        "status": "healthy",
        "message": "TestMind backend is running",
        "version": "1.0.0"
    })

@router.post("/transcribe-audio")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """
    Transcribe uploaded audio file to text.
    
    Supports various audio formats including WAV, MP3, M4A, etc.
    """
    try:
        allowed_extensions = {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.webm'}
        file_extension = os.path.splitext(audio_file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
            )

        audio_content = await audio_file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(audio_content)
            temp_file_path = temp_file.name
        
        try:
            if file_extension != '.wav':
                audio = AudioSegment.from_file(temp_file_path)
                wav_path = temp_file_path.replace(file_extension, '.wav')
                audio.export(wav_path, format='wav')
                os.unlink(temp_file_path)  # Delete original file
                temp_file_path = wav_path

            recognizer = sr.Recognizer()

            with sr.AudioFile(temp_file_path) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = recognizer.record(source)

            text = recognizer.recognize_google(audio_data)
            
            return AudioTranscriptionResponse(
                status="success",
                text=text,
                confidence=0.8
            )
            
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except sr.UnknownValueError:
        return AudioTranscriptionResponse(
            status="error",
            error_message="Could not understand the audio. Please try again with clearer speech."
        )
    except sr.RequestError as e:
        return AudioTranscriptionResponse(
            status="error",
            error_message=f"Speech recognition service error: {str(e)}"
        )
    except Exception as e:
        return AudioTranscriptionResponse(
            status="error",
            error_message=f"Error processing audio file: {str(e)}"
        )

@router.post("/mind")
async def conversation(user_input: UserInputSchema, request: Request):
    """
    Single endpoint for all TestMind interactions.
    
    This endpoint processes user input through the conversation agent to determine
    whether to continue the conversation or trigger matrix generation. It serves
    as the unified interface for all user interactions with the TestMind system.
    """
    try:
        conversation_context = request.session.get("conversation_context", {})

        handler = TestMindHandler(timeout=300)
        result = await handler.run(user_input.text, conversation_context=conversation_context)

        if "conversation_context" in result:
            request.session["conversation_context"] = result["conversation_context"]

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
                "matrix_data": result.get('matrix_data', {}),
                "matrix_statistics": result.get('matrix_statistics', {})
            }
        else:
            response = {
                "status": status,
                "error_message": result.get('message', 'Unknown error occurred')
            }
            
        return JSONResponse(content=response)
    except Exception:
        return JSONResponse(content={
            "status": "error",
            "error_message": "Sorry, something went wrong while processing your request. Please check your input or try again later."
        }, status_code=500)