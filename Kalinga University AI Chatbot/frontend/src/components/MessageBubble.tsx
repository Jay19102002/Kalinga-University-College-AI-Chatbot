import React from 'react';
import { Bot, User, AlertCircle, Sparkles } from 'lucide-react';
import { Message } from '../types/chat';
import { SourceCard } from './SourceCard';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';

  return (
    <div className={`flex w-full mb-3 sm:mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex items-start max-w-[92%] sm:max-w-[80%] space-x-2 sm:space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : 'flex-row'}`}>
        
        {/* Avatar Icon */}
        <div className={`w-7 h-7 sm:w-10 sm:h-10 rounded-xl sm:rounded-2xl flex items-center justify-center shrink-0 mt-0.5 ${
          isUser 
            ? 'bg-gradient-to-br from-blue-600 to-indigo-700 text-white shadow-neu-blue-glow border border-white/40' 
            : message.isError
            ? 'bg-rose-100 text-rose-600 shadow-neu-extruded-sm border border-rose-200'
            : 'bg-[#e0e5ec] text-blue-600 shadow-neu-extruded-sm border border-white/90'
        }`}>
          {isUser ? <User className="w-3.5 h-3.5 sm:w-5 sm:h-5" /> : message.isError ? <AlertCircle className="w-4 h-4 sm:w-5 sm:h-5" /> : <Bot className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600" />}
        </div>

        {/* Bubble Content Box */}
        <div className={`rounded-2xl sm:rounded-3xl px-3.5 py-2.5 sm:px-5 sm:py-4 text-xs sm:text-sm leading-relaxed whitespace-pre-wrap ${
          isUser
            ? 'bg-gradient-to-br from-blue-600 to-indigo-700 text-white shadow-neu-blue-glow rounded-tr-none font-medium border border-blue-400/30'
            : message.isError
            ? 'bg-gradient-to-br from-rose-50 to-rose-100 text-rose-900 border border-rose-200/80 shadow-neu-extruded rounded-tl-none font-medium'
            : 'bg-gradient-to-br from-[#f0f5fc] to-[#d8e2ee] text-slate-800 border border-white/90 shadow-neu-extruded rounded-tl-none font-normal'
        }`}>
          {/* Metadata badges for Bot responses */}
          {!isUser && message.intent && (
            <div className="flex items-center space-x-1.5 mb-1.5 pb-1 border-b border-slate-300/70 text-[10px] sm:text-[11px] text-slate-600">
              <span className="flex items-center text-blue-800 font-extrabold uppercase tracking-wide">
                <Sparkles className="w-3 h-3 sm:w-3.5 sm:h-3.5 mr-1 text-blue-600" />
                Intent: {message.intent}
              </span>
              {message.confidence !== undefined && (
                <span className="bg-[#e0e5ec] text-blue-800 px-2 py-0.5 rounded-full text-[9px] sm:text-[10px] font-bold border border-white/60 shadow-neu-badge">
                  Conf: {(message.confidence * 100).toFixed(0)}%
                </span>
              )}
            </div>
          )}

          {/* Main Message Content */}
          <div className={isUser ? "text-white font-semibold" : "text-slate-800 font-medium"}>
            {message.text}
          </div>

          {/* Sources */}
          {!isUser && message.sources && message.sources.length > 0 && (
            <SourceCard sources={message.sources} />
          )}

          {/* Timestamp */}
          <div className={`text-[9px] sm:text-[10px] mt-1.5 text-right font-bold ${isUser ? 'text-blue-100' : 'text-slate-400'}`}>
            {message.timestamp}
          </div>
        </div>

      </div>
    </div>
  );
};
