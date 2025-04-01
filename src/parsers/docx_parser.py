from docx import Document
from pathlib import Path
import re
from typing import Dict, Any

from .base_parser import BaseParser

class DocxParser(BaseParser):
    """Parser for DOCX resume documents."""
    
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        
    def parse(self) -> Dict[str, Any]:
        """Parse DOCX resume and extract structured content."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
            
        # Load document
        doc = Document(self.file_path)
        
        # Extract full text
        paragraphs = [para.text for para in doc.paragraphs]
        full_text = "\n".join(paragraphs)
        
        # Identify sections 
        sections = self._identify_sections(paragraphs)
        
        return {
            'raw_text': full_text,
            'sections': sections
        }
    
    def _identify_sections(self, paragraphs) -> Dict[str, str]:
        """Identify common resume sections by analyzing text."""
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
        
        sections = {}
        current_section = 'header'  # Default section
        section_content = []
        
        for para in paragraphs:
            text = para.strip()
            if not text:
                continue
                
            # Check if paragraph is a section header
            matched_section = None
            for section, pattern in section_patterns.items():
                if re.search(pattern, text):
                    matched_section = section
                    break
            
            if matched_section:
                # Save previous section content
                if section_content:
                    sections[current_section] = '\n'.join(section_content)
                # Start new section
                current_section = matched_section
                section_content = []
            else:
                section_content.append(text)
        
        # Save the last section
        if section_content:
            sections[current_section] = '\n'.join(section_content)
            
        return sections