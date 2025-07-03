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
  const [currentPage, setCurrentPage] = useState('welcome')

  const items = [
    { icon: <VscHome size={18} color="white"/>, label: 'Home', onClick: () => setCurrentPage('main') },
    { icon: <VscAccount size={18} color="white"/>, label: 'Profile', onClick: () => setCurrentPage('profile') },
    { icon: <VscSettingsGear size={18} color="white"/>, label: 'Settings', onClick: () => setCurrentPage('settings') },
    { icon: <VscInfo size={18} color="white"/>, label: 'About', onClick:() =>  setCurrentPage('about') }
  ];

  return (
    <div className="app-container">
      {(currentPage === 'welcome' || currentPage === 'main') && (
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
          {/* Render the main page if the mainPage state is true */}
          {currentPage === 'main' && <LandingPage />}
          {/* Remove animation when mainPage is true */}
          {currentPage === 'welcome' && <SplashCursor SPLAT_RADIUS={0.1} />}
        </>
      )}
      {currentPage === 'about' && (<AboutPage />)}
      {currentPage === 'profile' && <div>Profile Page Coming Soon!</div>}
      {currentPage === 'settings' && <div>Settings Page Coming Soon!</div>}
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
