import sys
from catalogue import find_similar_courses

def main():
    # Read the description from stdin
    description = "Machine learning and artificial intelligence concepts"
    
    # Find similar courses
    similar_courses = find_similar_courses(description)
    
    # Print results
    print("\nSimilar courses:")
    for course_code, desc, similarity in similar_courses:
        print(f"\nCourse: {course_code}")
        print(f"Similarity: {similarity:.4f}")
        print(f"Description: {desc}")

if __name__ == "__main__":
    main()
