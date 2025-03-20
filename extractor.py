from collections import namedtuple
import os
import json
from pathlib import Path

import google.generativeai as genai
from PIL import Image
import pdf2image
from llm import gemini_model

Course = namedtuple('Course', ['code', 'description'])

def convert_pdf_to_images(pdf_path):
    """Convert PDF pages to a list of PIL Images."""
    return pdf2image.convert_from_path(pdf_path)

def extract_course_info(file_path) -> list[Course]:
    """Extract course codes and descriptions from a PDF or image file."""
    file_path = Path(file_path)
    
    # Prepare the images
    if file_path.suffix.lower() == '.pdf':
        images = convert_pdf_to_images(file_path)
    else:
        images = [Image.open(file_path)]
    
    courses = []
    
    for img in images:
        # Prompt engineering for better extraction
        prompt = """
        Extract all course codes and their descriptions from this transcript image.
        Format the output as a list of JSON objects with 'code' and 'description' fields.
        Example format:
        [
            {"code": "MATH101", "description": "Introduction to Calculus"},
            {"code": "PHYS200", "description": "Classical Mechanics"}
        ]
        Only include actual courses, ignore any other text.
        """
        
        response = gemini_model.generate_content([prompt, img])
        
        try:
            # Extract the JSON part from the response
            response_text = response.text
            # Find the JSON array in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                page_courses = json.loads(json_str)
                courses.extend(page_courses)
        except Exception as e:
            print(f"Error processing page: {e}")
            continue
    
    return [Course(code=course['code'], description=course['description']) for course in courses]


def extract_transcript_info(file_path) -> str:
    """Extract transcript information from a PDF or image file."""
    file_path = Path(file_path)
    
    # Prepare the images
    if file_path.suffix.lower() == '.pdf':
        images = convert_pdf_to_images(file_path)
    else:
        images = [Image.open(file_path)]
    
    prompt = """
    Analyze this transcript image and classify it based on these specific criteria.
    Provide your analysis in this exact JSON format:

    {
        "institution": {
            "name": "string or N/A",
            "code": "string or N/A",
            "confidence": "high|medium|low",
            "location": "where in document"
        },
        "format": {
            "style": "traditional|modern|minimalist|detailed",
            "term_organization": "semester|quarter|year|continuous",
            "grade_display": "letter|percentage|both|other",
            "course_arrangement": "chronological|subject_grouped|other",
            "confidence": "high|medium|low"
        },
        "structure": {
            "layout": "traditional_vertical|grid_based|multi_column|modern",
            "main_sections": [
                {
                    "name": "section name",
                    "position": "top|middle|bottom|left|right",
                    "format": "table|text|list"
                }
            ],
            "visual_elements": {
                "has_letterhead": true|false,
                "has_watermark": true|false,
                "has_seal": true|false,
                "has_security_features": true|false
            }
        }
    }

    Important:
    - Only include information you can see - use "N/A" for missing items
    - For institution, look for official school name and any institutional codes
    - For format, analyze the transcript's style and organization of information
    - For structure, analyze the physical layout and organization
    - Maintain exact JSON structure with these fields
    """
    
    response = gemini_model.generate_content([prompt, *images])
        
    try:
        response_text = response.text
    except Exception as e:
        print(f"Error processing: {e}")

    
    return response_text