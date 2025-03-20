from extractor import extract_transcript_info
from classifier import classify_transcript
import argparse

def main():
    parser = argparse.ArgumentParser(description='Classify a transcript file.')
    parser.add_argument('transcript_path', help='Path to the transcript PDF file')
    args = parser.parse_args()
    
    extracted_data = extract_transcript_info(args.transcript_path)
    classification = classify_transcript(args.transcript_path, extracted_data)
    print(classification)

if __name__ == "__main__":
    main()
