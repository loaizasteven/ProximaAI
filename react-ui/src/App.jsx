import { useState } from 'react'
import { VscHome, VscInfo, VscAccount, VscSettingsGear } from "react-icons/vsc";
import './App.css'

import BlurText from './BlurText'
import SplashCursor from './SplashCursor'
import Dock from './Dock';

import LandingPage from './LandingPage';
import AboutPage from './AboutPage';

function App() {
  const [enter, setEnter] = useState(false)
  const [mainPage, setMainPage] = useState(false)
  const [aboutPage, setAboutPage] = useState(false)

  const AssignAboutPage = () => {
    setAboutPage(true)
  }
  const handleAnimationComplete = () => {
    if (!mainPage) {
      setEnter(true)
    }
  };

  const handleMainPage = () => {
    setMainPage(true)
    setEnter(false)
    console.log("mainPage", mainPage)
    console.log("enter", enter)
  }

  const items = [
    { icon: <VscHome size={18} color="white"/>, label: 'Home', onClick: () => alert('Home!') },
    { icon: <VscAccount size={18} color="white"/>, label: 'Profile', onClick: () => alert('Profile!') },
    { icon: <VscSettingsGear size={18} color="white"/>, label: 'Settings', onClick: () => alert('Settings!') },
    { icon: <VscInfo size={18} color="white"/>, label: 'About', onClick: AssignAboutPage }
  ];

  return (
    <div className="app-container">
      {aboutPage ? (
        <AboutPage />
      ) : (
        <>
          <h1><BlurText
            text="Welcome to Proxima"
            shinyTexts={["Designer","Builder", "AI"]}
            stepDuration={0.35}
            carouselInterval={1500}
            delay={20}
            animateBy="letters"
            direction="top"
            onAnimationComplete={handleAnimationComplete}
            className="text-2xl mb-8"
          />
          </h1>
          {enter && (
            <div className="flex flex-col items-center justify-center h-screen">
              <button onClick={handleMainPage}>Enter</button>
            </div>
          )}
          {/* Render the main page if the mainPage state is true */}
          {mainPage && <LandingPage />}
          {/* Remove animation when mainPage is true */}
          {!mainPage && <SplashCursor SPLAT_RADIUS={0.1} />}
        </>
      )}
      <Dock 
        items={items}
        panelHeight={68}
        baseItemSize={50}
        magnification={70}
      />
    </div>
  )
}

export default App
