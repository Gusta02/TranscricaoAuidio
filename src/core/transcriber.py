import whisper
import torch
from pathlib import Path
from loguru import logger
import numpy as np
from typing import Optional, Dict, Any

class AudioTranscriber:
    def __init__(self, model_name: str = "base", device: Optional[str] = None):
        """
        Initialize the AudioTranscriber with specified model and device.
        
        Args:
            model_name (str): Whisper model name ('tiny', 'base', 'small', 'medium', 'large')
            device (str, optional): Device to use ('cuda' if GPU available, else 'cpu')
        """
        self.model_name = model_name
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Initializing AudioTranscriber with model: {model_name} on device: {self.device}")
        
        # Load model with optimized settings
        self.model = self._load_model()
        
    def _load_model(self) -> whisper.Whisper:
        """Load and configure the Whisper model with optimized settings."""
        try:
            model = whisper.load_model(
                self.model_name,
                device=self.device,
                download_root=str(Path("models").absolute())
            )
            
            # Enable half-precision if using CUDA
            if self.device == "cuda":
                model = model.half()
            
            return model
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def transcribe(self, audio_path: str, **kwargs) -> Dict[str, Any]:
        """
        Transcribe audio file with optimized settings.
        
        Args:
            audio_path (str): Path to audio file
            **kwargs: Additional arguments for whisper.transcribe()
            
        Returns:
            Dict containing transcription results
        """
        try:
            logger.info(f"Starting transcription of: {audio_path}")
            
            # Default optimized parameters
            default_params = {
                "fp16": True if self.device == "cuda" else False,
                "language": "pt",  # Default to Portuguese
                "task": "transcribe",
                "verbose": None
            }
            
            # Update with user parameters
            params = {**default_params, **kwargs}
            
            # Perform transcription
            result = self.model.transcribe(audio_path, **params)
            
            logger.success(f"Transcription completed successfully for: {audio_path}")
            return result
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            raise

    def get_available_models(self) -> list:
        """Return list of available Whisper models."""
        return ["tiny", "base", "small", "medium", "large"]

    def get_system_info(self) -> Dict[str, Any]:
        """Return system information including GPU availability and current settings."""
        return {
            "device": self.device,
            "model": self.model_name,
            "cuda_available": torch.cuda.is_available(),
            "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "cuda_device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
        }
