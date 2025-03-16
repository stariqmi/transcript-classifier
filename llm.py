import os   
import dotenv
import google.generativeai as genai

dotenv.load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')
