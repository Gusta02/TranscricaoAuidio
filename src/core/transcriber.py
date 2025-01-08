import whisper
import torch
from pathlib import Path
from loguru import logger
from typing import Dict, Any, Optional
from ..utils.text_processor import TextProcessor

class AudioTranscriber:
    def __init__(self, model_name: str = "base"):
        """
        Initialize the AudioTranscriber with specified model.
        
        Args:
            model_name (str): Whisper model name ('tiny', 'base', 'small', 'medium', 'large')
        """
        self.model = None
        self.model_name = model_name
        self.text_processor = TextProcessor()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.load_model()

    def load_model(self):
        """Carrega o modelo Whisper"""
        try:
            self.model = whisper.load_model(self.model_name)
            logger.info(f"Modelo {self.model_name} carregado com sucesso no dispositivo {self.device}")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            raise

    def transcribe(self, audio_path: str, **kwargs) -> Dict[str, Any]:
        """
        Transcreve o áudio e aplica correções personalizadas.
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            Dict containing transcription results
        """
        try:
            # Configurações padrão
            default_params = {
                "language": "pt",
                "task": "transcribe",
                "fp16": self.device == "cuda"
            }

            # Mescla com os parâmetros fornecidos
            params = {**default_params, **kwargs}
            
            # Realiza a transcrição
            result = self.model.transcribe(audio_path, **params)
            
            # Aplica correções ao texto transcrito
            original_text = result["text"]
            corrected_text = self.text_processor.apply_corrections(original_text)
            
            # Adiciona sugestões de correções
            suggestions = self.text_processor.suggest_corrections(corrected_text)
            
            return {
                "original_text": original_text,
                "corrected_text": corrected_text,
                "suggestions": suggestions,
                "language": result.get("language", ""),
                "confidence": result.get("confidence", 0)
            }
        except Exception as e:
            logger.error(f"Erro na transcrição: {e}")
            raise

    def add_correction(self, wrong: str, correct: str):
        """Adiciona uma nova correção ao dicionário"""
        self.text_processor.add_correction(wrong, correct)

    def get_correction_stats(self):
        """Retorna estatísticas sobre as correções"""
        return self.text_processor.get_statistics()

    def get_available_models(self):
        """Retorna lista de modelos disponíveis"""
        return ["tiny", "base", "small", "medium", "large"]

    def get_system_info(self) -> Dict[str, Any]:
        """Retorna informações do sistema"""
        return {
            "device": self.device,
            "model": self.model_name,
            "cuda_available": torch.cuda.is_available(),
            "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "cuda_device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
        }
