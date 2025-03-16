from extractor import Course, extract_course_info
from catalogue import find_similar_courses
from llm import gemini_model

def evaluate_transcript(transcript: str):
    courses = extract_course_info(transcript)
    transcript_data = "";
    for course in courses:
        transcript_data += f"Course: {course.code}\n"
        transcript_data += f"Description: {course.description}\n"
        similar_courses = find_similar_courses(course.description)

        transcript_data += "\nSimilar courses:\n"
        for course_code, desc, _similarity in similar_courses:
            transcript_data += f"Course: {course_code}\n"
            transcript_data += f"Description: {desc}\n"

    # Evaluate transfer credits using LLM
    prompt = f"""Given the following transcript information, evaluate if the student qualifies for transfer credits.
    Consider course similarities and content overlap. Provide a clear yes/no recommendation for each course.
    
    {transcript_data}"""
    
    evaluation = gemini_model.generate_content(prompt).text
    return "\nTransfer Credit Evaluation:\n" + evaluation
