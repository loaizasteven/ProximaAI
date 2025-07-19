import { useState } from 'react';
import '../styling/AppAssistant.css';

import { useStream } from "@langchain/langgraph-sdk/react";
import type { Message } from "@langchain/langgraph-sdk";

import {CreditBalance} from '@/components/credits/credit-balance'
import {CreditUpdate} from '@/providers/Credits'
import { useAuth, useSupabase } from '@/auth/Authentication';

const galaxy = "https://images.unsplash.com/photo-1750292836196-3aafd7645c08?q=80&w=1728&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";
const sphere = "https://plus.unsplash.com/premium_photo-1752113495331-165d1b5b749a?q=80&w=3132&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";
const spiral = "https://images.unsplash.com/photo-1750969393822-36e48a31895f?q=80&w=1180&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

// Header component
const Header = () => {
  return (
    <header className="atomize-header">
      <div className="logo-nav">
        {/* <img src={reactLogo} alt="Logo" className="logo" /> */}
        <span className="brand">ProximaAI</span>
      </div>
      <span ><CreditBalance/ ></span>
    </header>
  );
};
// SubHeader section
const SubHeader = ({ onRun, thread, fileName, lastResumeHtml }) => (
  <section className="atomize-hero">
    <h1>Resume Designer Agent</h1>
    <p className="subtitle">
      Our Multi Agent System helps users tailor their resume to the target job role with the application process.
      {lastResumeHtml &&
        <span>
        Your resume is ready{" "}
        <a
          href={`data:text/html;charset=utf-8,${encodeURIComponent(lastResumeHtml)}`}
          download={fileName ? fileName.replace(/\.[^/.]+$/, '.html') : 'resume.html'}
        >
          click here
        </a>
        {" "}to download.
      </span>
      }
    </p>
    <div>
      <button className="primary-btn" onClick={onRun}>
        {thread.isLoading ? (
          <span className="pulse-text">Agent Thinking...</span>
        ) : (
          "Run Workflow"
        )}
      </button>
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
  const [fileInputKey, setFileInputKey] = useState(0);
  const supabase = useSupabase();
  const session = useAuth();

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

  const handleRun = async () => {
    // Use userquery, fileName, fileBase64 as needed
    // Construct the thread payload
    const humanMessage = `
    ${userquery}

    --------------
    # Target Company Job Description
    ${jobdetails}
    `;
    payload.messages[0].content = userquery;
    // placeholder user id
    payload.user_id = "sloa1991"
    payload.file_input = {
      "file_data": fileBase64,
      "file_name": fileName
    };
    thread.submit(payload);

    // Update Credit Usage
    await CreditUpdate({ authenticated: session? true: false, credit_usage: 1, supabase: supabase, session: session})
    // Reset state
    setUserQuery('');
    setJobDetails('');
    setFileName('');
    setFileBase64(null);
    setFileInputKey(prev => prev + 1); // Add this line
  };

  return (
    <div className="atomize-root">
      <Header />
      <SubHeader onRun={handleRun} thread={thread} fileName={fileName} lastResumeHtml={lastResumeHtml}/>
      <div className="cards-row">
        <UserInputCard userquery={userquery} setUserQuery={setUserQuery} />
        <DocumentInputCard key={fileInputKey} handleFileChange={handleFileChange} />
        <JobDescriptionCard jobdetails={jobdetails} setJobDetails={setJobDetails} />
      </div>
    </div>
  );
};

export default LandingPageAtomize; 
