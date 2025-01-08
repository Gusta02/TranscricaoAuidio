import os
import shutil
from pathlib import Path
from typing import Union, List
import subprocess
from loguru import logger
import sys

# Configure logger
logger.remove()
logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(sys.stderr, level="INFO")

def setup_directories(dirs: List[Union[str, Path]]) -> None:
    """
    Create necessary directories if they don't exist.
    
    Args:
        dirs (List[Union[str, Path]]): List of directory paths to create
    """
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ensured: {dir_path}")

def safe_delete_file(file_path: Union[str, Path]) -> bool:
    """
    Safely delete a file with logging.
    
    Args:
        file_path: Path to file to delete
        
    Returns:
        bool: True if deletion was successful
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Successfully deleted file: {file_path}")
            return True
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")
    return False

def check_ffmpeg() -> bool:
    """
    Check if FFmpeg is installed and accessible.
    
    Returns:
        bool: True if FFmpeg is available
    """
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        logger.info("FFmpeg is available")
        return True
    except FileNotFoundError:
        logger.error("FFmpeg not found in system PATH")
        return False

def validate_audio_file(file_path: Union[str, Path]) -> bool:
    """
    Validate audio file format and existence.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        bool: True if file is valid
    """
    valid_extensions = {'.mp3', '.wav', '.m4a'}
    file_path = Path(file_path)
    
    if not file_path.exists():
        logger.error(f"File does not exist: {file_path}")
        return False
        
    if file_path.suffix.lower() not in valid_extensions:
        logger.error(f"Invalid file format: {file_path.suffix}")
        return False
        
    return True

def get_temp_path(filename: str) -> Path:
    """
    Generate temporary file path.
    
    Args:
        filename: Original filename
        
    Returns:
        Path: Path object for temporary file
    """
    temp_dir = Path("input")
    return temp_dir / f"temp_{filename}"

def clean_temp_files(directory: Union[str, Path]) -> None:
    """
    Clean temporary files from specified directory.
    
    Args:
        directory: Directory to clean
    """
    try:
        directory = Path(directory)
        for file in directory.glob("temp_*"):
            safe_delete_file(file)
        logger.info(f"Cleaned temporary files in {directory}")
    except Exception as e:
        logger.error(f"Error cleaning temporary files: {str(e)}")

def ensure_output_dir(filename: str) -> Path:
    """
    Ensure output directory exists and generate output path.
    
    Args:
        filename: Original filename
        
    Returns:
        Path: Path object for output file
    """
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    return output_dir / f"{Path(filename).stem}_transcription.txt"
