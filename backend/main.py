from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from huggingface_hub import InferenceClient
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Plan C: Use Hugging Face (Public API)
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3")

@app.get("/")
def home():
    return {"message": "Hugging Face Chef is ready!"}

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
    
    formatted_data = ""
    for i in range(min(len(QUESTIONS), len(all_answers))):
        formatted_data += f"Q: {QUESTIONS[i]} | A: {all_answers[i]}\n"
    
    prompt = f"<s>[INST] You are a Career Coach. Analyze these answers:\n{formatted_data}\nPredict TOP 3 careers with roadmaps. Use Markdown. [/INST]"

    try:
        response = client.text_generation(prompt, max_new_tokens=1000)
        return {"analysis": response}
    except Exception as exc:
        print(f"REAL ERROR: {exc}")
        raise HTTPException(status_code=500, detail="The AI is sleeping. Try again in 1 minute.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)