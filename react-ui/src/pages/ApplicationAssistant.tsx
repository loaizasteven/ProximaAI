import React, { useState, useEffect } from "react";

import { useStream } from "@langchain/langgraph-sdk/react";
import type { Message } from "@langchain/langgraph-sdk";

// Utility Function
function MyButton() {
  return (
    <button type="submit">submit</button>
  );
}


export default function ApplicationAssistant() {
  // Constants
  const [lastResumeHtml, setLastResumeHtml] = useState<string | null>(null);
  const thread = useStream<{ messages: Message[] }>({
    apiUrl: "http://localhost:2024/",
    assistantId: "main_agent",
    messagesKey: "messages", // for chat history
    onFinish: (state) => {
      const messages = state?.values?.messages;
      setLastResumeHtml(messages && messages.length > 0 ? messages[messages.length - 1].content as string : null)
    }
  });
  const [fileBase64, setFileBase64] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);

  useEffect(() => {
    if (!thread.isLoading && lastResumeHtml) {
      <div> 
        <h1> TEst</h1>
      </div>
    }
  }, [thread.isLoading]);

  // Handle file input change
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) {
      setFileBase64(null);
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      setFileName(file.name)
      const dataUrl = reader.result as string;
      const base64 = dataUrl.split(',')[1]; // Extract base64 only
      setFileBase64(base64);
    };
    reader.readAsDataURL(file); 
    
  }
  // Return default function
  return (
    <div>
      <h2> Application Assistant Beta</h2>
      <div>
        <h3>Tailored Resume Markdown</h3>
        {/* <div>{lastResumeHtml}</div> */}
      </div>
      {/* <div>
        {thread.messages.map((message, idx) => (
          <div key={message.id ?? idx}>
            {typeof message.content === "string"
              ? message.content
              : Array.isArray(message.content)
                ? message.content.map((c, i) =>
                    typeof c === "string"
                      ? c
                      : JSON.stringify(c)
                  ).join(" ")
                : JSON.stringify(message.content)}
            {message.id ?? idx}
          </div>
        ))}
      </div> */}
      {lastResumeHtml && (
        <div 
          style={{ textAlign: "left" }}
          dangerouslySetInnerHTML={{ __html: lastResumeHtml }} 
        />
      )}

      {/* {thread.messages.map((message, idx) => {
          console.log(
            Array.isArray(message.content) && message.content[0] && "name" in message.content[0]
              ? message.content[0].name
              : "error"
          );
          return (
            <div key={message.id ?? idx}>
              {Array.isArray(message.content)
                ? message.content.map((c, i) =>
                    typeof c === "string"
                      ? c
                      : JSON.stringify(c)
                  ).join(" ")
                : typeof message.content === "string"
                  ? message.content
                  : JSON.stringify(message.content)}
              {message.id ?? idx}
            </div>
          );
        })} */}
      <form
        onSubmit={(e) => {
          e.preventDefault();

          const form = e.target as HTMLFormElement;
          const message = new FormData(form).get("message") as string;

          //compose payload
          const payload: any = { messages: [{ type: "human", content: message }] }
          if (fileBase64) {
            payload.file_input = {
              "file_data": fileBase64,
              "file_name": fileName
          }}
          payload.user_id = 'sloa1991';
          console.log(payload)
          thread.submit(payload);

          // Reset after submission
          form.reset();
          setFileBase64(null);
          setFileName(null);
        }}
      >
        <div>
          <p>Add Message <input type="text-box" name="message" /> </p>
          <input type="file" accept="*/*" onChange={handleFileChange} />
        </div>
        
        {thread.isLoading ? (
          <button key="stop" type="button" onClick={() => thread.stop()}>
            Stop
          </button>
        ) : (
          <MyButton/>
        )}
      </form>
    </div>
  );
}
