from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from groq import Groq
from dotenv import load_dotenv
import os


env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


# GROQ_API_KEY` from .env when running locally
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable is required")

client = Groq(api_key=GROQ_API_KEY)

@app.get("/")
def home():
    return {"message": "The Career Chef is ready (Powered by Groq)!"}

@app.post("/predict")
def predict(data: dict):
    QUESTIONS = [
        "Would you rather fix a broken physical object, or a broken relationship between two people?",
        "Does a blank spreadsheet make you feel organized and powerful, or bored and restricted?",
        "In a high-stakes meeting, are you the one pitching the vision, or the one taking notes?",
        "Would you prefer 8 hours with technical manuals or a canvas and paint?",
        "Do you want to see the 'Big Picture' first, or step-by-step instructions?",
        "Does 'ambiguity' at work give you a thrill or a headache?",
        "Would you rather be an anonymous inventor or the famous face of a brand?",
        "Do you check the data/facts first, or check how the team is feeling?",
        "If you won the lottery, would you still enjoy the planning, the doing, or the selling?",
        "Do you prefer to be judged on your individual work or your success as a leader?"
    ]

    all_answers = data.get('answers', []) 
    
    # Construct the prompt
    prompt = f"""
    Analyze these 10 psychological career preferences: {all_answers}.
    
    Based on these, predict the TOP 3 most suitable careers.
    For each career, provide:
    1. Career Name
    2. Why it fits (based on their specific answers)
    3. A 3-step mini roadmap to get started.
    
    Format the response clearly using Markdown (bold titles and bullet points).
    """

    try:
      
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert career counselor and psychologist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        return {"analysis": completion.choices[0].message.content}

    except Exception as exc:
        print(f"Error: {exc}")
        raise HTTPException(
            status_code=503,
            detail="The AI is sleeping. Try again in a minute."
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)