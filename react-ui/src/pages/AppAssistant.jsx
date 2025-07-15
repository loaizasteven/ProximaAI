import React from 'react';
import '../styling/AppAssistant.css'; // We'll create this CSS file next
import reactLogo from '../assets/react.svg'; // Placeholder logo

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

const ImageCard = () => (
  <div className="card image-card">
    <div className="image-placeholder" />
    <div className="image-info">
      <div className="name">Meagan Fisher</div>
      <div className="mini-profile">
        <div className="mini-avatar" />
        <span>John Doe</span>
        <span className="mini-role">UI/UX Designer</span>
      </div>
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
      <ImageCard />
      <LoginCard />
    </div>
  </div>
);

export default LandingPageAtomize; 