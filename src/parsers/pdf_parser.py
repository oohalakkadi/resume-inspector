import pdfplumber
from pathlib import Path
import re
from typing import Dict, Any

from .base_parser import BaseParser

class PDFParser(BaseParser):
    """Parser for PDF resume documents."""
    
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        
    def parse(self) -> Dict[str, Any]:
        """Parse PDF resume and extract structured content."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
            
        # Extract text from PDF
        text = self._extract_text()
        
        # Identify sections using common headers
        sections = self._identify_sections(text)
        
        return {
            'raw_text': text,
            'sections': sections
        }
    
    def _extract_text(self) -> str:
        """Extract text from PDF document."""
        with pdfplumber.open(self.file_path) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages)
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify common resume sections."""
        # Common section headers in resumes
        section_patterns = {
            'summary': r'(?i)(SUMMARY|PROFESSIONAL\s+SUMMARY|PROFILE|OBJECTIVE)',
            'experience': r'(?i)(EXPERIENCE|WORK\s+EXPERIENCE|PROFESSIONAL\s+EXPERIENCE|EMPLOYMENT)',
            'education': r'(?i)(EDUCATION|ACADEMIC|QUALIFICATIONS)',
            'skills': r'(?i)(SKILLS|TECHNICAL\s+SKILLS|CORE\s+COMPETENCIES|COMPETENCIES)',
            'certifications': r'(?i)(CERTIFICATIONS|CERTIFICATES|ACCREDITATIONS)',
            'projects': r'(?i)(PROJECTS|KEY\s+PROJECTS)',
            'references': r'(?i)(REFERENCES)',
            'languages': r'(?i)(LANGUAGES|LANGUAGE\s+PROFICIENCY)',
            'awards': r'(?i)(AWARDS|HONORS|ACHIEVEMENTS)'
        }
        
        # Split text by common section headers
        sections = {}
        current_section = 'header'  # Default section
        section_text = []
        
        lines = text.split('\n')
        for line in lines:
            # Check if line matches any section pattern
            matched_section = None
            for section, pattern in section_patterns.items():
                if re.search(pattern, line):
                    matched_section = section
                    break
                    
            if matched_section:
                # Save previous section
                if section_text:
                    sections[current_section] = '\n'.join(section_text)
                # Start new section
                current_section = matched_section
                section_text = []
            else:
                section_text.append(line)
                
        # Save the last section
        if section_text:
            sections[current_section] = '\n'.join(section_text)
            
        return sections