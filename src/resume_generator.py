from formatters.dynamic_resume_formatter import DynamicResumeFormatter
from pathlib import Path

def main():
    # Sample candidate data
    candidate = {
        'name': 'Jane Doe',
        'title': 'Senior Salesforce Developer',
        'summary_points': [
            'Has 18+ years of experience as a Sr. Technical Program/ Project Manager/ Scrum Master in the IT industry in all aspects of Program Management / Project  Management in requirements gathering,  design, architecture, application administration, installation, implementation, documentation, maintenance operations, release management and production support.',
            'Certified Salesforce Administrator, Developer, and Consultant',
            'Expertise in CPQ implementations and complex pricing configurations',
            'Strong background in healthcare and SaaS industry integrations'
        ],
        'education': [
            {
                'degree': 'Master of Computer Science',
                'institution': 'Stanford University',
                'year': '2015'
            },
            {
                'degree': 'Bachelor of Science in Information Technology',
                'institution': 'University of California, Berkeley',
                'year': '2013'
            }
        ],
        'certifications': [
            'Salesforce Certified Platform Developer II',
            'Salesforce Certified Administrator',
            'Salesforce Certified CPQ Specialist',
            'Agile Scrum Master Certified',
            'AWS Certified Solutions Architect'
        ],
        'experience': [
            {
                'company': 'Cloudforce Solutions',
                'location': 'San Francisco, CA',
                'dates': 'Jan 2022 - Present',
                'role': 'Senior Salesforce Developer',
                'bullets': [
                    'Lead a team of 5 developers implementing complex CPQ solutions for healthcare clients',
                    'Architected and deployed custom pricing engines that reduced quote generation time by 65%',
                    'Developed integration between Salesforce and EHR systems using MuleSoft',
                    'Implemented automated testing framework that improved code coverage to 92%'
                ]
            },
            {
                'company': 'TechHealth Systems',
                'location': 'Boston, MA',
                'dates': 'Mar 2019 - Dec 2021',
                'role': 'Salesforce Developer',
                'bullets': [
                    'Built custom patient management system on Salesforce Health Cloud',
                    'Designed and implemented automated approval workflows for insurance verification',
                    'Created Lightning Web Components for patient intake process',
                    'Integrated Salesforce with legacy billing systems using REST APIs'
                ]
            },
            {
                'company': 'Global SaaS Innovations',
                'location': 'Austin, TX',
                'dates': 'Jun 2017 - Feb 2019',
                'role': 'CRM Developer',
                'bullets': [
                    'Implemented Salesforce Sales Cloud for a team of 50+ sales representatives',
                    'Developed custom sales forecasting dashboards',
                    'Created automated lead routing and scoring system',
                    'Built integration between Salesforce and NetSuite using Dell Boomi'
                ]
            }
        ],
        'skills': {
            'Salesforce.com': ['Sales Cloud', 'Service Cloud', 'Health Cloud', 'Experience Cloud', 'Lightning Component Framework'],
            'CPQ': ['Salesforce CPQ', 'Custom Product Configurator', 'Advanced Pricing Rules', 'Approval Workflows'],
            'Development': ['Apex', 'JavaScript', 'LWC', 'Aura', 'SOQL', 'SOSL', 'API Integration'],
            'PMO': ['Agile Methodology', 'Scrum', 'JIRA', 'Confluence', 'Release Management']
        }
    }
    
    # Create the formatter
    formatter = DynamicResumeFormatter()
    
    # Generate the resume
    output_path = formatter.format_resume(candidate)
    
    print(f"Resume generated successfully: {output_path}")

if __name__ == "__main__":
    main()