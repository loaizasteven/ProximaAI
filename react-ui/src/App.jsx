import { useState } from 'react'
import { VscHome, VscInfo, VscAccount, VscSettingsGear } from "react-icons/vsc";
import './App.css'

import BlurText from './BlurText'
import SplashCursor from './SplashCursor'
import Dock from './Dock';

import LandingPage from './LandingPage';
import AboutPage from './AboutPage';

"use client";

import { useStream } from "@langchain/langgraph-sdk/react";

function App() {
  const [currentPage, setCurrentPage] = useState('welcome')
  const [resetDock, setResetDock] = useState(0)

  const items = [
    { icon: <VscHome size={18} color="white"/>, label: 'Home', onClick: () => { setCurrentPage('main'); setResetDock(r => r + 1); } },
    { icon: <VscAccount size={18} color="white"/>, label: 'Profile', onClick: () => setCurrentPage('profile') },
    { icon: <VscSettingsGear size={18} color="white"/>, label: 'Settings', onClick: () => setCurrentPage('settings') },
    { icon: <VscInfo size={18} color="white"/>, label: 'About', onClick:() =>  setCurrentPage('about') }
  ];

  const thread = useStream({
    apiUrl: "http://localhost:2024",
    assistantId: "main_agent",
    messagesKey: "messages",
  });

  // Function Definitions
  function EnterStage(){
    return <button className='welcome-button fadeIn' onClick={() => setCurrentPage('main')}> Start your Journey </button>
  }

  return (
    <div className="app-container">
      {(currentPage === 'welcome') && (
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
          <SplashCursor SPLAT_RADIUS={0.1}></SplashCursor>
        </>
      )}
      {currentPage === 'main' && <LandingPage reset={resetDock}/>}
      {currentPage === 'about' && (<AboutPage />)}
      {currentPage === 'profile' && 
        <div>
      <div>
        {thread.messages.map((message) => (
          <div key={message.id}>
            {typeof message.content === 'string' 
              ? message.content 
              : JSON.stringify(message.content)}
          </div>
        ))}
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault();

          const form = e.target;
          const message = new FormData(form).get("message");

          form.reset();
          thread.submit({ messages: [{ type: "human", content: message }], reasoning: "", current_step: "start" });
        }}
      >
        <input type="text" name="message" />

        {thread.isLoading ? (
          <button key="stop" type="button" onClick={() => thread.stop()}>
            Stop
          </button>
        ) : (
          <button type="submit">Send</button>
        )}
      </form>
    </div>
}
      {currentPage === 'settings' && <div>Settings Page Coming Soon!</div>}

      {currentPage === 'welcome'?<EnterStage/>:<Dock 
        items={items}
        panelHeight={68}
        baseItemSize={50}
        magnification={70}
      />}
    </div>
  )
}

export default App
