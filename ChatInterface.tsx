"""
React Component: Chat Interface
Main UI for interacting with JARVIS
Handles text, voice, and real-time communication
"""

import React, { useState, useRef, useEffect } from 'react';
import { useWebSocket } from '../services/websocket';
import { MessageType, Message } from '../types';
import './ChatInterface.css';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  thinking?: string;
  action?: string;
  emotion?: string;
}

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [status, setStatus] = useState<'connecting' | 'connected' | 'disconnected'>('disconnected');
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<any>(null);
  const { send, subscribe, connect } = useWebSocket();
  
  // Initialize WebSocket connection
  useEffect(() => {
    connect('ws://localhost:8000/ws/chat').then(() => {
      setStatus('connected');
    });
    
    // Subscribe to messages
    subscribe((message) => {
      handleMessage(message);
    });
  }, []);
  
  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleMessage = (message: any) => {
    const newMessage: ChatMessage = {
      id: `${Date.now()}`,
      role: 'assistant',
      content: message.text,
      timestamp: new Date(),
      thinking: message.thinking_process,
      action: message.action,
      emotion: message.emotion
    };
    
    setMessages((prev) => [...prev, newMessage]);
    setIsLoading(false);
  };
  
  const sendMessage = async (content: string) => {
    if (!content.trim()) return;
    
    const userMessage: ChatMessage = {
      id: `${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date()
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    
    send({
      type: 'text',
      content
    });
  };
  
  const handleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Speech Recognition not supported in this browser');
      return;
    }
    
    const SpeechRecognition = window.webkitSpeechRecognition;
    recognitionRef.current = new SpeechRecognition();
    
    recognitionRef.current.onstart = () => {
      setIsListening(true);
    };
    
    recognitionRef.current.onresult = (event: any) => {
      const transcript = Array.from(event.results)
        .map((result: any) => result[0].transcript)
        .join('');
      
      setInputValue(transcript);
    };
    
    recognitionRef.current.onend = () => {
      setIsListening(false);
    };
    
    recognitionRef.current.start();
  };
  
  const stopVoiceInput = () => {
    recognitionRef.current?.stop();
    setIsListening(false);
  };
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(inputValue);
    }
  };
  
  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h1>🤖 JARVIS</h1>
        <div className="status-indicator" data-status={status}>
          {status === 'connected' ? '🟢 Online' : '🔴 Offline'}
        </div>
      </div>
      
      <div className="messages-container">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h2>Welcome to JARVIS</h2>
            <p>Your advanced AI assistant</p>
            <p>Ask me anything or give me commands...</p>
          </div>
        )}
        
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <div className="message-header">
              <span className="role">{message.role === 'user' ? '👤 You' : '🤖 JARVIS'}</span>
              <span className="timestamp">
                {message.timestamp.toLocaleTimeString()}
              </span>
            </div>
            
            <div className="message-content">{message.content}</div>
            
            {message.thinking && (
              <details className="thinking-process">
                <summary>💭 Show thinking process</summary>
                <div className="thinking-content">{message.thinking}</div>
              </details>
            )}
            
            {message.action && (
              <div className="action-badge">⚙️ Action: {message.action}</div>
            )}
            
            {message.emotion && (
              <div className="emotion-badge">😊 Emotion: {message.emotion}</div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="message assistant-message loading">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <div className="input-area">
        <div className="input-controls">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type message or press voice button..."
            className="input-field"
            disabled={!status || isLoading}
          />
          
          <button
            onClick={() => (isListening ? stopVoiceInput() : handleVoiceInput())}
            className={`voice-button ${isListening ? 'active' : ''}`}
            title="Voice input"
          >
            {isListening ? '⏹️ Stop' : '🎤 Voice'}
          </button>
          
          <button
            onClick={() => sendMessage(inputValue)}
            className="send-button"
            disabled={!inputValue.trim() || isLoading || !status}
          >
            📤 Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
