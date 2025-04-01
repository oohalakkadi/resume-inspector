from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseParser(ABC):
    """Base interface for document parsers."""
    
    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        """
        Parse document and extract structured content.
        
        Returns:
            Dict with normalized resume sections
        """
        pass