from docxtpl import DocxTemplate
from pathlib import Path
import datetime
import os

class DynamicResumeFormatter:
    """Formats resume data into Buxton's standard format using a docxtpl template."""
    
    def __init__(self, template_path=None):
        # Default template path is in the data/templates folder
        if template_path is None:
            template_path = Path(__file__).parent.parent.parent / "data" / "templates" / "Buxton_Template.docx"
        self.template_path = Path(template_path)
        
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
    
    def format_resume(self, candidate_data, output_path=None):
        """
        Format resume according to Buxton's standard format.
        
        Args:
            candidate_data: Dictionary containing candidate information
            output_path: Path to save the formatted resume
            
        Returns:
            Path to the formatted resume file
        """
        # Create template context
        context = {
            'candidate': candidate_data,
            'current_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Load the template
        doc = DocxTemplate(self.template_path)
        
        # Render the template with our context
        doc.render(context)
        
        # If no output path provided, create one in the output directory
        if output_path is None:
            output_dir = Path(__file__).parent.parent.parent / "data" / "output"
            output_dir.mkdir(exist_ok=True, parents=True)
            output_path = output_dir / f"{candidate_data['name'].replace(' ', '_')}_Resume.docx"
        
        # Save the document
        doc.save(output_path)
        
        return output_path