from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from typing import Optional
import os
import time

from src.core.transcriber import AudioTranscriber
from src.utils.helpers import (
    validate_audio_file, 
    get_temp_path, 
    clean_temp_files, 
    ensure_output_dir,
    check_ffmpeg,
    setup_directories
)
from loguru import logger

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize FastAPI app
app = FastAPI(
    title="Audio Transcription API",
    description="API for transcribing audio files using Whisper",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Initialize directories
REQUIRED_DIRS = [
    BASE_DIR / "input",
    BASE_DIR / "output",
    BASE_DIR / "logs",
    BASE_DIR / "models"
]
setup_directories(REQUIRED_DIRS)

# Initialize transcriber
transcriber = AudioTranscriber(model_name="base")

@app.on_event("startup")
async def startup_event():
    """Verify system requirements on startup"""
    if not check_ffmpeg():
        logger.error("FFmpeg not found. Please install FFmpeg.")
        raise RuntimeError("FFmpeg not found")
    logger.info("Application started successfully")

@app.get("/")
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(
    file: UploadFile,
    model: str = "base",
    language: Optional[str] = "pt"
):
    """
    Handle audio file upload and transcription
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        temp_path = get_temp_path(file.filename)
        
        # Save uploaded file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        if not validate_audio_file(temp_path):
            os.remove(temp_path)
            raise HTTPException(
                status_code=400,
                detail="Invalid audio file. Supported formats: .mp3, .wav, .m4a"
            )
        
        # Process transcription immediately instead of background
        try:
            start_time = time.time()
            result = await process_transcription(
                temp_path,
                file.filename,
                model,
                language
            )
            end_time = time.time()
            processing_time = round(end_time - start_time, 2)
            
            return JSONResponse({
                "message": "Transcrição concluída com sucesso",
                "filename": file.filename,
                "transcription": result["text"] if result else "Não foi possível transcrever o áudio",
                "processing_time": processing_time
            })
            
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_transcription(
    temp_path: Path,
    original_filename: str,
    model: str,
    language: str
):
    """
    Process audio transcription
    """
    try:
        # Transcribe audio
        result = transcriber.transcribe(
            str(temp_path),
            language=language
        )
        
        # Save transcription to file
        output_path = ensure_output_dir(original_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        logger.info(f"Transcription completed: {output_path}")
        return result
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        return None

@app.get("/system-info")
async def get_system_info():
    """Get system information including GPU availability"""
    return transcriber.get_system_info()

@app.get("/models")
async def get_available_models():
    """Get list of available Whisper models"""
    return {"models": transcriber.get_available_models()}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
