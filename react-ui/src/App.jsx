import { useState } from 'react';
import { useLocation, Navigate, BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import { VscHome, VscInfo, VscAccount, VscSettingsGear } from "react-icons/vsc";
import './App.css'

// UI Components
import Dock from './Dock';

// SubPages
import WelcomePage from './pages/WelcomePage';
import Authentication, { useAuth, LoginForm } from './auth/Authentication';
import LandingPage from './LandingPage';
import AboutPage from './AboutPage';

"use client";

import { useStream } from "@langchain/langgraph-sdk/react";

function RequireAuth({ children }) {
  const session = useAuth()
  const location = useLocation();
  if (!session) return <Navigate to="/login" replace state={{ from: location}}/>
  return children
}

function App() {
  const [currentPage, setCurrentPage] = useState('welcome')
  const [resetDock, setResetDock] = useState(0)
  const location = useLocation();
  const dockVisibleRoutes = ["/about", "/products"]; 

  const thread = useStream({
    apiUrl: "http://localhost:2024",
    assistantId: "main_agent",
    messagesKey: "messages",
  });
  const navigate = useNavigate();

  const items = [
    { icon: <VscHome size={18} color="white"/>, label: 'Home', onClick: () => { navigate('/products'); setResetDock(r => r + 1); } },
    { icon: <VscAccount size={18} color="white"/>, label: 'Profile', onClick: () => navigate('/about') },
    { icon: <VscSettingsGear size={18} color="white"/>, label: 'Settings', onClick: () => navigate('/products') },
    { icon: <VscInfo size={18} color="white"/>, label: 'About', onClick: () => navigate('/products') }
  ];
  
  return (
    <Authentication>
      <Routes>
          <Route path="/" element={<WelcomePage />} />
          <Route path="/about" element={<RequireAuth><AboutPage /></RequireAuth>} />
          <Route path="/products" element={<LandingPage />} />
          <Route path="/login" element={<LoginForm />} />
        </Routes>
        <div>
          {dockVisibleRoutes.includes(location.pathname) && (
          <Dock 
            items={items}
            panelHeight={68}
            baseItemSize={50}
            magnification={70}
          />
        )}
        </div>
    </Authentication>
  )
}

export default function AppWithRouter() {
  return (
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
}
