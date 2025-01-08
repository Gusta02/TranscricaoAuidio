import whisper
import torch
from pathlib import Path
from loguru import logger
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
        self.load_model()

    def load_model(self):
        """Carrega o modelo Whisper"""
        try:
            self.model = whisper.load_model(self.model_name)
            logger.info(f"Modelo {self.model_name} carregado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            raise

    def transcribe(self, audio_path: str) -> dict:
        """
        Transcreve o áudio e aplica correções personalizadas.
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            Dict containing transcription results
        """
        try:
            result = self.model.transcribe(audio_path)
            
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
