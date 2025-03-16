from sqlalchemy import Column, String, Text
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