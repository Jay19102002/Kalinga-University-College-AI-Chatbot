import React from 'react';
import { ExternalLink, CheckCircle2 } from 'lucide-react';
import { SourceItem } from '../types/chat';

interface SourceCardProps {
  sources: SourceItem[];
}

export const SourceCard: React.FC<SourceCardProps> = ({ sources }) => {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3.5 pt-3 border-t border-slate-300/70">
      <div className="flex items-center space-x-1.5 text-[10px] font-extrabold text-slate-600 uppercase tracking-wider mb-2">
        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
        <span>Official Verification Source</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {sources.map((src, idx) => (
          <a
            key={idx}
            href={src.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-2xl text-xs font-extrabold text-blue-800 bg-gradient-to-br from-[#f0f5fc] to-[#d2d7de] shadow-neu-button active:shadow-neu-button-active hover:text-blue-950 border border-white/80 transition-all duration-150 group"
          >
            <span>{src.title}</span>
            <ExternalLink className="w-3.5 h-3.5 text-blue-600 group-hover:text-blue-900" />
          </a>
        ))}
      </div>
    </div>
  );
};
