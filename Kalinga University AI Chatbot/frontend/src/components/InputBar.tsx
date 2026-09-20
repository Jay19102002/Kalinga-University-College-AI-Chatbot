import React, { useState, KeyboardEvent } from 'react';
import { Send, Loader2 } from 'lucide-react';

interface InputBarProps {
  onSend: (text: string) => void;
  isLoading: boolean;
}

export const InputBar: React.FC<InputBarProps> = ({ onSend, isLoading }) => {
  const [text, setText] = useState('');

  const handleSend = () => {
    if (!text.trim() || isLoading) return;
    onSend(text.trim());
    setText('');
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="sticky bottom-0 bg-[#e0e5ec] border-t border-white/60 p-2 sm:p-4 shadow-neu-extruded z-20 shrink-0">
      <div className="max-w-5xl mx-auto flex items-center space-x-2 sm:space-x-3">
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about admissions, courses, fees, scholarships..."
          disabled={isLoading}
          className="flex-1 bg-[#e0e5ec] text-slate-900 placeholder-slate-400 font-semibold text-xs sm:text-sm rounded-xl sm:rounded-2xl px-3.5 py-2.5 sm:px-5 sm:py-3.5 shadow-neu-pressed focus:shadow-neu-pressed-deep focus:outline-none focus:ring-2 focus:ring-blue-500/50 border border-white/50 transition-all disabled:opacity-50 min-h-[42px] sm:min-h-[48px]"
        />
        <button
          onClick={handleSend}
          disabled={!text.trim() || isLoading}
          className="bg-gradient-to-br from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 text-white font-bold p-2.5 sm:p-3.5 rounded-xl sm:rounded-2xl shadow-neu-blue-glow active:shadow-neu-button-active border border-white/40 disabled:opacity-40 disabled:shadow-none transition-all flex items-center justify-center shrink-0 min-w-[42px] sm:min-w-[52px] min-h-[42px] sm:min-h-[48px] transform active:scale-95"
        >
          {isLoading ? (
            <Loader2 className="w-4 h-4 sm:w-5 sm:h-5 animate-spin" />
          ) : (
            <Send className="w-4 h-4 sm:w-5 sm:h-5 drop-shadow-sm" />
          )}
        </button>
      </div>
    </div>
  );
};
