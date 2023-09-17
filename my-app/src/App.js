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
      <div className="status-box">
        <div className="status-item accepted" style={{ color: 'green' }}>Offer: {x}</div>
        <div className="status-item rejected" style={{ color: 'red' }}>Rejected: {y}</div>
        <div className="status-item">Interview/OA: {z}</div>
      </div>
      <h1>Email Processing Result</h1>
      <EmailProcessor />
      <div className="textbox">
        <div className="button-container">
          <button className="pill" onClick={handlePrevClick}>&#8592; Previous</button>
          <button className="pill" onClick={handleNextClick}>Next &#8594;</button>
        </div>
        <div className="styled-textbox">
          <div className="entered-text">
            <div className="email-body">
              {carouselContent[currentIndex]}
            </div>
          </div>
        </div>
      </div>
      <div className={`drawer ${isDrawerOpen ? 'open' : ''}`}>
        <div className="drawer-toggle" onClick={toggleDrawer}>
          {isDrawerOpen ? <span>&#10005; Close</span> : <span>&#9776; Click to Learn!</span>}
        </div>
        <div className="drawer-content">
          <div className="centered-text">
            Fun fact! The average adult spends 30 minutes mindlessly scrolling through their inbox every day just to stay updated.
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;