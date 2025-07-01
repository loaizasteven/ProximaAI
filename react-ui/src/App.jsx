import { useState } from 'react'
import './App.css'
import BlurText from './BlurText'

function App() {
  const [enter, setEnter] = useState(false)
  const handleAnimationComplete = () => {
    setEnter(true)
  };

  return (
    <>
      <h1><BlurText
      text="Welcome to Proxima"
      shinyTexts={["Designer","Builder", "AI"]}
      carouselInterval={2000}
      delay={200}
      animateBy="letters"
      direction="top"
      onAnimationComplete={handleAnimationComplete}
      className="text-2xl mb-8"

    />
    </h1>
    {enter && (
      <div className="flex flex-col items-center justify-center h-screen">
        <button onClick={() => setEnter(false)}>Enter</button>
      </div>
    )}
    </>
  )
}

export default App
