import React, { useState } from 'react';
import './App.css';

function App() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const carouselContent = [
    `Acceptance for Company : Company Name`,
    `Rejection for Company : Company Name`,
    'Interview for Company : Company Name',
    // Add more contents as needed
  ];

  const handlePrevClick = () => {
    setCurrentIndex(prevIndex => (prevIndex === 0 ? carouselContent.length - 1 : prevIndex - 1));
  };

  const handleNextClick = () => {
    setCurrentIndex(prevIndex => (prevIndex === carouselContent.length - 1 ? 0 : prevIndex + 1));
  };

  return (
    <div className="app">
      <div className="title">InternTrack</div> {/* Added Company Name */}
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
    </div>
  );
}

export default App;
