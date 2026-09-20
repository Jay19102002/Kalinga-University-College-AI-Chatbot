import React from 'react';
import { HelpCircle, Sparkles } from 'lucide-react';

interface SuggestedQuestionsProps {
  onSelect: (question: string) => void;
}

const SUGGESTIONS = [
  "What is the admission procedure?",
  "What entrance exam is required?",
  "What is the fee for BBA?",
  "Does Kalinga offer scholarships?",
  "Does the university provide internships?",
  "Which companies recruit students?",
  "What is the highest package?",
  "What is KALSEE?"
];

export const SuggestedQuestions: React.FC<SuggestedQuestionsProps> = ({ onSelect }) => {
  return (
    <div className="py-1.5 px-1 sm:px-4 mb-1.5 shrink-0">
      <div className="flex items-center space-x-1.5 text-[10px] sm:text-xs text-slate-600 mb-1.5 font-extrabold uppercase tracking-wider">
        <Sparkles className="w-3.5 h-3.5 text-amber-500" />
        <span>Suggested Queries</span>
      </div>
      <div className="flex overflow-x-auto sm:flex-wrap gap-2 pb-1 sm:pb-0 scrollbar-none max-w-full touch-pan-x">
        {SUGGESTIONS.map((q, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(q)}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-full text-[11px] sm:text-xs font-bold text-slate-800 bg-gradient-to-br from-[#f0f5fc] to-[#d2d7de] shadow-neu-button active:shadow-neu-button-active hover:text-blue-700 hover:scale-105 border border-white/80 transition-all shrink-0 whitespace-nowrap"
          >
            <HelpCircle className="w-3 h-3 text-blue-600 shrink-0" />
            <span>{q}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
