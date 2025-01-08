from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks, Request, Form
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
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload and transcription"""
    try:
        # Validate file
        if not file.filename.lower().endswith(('.mp3', '.wav', '.m4a')):
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado")

        # Save file temporarily
        temp_file = Path("input") / file.filename
        temp_file.parent.mkdir(exist_ok=True)
        
        try:
            contents = await file.read()
            temp_file.write_bytes(contents)
            
            # Start transcription with timing
            start_time = time.time()
            
            transcription_result = transcriber.transcribe(
                str(temp_file),
                language="pt",
                task="transcribe"
            )
            
            processing_time = time.time() - start_time
            
            # Add processing time to result
            transcription_result["processing_time"] = round(processing_time, 2)
            
            return transcription_result
            
        finally:
            # Cleanup
            if temp_file.exists():
                temp_file.unlink()
                
    except Exception as e:
        logger.error(f"Erro na transcrição: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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

@app.post("/add-correction")
async def add_correction(wrong: str = Form(...), correct: str = Form(...)):
    """Adiciona uma nova correção ao dicionário personalizado"""
    try:
        transcriber.add_correction(wrong, correct)
        return {"status": "success", "message": f"Correção adicionada: '{wrong}' -> '{correct}'"}
    except Exception as e:
        logger.error(f"Erro ao adicionar correção: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/correction-stats")
async def get_correction_stats():
    """Retorna estatísticas sobre as correções aplicadas"""
    try:
        return transcriber.get_correction_stats()
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))
