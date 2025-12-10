import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from '@docusaurus/router';
import styles from './ChatWidget.module.css';
import { getTranslations, isRTL, type ChatWidgetStrings } from './translations';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
}

interface ChatWidgetProps {
  apiUrl?: string;
  chapterSlug?: string;
}

/**
 * Extract locale from URL path (e.g., /fr/docs/intro -> 'fr')
 */
function getLocaleFromPath(pathname: string): string {
  const localeMatch = pathname.match(/^\/(fr|ar|ur)\//);
  return localeMatch ? localeMatch[1] : 'en';
}

export default function ChatWidget({ 
  apiUrl = 'http://localhost:8000',
  chapterSlug 
}: ChatWidgetProps): JSX.Element {
  const location = useLocation();
  const locale = getLocaleFromPath(location.pathname);
  const t: ChatWidgetStrings = getTranslations(locale);
  const rtl = isRTL(locale);
  
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Listen for text selection
  useEffect(() => {
    // Only run in browser environment
    if (typeof window === 'undefined' || typeof document === 'undefined') {
      return;
    }

    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();
      if (text && text.length > 10) {
        setSelectedText(text);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          session_id: sessionId,
          selected_text: selectedText,
          chapter_slug: chapterSlug,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      
      // Update session ID if this is the first message
      if (!sessionId && data.session_id) {
        setSessionId(data.session_id);
      }

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        sources: data.sources,
      };

      setMessages(prev => [...prev, assistantMessage]);
      setSelectedText(null); // Clear selected text after using it
      
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
    // Close on Escape key
    if (e.key === 'Escape' && isOpen) {
      setIsOpen(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSessionId(null);
    setSelectedText(null);
  };
  
  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  return (
    <>
      {/* Toggle Button */}
      <button
        className={styles.toggleButton}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? t.close : 'Open chat'}
        aria-expanded={isOpen}
        aria-controls="chat-window"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div 
          id="chat-window"
          className={styles.chatWindow}
          dir={rtl ? 'rtl' : 'ltr'}
          role="dialog"
          aria-label={t.title}
        >
          {/* Header */}
          <div className={styles.header}>
            <h3>{t.title}</h3>
            <div className={styles.headerActions}>
              <span className={styles.aiNote}>{t.aiResponseNote}</span>
              <button 
                onClick={clearChat} 
                className={styles.clearButton}
                title={t.clear}
                aria-label={t.clear}
              >
                🗑️
              </button>
            </div>
          </div>

          {/* Selected Text Banner */}
          {selectedText && (
            <div className={styles.selectedTextBanner}>
              <span className={styles.selectedTextLabel}>{t.selectedText}</span>
              <span className={styles.selectedTextContent}>
                "{selectedText.substring(0, 50)}..."
              </span>
              <button
                onClick={() => setSelectedText(null)}
                className={styles.clearSelectionButton}
                aria-label="Clear selection"
              >
                ✕
              </button>
            </div>
          )}

          {/* Messages */}
          <div 
            className={styles.messages}
            role="log"
            aria-live="polite"
            aria-label="Chat messages"
          >
            {messages.length === 0 && (
              <div className={styles.emptyState}>
                <p>{t.emptyStateGreeting}</p>
                <p>{t.emptyStateHint}</p>
                {selectedText && (
                  <p className={styles.hint}>
                    {t.selectedTextHint}
                  </p>
                )}
              </div>
            )}

            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`${styles.message} ${
                  msg.role === 'user' ? styles.userMessage : styles.assistantMessage
                }`}
                role="article"
                aria-label={msg.role === 'user' ? 'Your message' : 'AI response'}
              >
                <div className={styles.messageContent}>{msg.content}</div>
                
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sources}>
                    <span className={styles.sourcesLabel}>{t.sources}</span>
                    {msg.sources.map((source, i) => (
                      <span key={i} className={styles.source}>
                        {source.replace('module-', 'Module ').replace('/', ' › ')}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div 
                className={`${styles.message} ${styles.assistantMessage}`}
                role="status"
                aria-label={t.typing}
              >
                <div className={styles.loading}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className={styles.inputContainer}>
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={t.placeholder}
              className={styles.input}
              rows={2}
              disabled={isLoading}
              aria-label={t.placeholder}
              dir={rtl ? 'rtl' : 'ltr'}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              className={styles.sendButton}
              aria-label={t.send}
            >
              {isLoading ? '⏳' : '➤'}
            </button>
          </div>
        </div>
      )}
    </>
  );
}
