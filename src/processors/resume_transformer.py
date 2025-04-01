from typing import Dict, Any, List
import re

def transform_parsed_resume(parsed_resume, skill_matches=None):
    """
    Transform the parsed resume into a format suitable for the template.
    
    Args:
        parsed_resume: The parsed resume from the parser
        skill_matches: Optional skill matching results
        
    Returns:
        Dictionary in the format expected by the template
    """
    sections = parsed_resume.get('sections', {})
    
    # Extract name from header
    name = ""
    if 'header' in sections:
        # Typically the name is on the first line
        header_lines = sections['header'].strip().split('\n')
        if header_lines:
            name = header_lines[0].strip()
    
    # Extract title/role
    title = ""
    if 'summary' in sections:
        # Title is often in the first line of summary
        summary_lines = sections['summary'].strip().split('\n')
        if summary_lines:
            title = summary_lines[0].strip()
    
    # Extract summary points
    summary_points = []
    if 'summary' in sections:
        # Split summary into bullet points by newlines or bullet characters
        summary_text = sections['summary']
        # Remove the first line if it was used as title
        if title and summary_text.startswith(title):
            summary_text = summary_text[len(title):].strip()
        
        # Split by bullets or newlines
        bullet_points = re.split(r'[\n•\-\*]+', summary_text)
        summary_points = [point.strip() for point in bullet_points if point.strip()]
    
    # Extract education
    education = []
    if 'education' in sections:
        edu_text = sections['education']
        # Split by blank lines or bullets
        edu_blocks = re.split(r'\n\s*\n+|(?:\n[\s]*[•\-\*])', edu_text)
        
        for block in edu_blocks:
            if not block.strip():
                continue
                
            # Try to extract degree, institution and year
            lines = block.strip().split('\n')
            if not lines:
                continue
                
            edu_entry = {'degree': '', 'institution': '', 'year': ''}
            
            # First line typically has degree and/or institution
            first_line = lines[0].strip()
            
            # Look for year in parentheses
            year_match = re.search(r'\((\d{4})\)', first_line)
            if year_match:
                edu_entry['year'] = year_match.group(1)
                first_line = first_line.replace(year_match.group(0), '').strip()
            
            # If there's a comma, it's likely "degree, institution"
            if ',' in first_line:
                degree, institution = first_line.split(',', 1)
                edu_entry['degree'] = degree.strip()
                edu_entry['institution'] = institution.strip()
            else:
                edu_entry['institution'] = first_line
            
            education.append(edu_entry)
    
    # Extract certifications
    certifications = []
    if 'certifications' in sections:
        cert_text = sections['certifications']
        # Split by bullets or newlines
        cert_lines = re.split(r'[\n•\-\*]+', cert_text)
        certifications = [cert.strip() for cert in cert_lines if cert.strip()]
    
    # Extract experience
    experience = []
    if 'experience' in sections:
        exp_text = sections['experience']
        # Split by multiple newlines which often indicate different jobs
        job_blocks = re.split(r'\n\s*\n+', exp_text)
        
        for block in job_blocks:
            if not block.strip():
                continue
                
            lines = block.strip().split('\n')
            if not lines:
                continue
                
            job = {
                'company': '',
                'location': '',
                'dates': '',
                'role': '',
                'bullets': []
            }
            
            # First line typically has company and possibly location
            if lines:
                first_line = lines[0].strip()
                if ',' in first_line:
                    company, location = first_line.split(',', 1)
                    job['company'] = company.strip()
                    job['location'] = location.strip()
                else:
                    job['company'] = first_line
            
            # Second line might have dates or role
            if len(lines) > 1:
                second_line = lines[1].strip()
                # Check if it looks like a date range
                if re.search(r'\d{4}|\d{2}/\d{2}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec', second_line):
                    job['dates'] = second_line
                    if len(lines) > 2:
                        job['role'] = lines[2].strip()
                else:
                    job['role'] = second_line
            
            # Look for bullets
            bullet_start = 3 if job['role'] else 2
            if job['dates']:
                bullet_start = 3 if job['role'] else 2
            else:
                bullet_start = 2 if job['role'] else 1
            
            bullets = []
            for line in lines[bullet_start:]:
                line = line.strip()
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    bullets.append(line[1:].strip())
                elif line:
                    bullets.append(line)
            
            job['bullets'] = bullets
            experience.append(job)
    
    # Extract skills
    skills = {}
    if 'skills' in sections:
        skills_text = sections['skills']
        
        # Try to identify categories
        skill_lines = skills_text.strip().split('\n')
        current_category = 'Technical Skills'  # Default category
        
        for line in skill_lines:
            line = line.strip()
            if not line:
                continue
                
            # If line ends with a colon, it's likely a category
            if line.endswith(':'):
                current_category = line[:-1].strip()
                skills[current_category] = []
            else:
                # If line starts with bullet, strip it
                if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                    line = line[1:].strip()
                
                # If category doesn't exist yet, create it
                if current_category not in skills:
                    skills[current_category] = []
                
                # Check if line contains multiple skills separated by commas
                if ',' in line:
                    skill_items = [s.strip() for s in line.split(',')]
                    skills[current_category].extend(skill_items)
                else:
                    skills[current_category].append(line)
    
    # If no categories found, use the entire skills section as one list
    if not skills and 'skills' in sections:
        skill_items = re.split(r'[\n,•\-\*]+', sections['skills'])
        clean_skills = [s.strip() for s in skill_items if s.strip()]
        if clean_skills:
            skills['Technical Skills'] = clean_skills
    
    # Create candidate data structure
    candidate_data = {
        'name': name,
        'title': title,
        'summary_points': summary_points,
        'education': education,
        'certifications': certifications,
        'experience': experience,
        'skills': skills
    }
    
    # Add skill assessment if available
    if skill_matches:
        candidate_data['skill_assessment'] = {
            'total_score': skill_matches['total_score'],
            'must_have': {
                'score': skill_matches['must_have']['score'],
                'matches': skill_matches['must_have']['matches'],
                'missing': skill_matches['must_have']['missing']
            },
            'nice_to_have': {
                'score': skill_matches['nice_to_have']['score'],
                'matches': skill_matches['nice_to_have']['matches']
            },
            'industry': {
                'score': skill_matches['industry']['score'],
                'matches': skill_matches['industry']['matches']
            },
            'education': {
                'present': skill_matches['education']['present'],
                'score': skill_matches['education']['score']
            }
        }
    
    return candidate_data