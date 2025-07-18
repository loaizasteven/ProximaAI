import React from 'react';
import './LandingPage.css'
import { useNavigate } from "react-router-dom";
import BlurText from './BlurText';

import logo from './assets/react.svg';

function TrackCard( {title, description, colorClass, icon, onLearnMore}) {
    return (
        <div className={`track-card ${colorClass}`}>
            <div className="track-content">
                <h2>{title}</h2>
                <p>{description}</p>                
            </div>
            <div className="track-icon-and-button">
                <div className="track-icon ">
                    <img src={icon} alt="logo" />
                </div>
                <button className={`learn-more ${colorClass}`} onClick={onLearnMore}>Learn more</button>
            </div>
        </div>
    )
}

function LandingPageMain({ handleResumeBuilderClick, handleApplicationAssistantClick }){
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

function ProductCard(){
    const navigate = useNavigate();
    const handleResumeBuilderClick = () => {
        alert('Veloa Resume Builder Coming Soon!');
    };
    const handleApplicationAssistantClick = () => {
        navigate("/products/app-assistant")
    };
    return (
            <>
                <h1><BlurText
                    text="Welcome to Proxima"
                    shinyTexts={["Designer","Builder", "AI"]}
                    stepDuration={0.35}
                    carouselInterval={1500}
                    delay={20}
                    animateBy="letters"
                    direction="top"
                    onAnimationComplete={() => {}}
                    className="text-2xl mb-8"
                />
                </h1>
                <div className="landing-page-headline">
                    ProximaAI is an AI-powered job search and resume assistant inspired by Anthropic's multi-agent research system. It leverages multi-agent technology and the Lang ecosystem to accelerate your career journey.
                </div>
                <LandingPageMain handleResumeBuilderClick={handleResumeBuilderClick} handleApplicationAssistantClick={handleApplicationAssistantClick} />
            </>
    );
}

const LandingPage = () => (
  <>
  <div className="product-card-container">
    <ProductCard/>
  </div>
  </>

);

export default LandingPage;