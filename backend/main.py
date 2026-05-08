from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from google import genai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


client = genai.Client(api_key="AIzaSyA5FSSNDhTiW1-pY16kctAi0Cxtv12EWaE")

@app.get("/")
def home():
    return {"message": "The Career Chef is ready!"}

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
    
    prompt = f"""
    {QUESTIONS}
    Analyze these 10 psychological career preferences: {all_answers}.
    
    Based on these, predict the TOP 3 most suitable careers.
    For each career, provide:
    1. Career Name
    2. Why it fits (based on their specific answers)
    3. A 3-step mini roadmap to get started.
    
    Format the response clearly using Markdown (bold titles and bullet points).
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        return {"analysis": response.text}
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "AI backend unavailable. "
                "Please verify your Google GenAI quota/API key or try again later."
            ),
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,
    )