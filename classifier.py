import os

from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base, Transcript
from extractor import extract_transcript_info

# Load environment variables
load_dotenv()

def classify_transcript(transcript_name: str, transcript_data: str):
    # Database connection
    db_url = os.getenv('DATABASE_URL')
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    # Initialize the sentence transformer model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embedding = model.encode(transcript_data)

    classification = "unknown"
    similar_transcript = Transcript.find_similar_transcripts(embedding)
    if similar_transcript:
        classification = similar_transcript.classification
    else:
        # TODO: Get top X similar transcripts below threshold and use an LLM to check if it is still unclassified
        # TODO: Find new classification from unknown transcripts using HDBSCAN, use an LLM to validate the classification
        pass

    with Session(engine) as session:
        transcript = Transcript(
            file_name=transcript_name,
            transcript_data=transcript_data,
            classification=classification,
            embedding=embedding
        )
    session.add(transcript)
    session.commit()

    return classification


