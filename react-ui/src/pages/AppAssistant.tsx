import React, { useState } from 'react';
import '../styling/AppAssistant.css';

import { useStream } from "@langchain/langgraph-sdk/react";
import type { Message } from "@langchain/langgraph-sdk";

const galaxy = "https://images.unsplash.com/photo-1750292836196-3aafd7645c08?q=80&w=1728&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";
const sphere = "https://plus.unsplash.com/premium_photo-1752113495331-165d1b5b749a?q=80&w=3132&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";
const spiral = "https://images.unsplash.com/photo-1750969393822-36e48a31895f?q=80&w=1180&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

// Header component
const Header = () => (
  <header className="atomize-header">
    <div className="logo-nav">
      {/* <img src={reactLogo} alt="Logo" className="logo" /> */}
      <span className="brand">ProximaAI</span>
    </div>
  </header>
);

// Hero section
const Hero = ({ onRun }) => (
  <section className="atomize-hero">
    <h1>Resume Designer Agent</h1>
    <p className="subtitle">
      Our Multi Agent System helps users tailor their resume to the target job role with the application process.
    </p>
    <div className="hero-actions">
      <button className="primary-btn" onClick={onRun}>Run Workflow</button>
    </div>
  </section>
);

type MyFormProps ={
  userquery: string;
  setUserQuery: (val: string) => void;
  placeholder?: string | null; //optional property
}
function MyForm({ userquery, setUserQuery, placeholder}: MyFormProps) {
  const handleNameChange = (event) => {
    setUserQuery(event.target.value);
  };

  return (
    <textarea
      className='inputbox'
      value={userquery}
      onChange={handleNameChange}
      placeholder={placeholder ?? "Add context here"}
    />
  );
}

const UserInputCard = ({ userquery, setUserQuery }) => (
  <div className="card document-input">
    <div 
      className="image-placeholder" 
      style={{
        background: `url(${galaxy}) center/cover`
      }}
    />
    <div className="document-input-info">
      <div className="description">
        User Prompt: <br /><br />
        Include any additional context you'd like our agent to understand as we work to tailor your resume.
      </div>
      <MyForm userquery={userquery} setUserQuery={setUserQuery} />
    </div>
  </div>
);

const DocumentInputCard = ({ handleFileChange }) => (
  <div className="card document-input">
    <div 
      className="image-placeholder" 
      style={{
        background: `url(${sphere}) center/cover`
      }}
    />
    <div className="document-input-info">
      <div className="description">
        Resume Upload: <br /><br />
        Provide our agents with the latest version of your resume and we will take care of the rest.
      </div>
      <input className="file-input" type="file" accept="*/*" onChange={handleFileChange} />
    </div>
  </div>
);

const JobDescriptionCard = ({ jobdetails, setJobDetails }) => (
  <div className="card document-input">
    <div 
      className="image-placeholder" 
      style={{
        background: `url(${spiral}) center/cover`
      }}
    />
    <div className="document-input-info">
      <div className="description">
        Target Job Description: <br /><br />
        Paste the job description or requirements here.
      </div>
      <MyForm userquery={jobdetails} setUserQuery={setJobDetails} placeholder="Add job details here"/>
    </div>
  </div>
);

const LandingPageAtomize = () => {
  const [userquery, setUserQuery] = useState('');
  const [fileName, setFileName] = useState('');
  const [fileBase64, setFileBase64] = useState<string | null>(null);
  const [jobdetails, setJobDetails] = useState('');
  const [lastResumeHtml, setLastResumeHtml] = useState('');

  // LangGraph React.js flow
  const thread = useStream<{ messages: Message[] }>({
    apiUrl: "http://localhost:2024/",
    assistantId: "main_agent",
    messagesKey: "messages", // for chat history
    onFinish: (state) => {
      const messages = state?.values?.messages;
      setLastResumeHtml(messages[messages.length - 1].content as string)
    }
  });
  const payload: any = { messages: [{ type: "human", content: "" }] }

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) {
      setFileBase64(null);
      setFileName('');
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      setFileName(file.name);
      const dataUrl = reader.result as string;
      const base64 = dataUrl?.split(',')[1];
      setFileBase64(base64);
    };
    reader.readAsDataURL(file);
  };

  const handleRun = () => {
    // Use userquery, fileName, fileBase64 as needed
    // Construct the thread payload
    const humanMessage = `
    ${userquery}

    --------------
    # Target Company Job Description
    ${jobdetails}
    `;
    payload.messages[0].content = userquery;
    payload.file_input = {
      "file_data": fileBase64,
      "file_name": fileName
    };
    thread.submit(payload);
  };

  return (
    <div className="atomize-root">
      <Header />
      {lastResumeHtml && (
        <div
          style={{
            position: 'fixed',
            bottom: '16px',
            right: '16px',
            backgroundColor: 'lightgrey',
            boxShadow: '0 2px 8px rgba(0,0,0,0.10)',
            borderRadius: '6px',
            padding: '4px 8px',
            zIndex: 1000,
            minWidth: '80px',
            maxWidth: 'calc(100vw - 32px)',
            textAlign: 'left',
            fontSize: '0.8rem',
            boxSizing: 'border-box',
            overflow: 'hidden',
            wordBreak: 'break-all',
          }}
        >
          {fileName && <div style={{ fontWeight: 100, marginBottom: 2, fontSize: '0.85em' }}>File: <span style={{ fontWeight: 100 }}>{fileName}</span></div>}
          <a
            href={`data:text/html;charset=utf-8,${encodeURIComponent(lastResumeHtml)}`}
            download={fileName ? fileName.replace(/\.[^/.]+$/, '.html') : 'resume.html'}
            className="primary-btn"
            style={{ display: 'inline-block', margin: '8px', width: 'auto', backgroundColor: 'green'}}
          >
            Download HTML
          </a>
        </div>
      )}
      <Hero onRun={handleRun} />
      <div className="cards-row">
        <UserInputCard userquery={userquery} setUserQuery={setUserQuery} />
        <DocumentInputCard handleFileChange={handleFileChange} />
        <JobDescriptionCard jobdetails={jobdetails} setJobDetails={setJobDetails} />
      </div>
    </div>
  );
};

export default LandingPageAtomize; 