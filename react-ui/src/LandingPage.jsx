import React from 'react';
import './LandingPage.css'


function TrackCard( {title, description, colorClass, icon}) {
    return (
        <div className={`track-card ${colorClass}`}>
            <div className="track-content">
                <h2>{title}</h2>
                <p>{description}</p>
                <button className={`learn-more ${colorClass}`}>Learn more</button>
            </div>
            <div className="track-icon ">
                {icon}
            </div>
        </div>
    )
}

function ProductCard(){
    return (
        <div className="product-card">
            <TrackCard
                title="Product"
                description="Product"
                colorClass="blue"
                icon="a"
            />
            <TrackCard
                title="Product2"
                description="Product2"
                colorClass="red"
                icon="hg"
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