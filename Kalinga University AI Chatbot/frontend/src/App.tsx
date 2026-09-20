import React, { useState, useEffect, useRef } from 'react';
import { Header } from './components/Header';
import { MessageBubble } from './components/MessageBubble';
import { InputBar } from './components/InputBar';
import { SuggestedQuestions } from './components/SuggestedQuestions';
import { KnowledgeModal } from './components/KnowledgeModal';
import { ConnectModal } from './components/ConnectModal';
import { Message } from './types/chat';
import { sendMessage, getHealthStatus, getDatabaseStats } from './services/api';
import { Bot, ShieldCheck } from 'lucide-react';

export const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome_1',
      sender: 'bot',
      text: 'Hello! I am the Kalinga University AI Student Assistant. How can I help you today with admissions, entrance exams (KALSEE/KAL-MAT), courses, fees, scholarships, internships, or placements?',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sources: [
        { title: 'Kalinga University Homepage', url: 'https://kalingauniversity.ac.in/' }
      ]
    }
  ]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [sessionId] = useState<string>(() => `sess_${Math.random().toString(36).substring(2, 9)}`);
  const [isKnowledgeOpen, setIsKnowledgeOpen] = useState<boolean>(false);
  const [isConnectOpen, setIsConnectOpen] = useState<boolean>(false);
  const [intentsCount, setIntentsCount] = useState<number>(33);
  const [totalRecords, setTotalRecords] = useState<number>(11070);

  // PWA Install State
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [canInstall, setCanInstall] = useState<boolean>(false);
  const [isInstalled, setIsInstalled] = useState<boolean>(() => {
    if (typeof window !== 'undefined') {
      return window.matchMedia('(display-mode: standalone)').matches ||
             (window.navigator as any).standalone === true;
    }
    return false;
  });

  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    checkHealth();

    // PWA beforeinstallprompt handler
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setCanInstall(true);
    };

    // PWA appinstalled handler
    const handleAppInstalled = () => {
      setIsInstalled(true);
      setCanInstall(false);
      setDeferredPrompt(null);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const checkHealth = async () => {
    try {
      const [res, stats] = await Promise.all([
        getHealthStatus(),
        getDatabaseStats().catch(() => null)
      ]);
      if (res.intents_count) {
        setIntentsCount(res.intents_count);
      }
      if (stats?.total_records) {
        setTotalRecords(stats.total_records);
      }
    } catch (err) {
      console.warn('Backend server not connected yet', err);
    }
  };

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleInstallApp = async () => {
    if (deferredPrompt) {
      try {
        deferredPrompt.prompt();
        const choice = await deferredPrompt.userChoice;
        if (choice.outcome === 'accepted') {
          setCanInstall(false);
        }
        setDeferredPrompt(null);
      } catch (err) {
        console.warn('Error launching install prompt:', err);
      }
    } else {
      // Fallback: Open ConnectModal which includes iOS & Android installation instructions
      setIsConnectOpen(true);
    }
  };

  const handleSend = async (userText: string) => {
    const userMsg: Message = {
      id: `user_${Date.now()}`,
      sender: 'user',
      text: userText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await sendMessage(userText, sessionId);
      const botMsg: Message = {
        id: `bot_${Date.now()}`,
        sender: 'bot',
        text: res.answer,
        intent: res.intent,
        confidence: res.confidence,
        entities: res.entities,
        sources: res.sources,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      const errorMsg: Message = {
        id: `err_${Date.now()}`,
        sender: 'bot',
        text: "Sorry, I'm having trouble connecting to the chatbot service. Please ensure the backend server is running and try again.",
        isError: true,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: `welcome_${Date.now()}`,
        sender: 'bot',
        text: 'Chat history cleared. How can I assist you with Kalinga University queries?',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        sources: [{ title: 'Kalinga University Homepage', url: 'https://kalingauniversity.ac.in/' }]
      }
    ]);
  };

  return (
    <div className="flex flex-col min-h-screen h-[100dvh] bg-[#e0e5ec] text-slate-800 font-sans selection:bg-blue-600 selection:text-white">
      
      {/* Top Header */}
      <Header
        onClearChat={handleClearChat}
        onOpenKnowledge={() => setIsKnowledgeOpen(true)}
        onOpenConnect={() => setIsConnectOpen(true)}
        onInstallApp={handleInstallApp}
        canInstall={canInstall}
        isInstalled={isInstalled}
        intentsCount={intentsCount}
        totalRecords={totalRecords}
      />

      {/* Main Chat Scroll Area */}
      <main className="flex-1 max-w-5xl w-full mx-auto p-2.5 sm:p-6 overflow-y-auto flex flex-col justify-between">
        
        <div className="flex-1">
          {/* Hero Welcome Banner */}
          <div className="bg-[#e0e5ec] border border-white/90 rounded-2xl sm:rounded-[28px] p-3 sm:p-5 mb-3 sm:mb-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2.5 sm:gap-4 shadow-neu-extruded">
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 sm:w-13 sm:h-13 rounded-xl sm:rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 shadow-neu-blue-glow border border-white/40 flex items-center justify-center shrink-0">
                <Bot className="w-5 h-5 sm:w-7 sm:h-7 text-white drop-shadow-sm" />
              </div>
              <div>
                <h2 className="text-xs sm:text-lg font-extrabold text-slate-900 flex items-center gap-1.5">
                  NLP Student Support Chatbot
                  <span className="text-[9px] sm:text-[10px] uppercase font-black bg-[#e0e5ec] text-emerald-700 px-2 py-0.5 rounded-full border border-white/60 shadow-neu-pressed">Active</span>
                </h2>
                <p className="text-[11px] sm:text-sm text-slate-600 mt-0.5 font-medium leading-tight">
                  Admissions, KALSEE, Fees, Scholarships, Internships & Placements.
                </p>
              </div>
            </div>

            <div className="hidden sm:flex items-center space-x-2 text-xs font-bold text-slate-700 bg-gradient-to-br from-[#f0f5fc] to-[#d2d7de] px-4 py-2 rounded-2xl border border-white/80 shadow-neu-button shrink-0">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>Grounded Knowledge Base</span>
            </div>
          </div>

          {/* Messages Feed */}
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}

          {/* Typing Indicator */}
          {isLoading && (
            <div className="flex items-center space-x-2 text-xs text-slate-700 py-3 px-4 bg-[#e0e5ec] rounded-2xl max-w-xs mb-4 border border-white/80 shadow-neu-extruded-sm font-bold">
              <div className="w-2.5 h-2.5 rounded-full bg-blue-600 animate-pulse"></div>
              <div className="w-2.5 h-2.5 rounded-full bg-blue-600 animate-pulse delay-150"></div>
              <div className="w-2.5 h-2.5 rounded-full bg-blue-600 animate-pulse delay-300"></div>
              <span className="ml-1 text-slate-800 font-extrabold">AI Assistant is typing...</span>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Suggested Query Pills */}
        <SuggestedQuestions onSelect={handleSend} />

      </main>

      {/* Sticky Bottom Input Bar */}
      <InputBar onSend={handleSend} isLoading={isLoading} />

      {/* Structured Knowledge Modal */}
      <KnowledgeModal
        isOpen={isKnowledgeOpen}
        onClose={() => setIsKnowledgeOpen(false)}
      />

      {/* Connect Mobile & Other Devices Modal */}
      <ConnectModal
        isOpen={isConnectOpen}
        onClose={() => setIsConnectOpen(false)}
      />

    </div>
  );
};

export default App;
