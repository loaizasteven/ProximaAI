import React from 'react';
import './LandingPage.css'

import logo from './assets/react.svg';

function TrackCard( {title, description, colorClass, icon}) {
    return (
        <div className={`track-card ${colorClass}`}>
            <div className="track-content">
                <h2>{title}</h2>
                <p>{description}</p>
                <button className={`learn-more ${colorClass}`}>Learn more</button>
            </div>
            <div className="track-icon ">
                <img src={icon} alt="logo" />
            </div>
        </div>
    )
}

function ProductCard(){
    return (
        <div className="product-card">
            <TrackCard
                title="Resume Builder with Veloa"
                description="Start with a blank canvas and let Veloa guide you through the process of creating a professional resume."
                colorClass="blue"
                icon={logo}
            />
            <TrackCard
                title="Veloa Application Assistant"
                description="Let Veloa help you find the perfect job. Veloa will search for jobs, 
                apply to them, and follow up with the hiring manager."
                colorClass="purple"
                icon={logo}
            />
        </div>
    )
}

const LandingPage = () => (
  <>
  ProximaAI is an AI-powered job search and resume assistant inspired by Anthropic's multi-agent research system. It leverages multi-agent technology and the Lang ecosystem to accelerate your career journey.
  <div className="product-card-container">
    <ProductCard />
  </div>
  </>

);

export default LandingPage;