import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from google import genai
import uvicorn

app = FastAPI()

# Enable CORS so your React app can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# --- CONFIGURATION ---
# 1) Store your Google Gemini API key securely in the environment.
#    Example: export GEMINI_API_KEY="your-secret-key"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is required")

# Initialize the Google GenAI Client
client = genai.Client(api_key=GEMINI_API_KEY)

@app.get("/")
def home():
    return {"status": "Career Chef API is Online"}

@app.post("/predict")
async def predict(data: dict):
    all_answers = data.get('answers', [])
    
    # Highly elaborative scenarios for deep AI context
    QUESTIONS = [
        "Problem Solving: Do you prefer technical 'fixing' (restoring objects/code) or social 'fixing' (resolving human conflicts)?",
        "Data vs. Creativity: Does a blank, structured spreadsheet make you feel powerful, or does a blank creative canvas excite you more?",
        "Leadership Style: In a crisis, do you naturally pitch the vision and lead, or do you prefer to document details and ensure accuracy?",
        "Deep Focus: Would you rather spend 8 hours mastering a technical manual or 8 hours using artistic tools to express an idea?",
        "Information Processing: Do you need to see the 'Big Picture' vision first, or do you prefer starting with step-by-step instructions?",
        "Risk Tolerance: Does a job with no clear rules and high ambiguity feel like a thrilling challenge or a stressful headache?",
        "Recognition: Would you rather be the anonymous inventor of a product or the famous face and spokesperson of a brand?",
        "Decision Making: Do you prioritize objective data/facts first, or do you prioritize how a decision impacts the team's feelings?",
        "Phase Preference: Do you find more joy in the Planning (strategy), the Doing (building), or the Selling (persuading) phase?",
        "Success Metric: Do you want to be judged on your high-quality individual output or your ability to lead a team to a goal?"
    ]

    # Combine questions and user answers into a psychometric profile
    user_profile = ""
    for q, a in zip(QUESTIONS, all_answers):
        user_profile += f"SCENARIO: {q}\nUSER CHOICE: {a}\n\n"

    # The 'Career Architect' Prompt
    prompt = f"""
    You are an expert Career Psychologist. Analyze this behavioral profile:
    
    {user_profile}

    TASK:
    1. Identify the user's 'Career Archetype' (e.g., The Digital Architect, The Empathetic Strategist).
    2. Recommend the TOP 3 Careers that perfectly balance their choices.
    3. For each career, provide:
       - **Why it matches**: Connect it to specific scenario answers.
       - **3-Step Roadmap**: Actionable steps to enter this field.

    Format the response in clean, professional Markdown with bold headings.
    """

    try:
        # Using Gemini 1.5 Flash - optimized for 2026 speed and accuracy
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        if not response.text:
            raise Exception("AI returned empty content")

        return {"analysis": response.text}

    except Exception as e:
        print(f"Gemini Error: {e}")
        # Standard rate-limit safety
        if "429" in str(e):
            raise HTTPException(status_code=429, detail="AI is over-capacity. Please wait 60 seconds.")
        raise HTTPException(status_code=500, detail="Career analysis failed. Verify your API key.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)