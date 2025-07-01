import { useState } from 'react'
import './App.css'
import BlurText from './BlurText'
import SplashCursor from './SplashCursor'

function App() {
  const [enter, setEnter] = useState(false)
  const [mainPage, setMainPage] = useState(false)
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

  return (
    
    <>
     <SplashCursor />

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

    {mainPage && (
      <>
        <h1>ProximaAI</h1>
        <p>ProximaAI is a platform for building AI-powered applications.</p>
      </>
    )}
    </>
  )
}

export default App
