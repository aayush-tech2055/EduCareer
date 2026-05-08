import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

const QUESTIONS = [
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
];

function App() {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [currentInput, setCurrentInput] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  // Progress percentage calculation
  const progress = ((currentStep + 1) / QUESTIONS.length) * 100;

  const handleNext = () => {
    if (!currentInput.trim()) return;
    
    const updatedAnswers = [...answers, currentInput];
    setAnswers(updatedAnswers);
    setCurrentInput("");
    
    if (currentStep < QUESTIONS.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      submitToAI(updatedAnswers);
    }
  };

  const submitToAI = async (finalAnswers) => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ answers: finalAnswers })
      });
      
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.detail || "Backend calculation failed.");
      }

      setResult(data.analysis);
    } catch (err) {
      alert("⚠️ Connection Failed: Make sure Python is running at http://127.0.0.1:8000\n\nOriginal Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // 1. RESULT SCREEN
  if (result) {
    return (
      <div className="main-container result-view">
        <header>
          <h1>Your Career Roadmap 🚀</h1>
          <p>Based on your unique personality profile</p>
        </header>
        <div className="result-card">
          <ReactMarkdown>{result}</ReactMarkdown>
        </div>
        <button className="restart-btn" onClick={() => window.location.reload()}>
          Retake Assessment
        </button>
      </div>
    );
  }

  // 2. QUIZ SCREEN
  return (
    <div className="main-container">
      <header className="header">
        <h1>EduCareer AI</h1>
        <div className="progress-container">
          <div className="progress-bar" style={{ width: `${progress}%` }}></div>
        </div>
        <p className="step-indicator">Question {currentStep + 1} of 10</p>
      </header>
      
      <div className="quiz-card">
        <h2 className="question-text">{QUESTIONS[currentStep]}</h2>
        <textarea 
          autoFocus
          value={currentInput}
          onChange={(e) => setCurrentInput(e.target.value)}
          placeholder="Describe your thoughts here..."
          className="answer-box"
        />
        
        <div className="button-wrapper">
          <button 
            className="next-btn"
            onClick={handleNext} 
            disabled={!currentInput.trim() || loading}
          >
            {loading ? "Processing..." : currentStep === 9 ? "Get My Prediction" : "Next Question →"}
          </button>
        </div>
      </div>

      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Gemini is decoding your future...</p>
        </div>
      )}
    </div>
  );
}

export default App;