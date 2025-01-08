from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import whisper
import os
from typing import Optional
import shutil
from pathlib import Path
import time
from datetime import datetime

# Criar diretório para arquivos temporários
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

# Configurações
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB em bytes
ALLOWED_EXTENSIONS = {'.wav', '.mp3', '.flac'}

# Inicializar a aplicação FastAPI
app = FastAPI(
    title="API de Transcrição de Áudio",
    description="API para transcrição de arquivos de áudio usando Whisper",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar modelo Whisper
model = whisper.load_model("base")

class ProcessingTime:
    def __init__(self):
        self.start_time = None
        self.steps = {}
        
    def start(self):
        self.start_time = time.time()
        self.steps = {}
        
    def add_step(self, step_name: str):
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.steps[step_name] = {
            "timestamp": datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S'),
            "elapsed_seconds": round(elapsed, 2)
        }
        
    def get_summary(self):
        if not self.steps:
            return {}
            
        total_time = time.time() - self.start_time
        steps_with_duration = {}
        
        previous_time = self.start_time
        for step_name, step_data in self.steps.items():
            current_time = datetime.strptime(step_data["timestamp"], '%Y-%m-%d %H:%M:%S').timestamp()
            duration = round(current_time - previous_time, 2)
            steps_with_duration[step_name] = {
                **step_data,
                "step_duration": duration
            }
            previous_time = current_time
            
        return {
            "steps": steps_with_duration,
            "total_time_seconds": round(total_time, 2)
        }

@app.post("/api/v1/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    model_size: Optional[str] = "base"
):
    """
    Endpoint para transcrição de áudio.
    Aceita arquivos nos formatos .wav, .mp3 e .flac
    """
    processing_time = ProcessingTime()
    processing_time.start()
    
    try:
        # Validar extensão do arquivo
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Formato de arquivo não suportado. Use: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        processing_time.add_step("validação_formato")
        
        # Validar tamanho do arquivo
        contents = await file.read()
        file_size = len(contents)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo muito grande. Tamanho máximo permitido: {MAX_FILE_SIZE/1024/1024}MB"
            )
        processing_time.add_step("validação_tamanho")
        
        try:
            # Criar arquivo temporário
            temp_file = TEMP_DIR / f"temp_{file.filename}"
            with open(temp_file, "wb") as f:
                f.write(contents)
            processing_time.add_step("salvamento_arquivo")
            
            # Carregar modelo Whisper
            model = whisper.load_model(model_size)
            processing_time.add_step("carregamento_modelo")
            
            # Realizar transcrição
            result = model.transcribe(str(temp_file))
            processing_time.add_step("transcrição")
            
            # Remover arquivo temporário
            os.remove(temp_file)
            processing_time.add_step("limpeza")
            
            # Preparar resposta
            timing_summary = processing_time.get_summary()
            
            return {
                "filename": file.filename,
                "text": result["text"],
                "status": "success",
                "processing_time": timing_summary
            }
            
        except Exception as e:
            # Garantir que o arquivo temporário seja removido em caso de erro
            if temp_file.exists():
                os.remove(temp_file)
            raise HTTPException(status_code=500, detail=str(e))
            
    except Exception as e:
        processing_time.add_step("erro")
        timing_summary = processing_time.get_summary()
        return {
            "status": "error",
            "detail": str(e),
            "processing_time": timing_summary
        }

@app.get("/")
async def root():
    """Endpoint de verificação de saúde da API"""
    return {"status": "online", "message": "API de Transcrição de Áudio"}
