from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import List, Optional, Dict
import tempfile
import os
from pathlib import Path
import shutil

# Import our modules
from src.parsers.parser_factory import get_parser
from src.processors.skill_matcher import SkillMatcher
from src.processors.resume_transformer import transform_parsed_resume
from src.formatters.dynamic_resume_formatter import DynamicResumeFormatter

app = FastAPI(title="Resume Inspector AI")

# Create necessary directories
data_dir = Path(__file__).parent.parent.parent / "data"
output_dir = data_dir / "output"
output_dir.mkdir(exist_ok=True, parents=True)

@app.post("/process-resume")
async def process_resume(
    resume_file: UploadFile = File(...),
    must_have_skills: str = Form(None),
    nice_to_have_skills: Optional[str] = Form(None),
    industry_experience: Optional[str] = Form(None)
):
    """
    Process a resume file and evaluate against required skills.
    
    Args:
        resume_file: The resume file (.pdf, .docx)
        must_have_skills: Comma-separated list of required skills
        nice_to_have_skills: Comma-separated list of nice-to-have skills
        industry_experience: Comma-separated list of required industry experience
        
    Returns:
        JSON response with scoring results and a link to the formatted resume
    """
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.filename)[1]) as temp_file:
        temp_file_path = temp_file.name
        shutil.copyfileobj(resume_file.file, temp_file)
    
    try:
        # Parse resume
        parser = get_parser(temp_file_path)
        parsed_resume = parser.parse()
        
        # Process skills if provided
        skill_matches = None
        if must_have_skills:
            # Convert comma-separated strings to lists
            must_have_list = [s.strip() for s in must_have_skills.split(',') if s.strip()]
            nice_to_have_list = [s.strip() for s in (nice_to_have_skills or "").split(',') if s.strip()]
            industry_list = [s.strip() for s in (industry_experience or "").split(',') if s.strip()]
            
            # Match skills
            matcher = SkillMatcher()
            skill_matches = matcher.match_skills(
                parsed_resume['raw_text'], 
                must_have_list,
                nice_to_have_list,
                industry_list
            )
        
        # Transform parsed resume into candidate data format
        candidate_data = transform_parsed_resume(parsed_resume, skill_matches)
        
        # Format resume
        formatter = DynamicResumeFormatter()
        
        # Create output file
        name_part = candidate_data['name'].replace(' ', '_') if candidate_data['name'] else 'formatted'
        output_filename = f"{name_part}_resume.docx"
        output_path = output_dir / output_filename
        
        # Format and save the resume
        formatter.format_resume(candidate_data, str(output_path))
        
        # Prepare response
        response = {
            "filename": output_filename,
            "download_url": f"/download/{output_filename}",
            "candidate_name": candidate_data['name']
        }
        
        if skill_matches:
            response["skill_assessment"] = {
                "total_score": skill_matches["total_score"],
                "must_have_score": skill_matches["must_have"]["score"],
                "nice_to_have_score": skill_matches["nice_to_have"]["score"],
                "industry_score": skill_matches["industry"]["score"],
                "education_score": skill_matches["education"]["score"],
                "missing_must_have": skill_matches["must_have"]["missing"]
            }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download a processed resume file.
    
    Args:
        filename: Name of the file to download
        
    Returns:
        The requested file for download
    """
    file_path = output_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(file_path), filename=filename)