import React, { useState } from 'react';
import './App.css';
import EmailProcessor from './EmailProcessor';

function App() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [relevantCount, setRelevantCount] = useState(0);
  const [irrelevantCount, setIrrelevantCount] = useState(0);

  const updateCounts = (relevant, irrelevant) => {
    setRelevantCount(relevant);
    setIrrelevantCount(irrelevant);
  };

  return (
    <div className="app">
      <div className="title">InternTrack</div>
      <div className="sub-header-description">
        Less time sifting emails, more time on what matters
      </div>
      <div className="description">
        Automatically scan your last 10 emails and let our advanced AI determine their relevance to your internship or job search. 
      </div>
      <h1 className="sub-header">Email Processing Result:</h1>
      <EmailProcessor updateCounts={updateCounts} />
      <div className="status-box">
        <div className="status-item accepted" style={{ color: 'green' }}>Relevant: {relevantCount}</div>
        <div className="status-item rejected" style={{ color: 'red' }}>Irrelevant: {irrelevantCount}</div>
        <div className="info-box"></div>
        <div className="fun-fact">
          Fun Fact: A report from McKinsey & Company found that people spend approximately 28% of their workweek just on email.
        </div>
      </div>
    </div>
  );
}

export default App;