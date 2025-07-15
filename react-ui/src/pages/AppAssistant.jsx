import React from 'react';
import '../styling/AppAssistant.css'; // We'll create this CSS file next
import reactLogo from '../assets/react.svg'; // Placeholder logo

// Background Images
const sphere = "https://plus.unsplash.com/premium_photo-1752113495331-165d1b5b749a?q=80&w=3132&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

// Handle file input change
const handleFileChange = (e) => {
  const file = e.target.files?.[0];
  if (!file) {
    setFileBase64(null);
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    setFileName(file.name)
    const dataUrl = reader.result;
    const base64 = dataUrl.split(',')[1]; // Extract base64 only
    setFileBase64(base64);
  };
  reader.readAsDataURL(file); 
  
}

// Header component
const Header = () => (
  <header className="atomize-header">
    <div className="logo-nav">
      <img src={reactLogo} alt="Logo" className="logo" />
      <span className="brand">ProximaAI</span>
    </div>
  </header>
);

// Hero section
const Hero = () => (
  <section className="atomize-hero">
    <h1>Resume Designer Agent</h1>
    <p className="subtitle">
      Our Multi Agent System helps users tailor their resume to the target job role with the application process.
    </p>
    <div className="hero-actions">
      <button className="primary-btn">Run Workflow</button>
    </div>
  </section>
);

// Card components
const ProfileCard = () => (
  <div className="card profile-card">
    <div className="avatar" />
    <div className="profile-info">
      <div className="name">Meagan Fisher</div>
      <div className="role">Engineering Manager</div>
    </div>
    <div className="profile-actions">
      <button className="follow-btn">Follow</button>
      <button className="message-btn">Message</button>
    </div>
  </div>
);

const DocumentInputCard = () => (
  <div className="card document-input">
    <div 
      className="image-placeholder" 
      style={{
        background: `url(${sphere}) center/cover`
      }}
    />
    <div className="document-input-info">
      <div className="description">
        Resume Upload: <br></br><br></br>
        Provide our agents with the latest version of your resume and we will take care of the rest.
      </div>
      <input className="file-input" type="file" accept="*/*" onChange={handleFileChange} />
    </div>
  </div>
);

const LoginCard = () => (
  <div className="card login-card">
    <div className="login-title">Login into your account</div>
    <div className="login-sub">Don't have an account yet? <a href="#">Create New</a></div>
    <input className="login-input" type="email" placeholder="johndoe1@gmail.com" />
    <input className="login-input" type="password" placeholder="Password" />
    <button className="login-btn">Login</button>
  </div>
);

// Main landing page layout
const LandingPageAtomize = () => (
  <div className="atomize-root">
    <Header />
    <Hero />
    <div className="cards-row">
      <ProfileCard />
      <DocumentInputCard />
      <LoginCard />
    </div>
  </div>
);

export default LandingPageAtomize; 