import './App.css'
import BlurText from './BlurText'

function App() {
  const handleAnimationComplete = () => {
    console.log('Animation completed!');
  };

  return (
    <>
      <h1><BlurText
      text="Welcome to ProximaAI"
      delay={200}
      animateBy="letters"
      direction="top"
      onAnimationComplete={handleAnimationComplete}
      className="text-2xl mb-8"
    /></h1>    
    </>
  )
}

export default App
