import React, { useState, useEffect } from 'react';
import './App.css';
import EmailProcessor from './EmailProcessor';

function App({ x, y, z }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [result, setResult] = useState([]);

  useEffect(() => {
    const updatedCarouselContent = result.map(item => item.toString());
    setCarouselContent(updatedCarouselContent);
  }, [result]);

  const [carouselContent, setCarouselContent] = useState([]);

  const handlePrevClick = () => {
    setCurrentIndex(prevIndex => (prevIndex === 0 ? carouselContent.length - 1 : prevIndex - 1));
  };

  const handleNextClick = () => {
    setCurrentIndex(prevIndex => (prevIndex === carouselContent.length - 1 ? 0 : prevIndex + 1));
  };

  const toggleDrawer = () => {
    setIsDrawerOpen(!isDrawerOpen);
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
      <EmailProcessor />
      <div className="status-box">
        <div className="status-item accepted" style={{ color: 'green' }}>Relevant: {x}</div>
        <div className="status-item rejected" style={{ color: 'red' }}>Irrelevant: {y}</div>
        <div className="info-box"></div>
        <div className="fun-fact">
        Fun Fact: A report from McKinsey & Company found that people spend approximately 28% of their workweek just on email.
</div>
      </div>
    </div>
  );
}

export default App;