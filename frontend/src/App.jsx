import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

const QUESTIONS = [
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
];

function App() {
  const [gameState, setGameState] = useState("home"); // home, quiz, result
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [currentInput, setCurrentInput] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const progress = ((currentStep + 1) / QUESTIONS.length) * 100;

  const handleNext = () => {
    if (!currentInput.trim()) return;
    
    const updatedAnswers = [...answers, currentInput];
    setAnswers(updatedAnswers);
    setCurrentInput("");
    
    if (currentStep < QUESTIONS.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setGameState("result");
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
      alert("⚠️ Connection Failed: Make sure your Python backend is running!\n" + err.message);
      setGameState("home");
    } finally {
      setLoading(false);
    }
  };

  // --- 1. HOME / LANDING VIEW ---
  if (gameState === "home") {
    return (
      <div className="app-canvas">
        <div className="home-container fade-in">
          <h1 className="brand-logo">EduCareer AI</h1>
          <p className="hero-tagline">Your career path, decoded by Intelligence.</p>
          
          <div className="explainer-section">
            <div className="explain-item">
              <span className="icon">🎯</span>
              <h3>What is EduCareer?</h3>
              <p>An AI-driven architect that analyzes behavioral patterns to find where you'll truly thrive.</p>
            </div>
            <div className="explain-item">
              <span className="icon">🧠</span>
              <h3>What it does</h3>
              <p>Maps your unique personality to high-growth career roadmaps using Gemini 1.5 Flash.</p>
            </div>
            <div className="explain-item">
              <span className="icon">🚀</span>
              <h3>How to use</h3>
              <p>Answer 10 behavioral scenarios. Be descriptive—the more context you give, the better the result.</p>
            </div>
          </div>

          <button className="primary-button large" onClick={() => setGameState("quiz")}>
            Begin Your Assessment
          </button>
        </div>
      </div>
    );
  }

  // --- 2. RESULT / CELEBRATION VIEW ---
  if (gameState === "result") {
    return (
      <div className="app-canvas result-canvas">
        <div className="result-container fade-in">
          <header className="congratulations-header">
            <div className="sparkle">✨</div>
            <h1 className="hero-announcement">Your Future Starts Now! 🚀</h1>
            <p className="hero-subtext">Gemini has architected a career path that perfectly matches your behavioral DNA.</p>
          </header>

          {loading ? (
            <div className="loader-box">
              <div className="pulse-ring"></div>
              <p>Analyzing your behavioral patterns...</p>
            </div>
          ) : (
            <div className="launchpad">
              <div className="markdown-body career-report">
                <ReactMarkdown>{result}</ReactMarkdown>
              </div>
              <div className="action-footer">
                <button className="secondary-button restart-btn" onClick={() => window.location.reload()}>
                  Retake Assessment
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // --- 3. QUIZ VIEW ---
  return (
    <div className="app-canvas">
      <div className="quiz-container fade-in">
        <h1 className="brand-logo small">EduCareer AI</h1>
        <p className="step-counter">Question {currentStep + 1} of 10</p>
        <h2 className="question-text">{QUESTIONS[currentStep]}</h2>
        
        <textarea 
          autoFocus
          value={currentInput}
          onChange={(e) => setCurrentInput(e.target.value)}
          placeholder="Describe your thoughts here..."
          className="clean-textarea"
        />
        
        <button 
          className="primary-button"
          onClick={handleNext} 
          disabled={!currentInput.trim()}
        >
          {currentStep === 9 ? "Generate My Roadmap" : "Next Question →"}
        </button>

        <div className="progress-track">
          <div className="progress-fill" style={{ width: `${progress}%` }}></div>
        </div>
      </div>
    </div>
  );
}

export default App;