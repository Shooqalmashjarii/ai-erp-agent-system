import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# Test it
if __name__ == "__main__":
    print("🧪 Testing Gemini connection...")
    try:
        response = llm.invoke("Explain what a purchase order is in one sentence.")
        print("🤖:", response.content)
    except Exception as e:
        print("❌ Error:", str(e))