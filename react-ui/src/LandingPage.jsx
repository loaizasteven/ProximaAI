import React from 'react';
    import './LandingPage.css'

import logo from './assets/react.svg';

function TrackCard( {title, description, colorClass, icon, onLearnMore}) {
    return (
        <div className={`track-card ${colorClass}`}>
            <div className="track-content">
                <h2>{title}</h2>
                <p>{description}</p>
                <button className={`learn-more ${colorClass}`} onClick={onLearnMore}>Learn more</button>
            </div>
            <div className="track-icon ">
                <img src={icon} alt="logo" />
            </div>
        </div>
    )
}

function ProductCard(){
    const handleResumeBuilderClick = () => {
        alert('Learn more about Resume Builder with Veloa');
    };
    const handleApplicationAssistantClick = () => {
        alert('Learn more about Veloa Application Assistant');
    };
    return (
        <div className="product-card">
            <TrackCard
                title="Resume Builder with Veloa"
                description="Start with a blank canvas and let Veloa guide you through the process of creating a professional resume."
                colorClass="blue"
                icon={logo}
                onLearnMore={handleResumeBuilderClick}
            />
            <TrackCard
                title="Veloa Application Assistant"
                description="Let Veloa help you find the perfect job. Veloa will search for jobs, 
                apply to them, and follow up with the hiring manager."
                colorClass="purple"
                icon={logo}
                onLearnMore={handleApplicationAssistantClick}
            />
        </div>
    )
}

const LandingPage = () => (
  <>
  <div className="landing-page-headline">
      ProximaAI is an AI-powered job search and resume assistant inspired by Anthropic's multi-agent research system. It leverages multi-agent technology and the Lang ecosystem to accelerate your career journey.
  </div>
  <div className="product-card-container">
    <ProductCard />
  </div>
  </>

);

export default LandingPage;