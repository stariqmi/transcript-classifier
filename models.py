from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Catalogue(Base):
    __tablename__ = 'catalogue'

    course_code = Column(String, primary_key=True)
    description = Column(Text)
    embedding = Column(Vector(384))  # sentence-transformers/all-MiniLM-L6-v2

    def __repr__(self):
        return f"<Course {self.course_code}>"


class Transcript(Base):
    __tablename__ = 'transcripts'

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    transcript_data = Column(Text)
    classification = Column(String)
    embedding = Column(Vector(384))  # sentence-transformers/all-MiniLM-L6-v2

    @classmethod
    def find_similar_transcripts(cls, embedding, threshold=0.2) -> 'Transcript':
        """Find similar transcripts using cosine distance.
        
        Args:
            embedding: The vector to compare against
            threshold: Maximum cosine distance (default 0.2, equivalent to 0.8 cosine similarity)
            
        Returns:
            The most similar transcript, or None if none found within threshold
        """
        from sqlalchemy import select
        from sqlalchemy.orm import Session
        from sqlalchemy import create_engine
        import os
        
        engine = create_engine(os.getenv('DATABASE_URL'))
        with Session(engine) as session:
            stmt = select(cls).order_by(
                cls.embedding.cosine_distance(embedding)
            ).limit(1)
            
            result = session.execute(stmt).scalar()
            
            if result and result.embedding.cosine_distance(embedding) < threshold:
                return result
            
            return None

    def __repr__(self):
        return f"<Course {self.course_code}>"