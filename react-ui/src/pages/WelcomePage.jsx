import React from 'react';
import { useNavigate } from "react-router";
import BlurText from '../BlurText'
import SplashCursor from '../SplashCursor'

// Function Definitions
function EnterStage(){
    let navigate = useNavigate();
    return <button className='welcome-button fadeIn' onClick={() => {navigate("/products")}}> Start your Journey </button>
}

function WelcomePage() {
    return (
        <div>
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
            <SplashCursor SPLAT_RADIUS={0.1}></SplashCursor>
            <EnterStage/>
        </div>
    );
};

export default WelcomePage;
