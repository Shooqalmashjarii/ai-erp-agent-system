from typing import Union
import os
import dotenv
from enum import Enum
from langchain_google_genai import ChatGoogleGenerativeAI
import sys
from langchain.schema import HumanMessage


# Get the path to the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up two directories to reach the project root
project_root = os.path.dirname(os.path.dirname(current_dir))
# Add the project root to the Python path
sys.path.insert(0, project_root)

class Stage(Enum):
    LOCAL = "local"
    CLOUD = "cloud"

##
MODEL_STAGE_MAP = {
    "gemini-2.5-flash-lite": Stage.CLOUD,
    "gemini-2.5-pro": Stage.CLOUD,
    "gemini-2.5-flash": Stage.CLOUD,
    "gemini-pro": Stage.CLOUD,
    "gemini-1.5-pro": Stage.CLOUD,
}


def initialize_llm(model_name: str) -> ChatGoogleGenerativeAI:
    stage = MODEL_STAGE_MAP.get(model_name)
    if stage is None:
        raise ValueError(f"Unknown model '{model_name}'. Available models: {list(MODEL_STAGE_MAP.keys())}")

    print(f"Building {stage.value} LLM for model: {model_name}")

    if stage == Stage.CLOUD:
        if model_name.startswith("gemini-"):
            dotenv.load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY is required. Please set it in your .env file")
            llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, temperature=0.2)
        else:
            raise ValueError(f"Cloud model '{model_name}' not supported. Only Gemini models are available.")
    else:
        raise ValueError(f"Local models are not supported. Only Gemini cloud models are available.")

    print(f"Successfully built {stage.value} LLM: {model_name}")
    return llm


_llm_instance = None

def build_llm(model_name: str = "gemini-2.5-flash"):
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = initialize_llm(model_name)
    return _llm_instance