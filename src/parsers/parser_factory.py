from pathlib import Path
from typing import Union

from .base_parser import BaseParser
from .pdf_parser import PDFParser
from .docx_parser import DocxParser

def get_parser(file_path: Union[str, Path]) -> BaseParser:
    """
    Factory function to get appropriate parser based on file extension.
    
    Args:
        file_path: Path to the resume file
        
    Returns:
        Appropriate parser instance for the file type
        
    Raises:
        ValueError: If file type is not supported
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
        
    extension = file_path.suffix.lower()
    
    if extension == '.pdf':
        return PDFParser(file_path)
    elif extension in ['.docx', '.doc']:
        return DocxParser(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")