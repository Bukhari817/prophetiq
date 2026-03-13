import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    MODEL_NAME = "gemini-2.5-flash-preview-04-17"  # Best free tier model
    MAX_TOKENS = 8192
    TEMPERATURE = 0.7
    
    # Agent debate settings
    DEBATE_ROUNDS = 2  # How many rounds agents challenge each other
    
    def validate(self):
        if not self.GEMINI_API_KEY:
            return False
        return True
