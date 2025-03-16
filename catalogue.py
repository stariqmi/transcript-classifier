import json
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Catalogue
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

def _generate_catalogue_embeddings():
    # Load environment variables
    load_dotenv()

    # Initialize the sentence transformer model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Database connection
    db_url = os.getenv('DATABASE_URL')
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    # Load course data
    with open('computer_science.json', 'r') as f:
        data = json.load(f)

    # Process each course
    with Session(engine) as session:
        for course in data['courses']:
            # Generate embedding from description only
            text_to_embed = course['description']
            
            # Generate embedding
            embedding = model.encode(text_to_embed)
            
            # Create catalogue entry
            catalogue_entry = Catalogue(
                course_code=course['course_code'],
                description=course['description'],
                embedding=embedding
            )
            
            # Add to session
            session.merge(catalogue_entry)  # merge instead of add to handle duplicates
        
        # Commit all changes
        session.commit()

    print("Course embeddings have been generated and saved to the database.")

def find_similar_courses(description: str, n: int = 5):
    """
    Find the top n similar courses given a course description.
    
    Args:
        description (str): The course description to compare against
        n (int): Number of similar courses to return (default: 5)
    
    Returns:
        list: List of tuples containing (course_code, description, similarity_score)
    """
    # Load environment variables and initialize model
    load_dotenv()
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # Generate embedding for the input description
    query_embedding = model.encode(description)
    
    # Connect to database
    db_url = os.getenv('DATABASE_URL')
    engine = create_engine(db_url)
    
    # Query all courses
    with Session(engine) as session:
        courses = session.query(Catalogue).all()
        
        # Calculate similarity scores
        similarities = []
        for course in courses:
            # Calculate cosine similarity
            similarity = cosine_similarity(
                query_embedding.reshape(1, -1), 
                course.embedding.reshape(1, -1)
            )
            similarities.append((
                course.course_code,
                course.description,
                float(similarity[0][0])  # sklearn returns a 2D array
            ))
        
        # Sort by similarity score in descending order
        similarities.sort(key=lambda x: x[2], reverse=True)
        
        # Return top n results
        return similarities[:n]
