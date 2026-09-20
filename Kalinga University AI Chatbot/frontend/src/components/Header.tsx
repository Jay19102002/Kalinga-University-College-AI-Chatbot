import React from 'react';
import { Bot, RefreshCw, Database, ShieldCheck, Download, QrCode, CheckCircle2 } from 'lucide-react';

interface HeaderProps {
  onClearChat: () => void;
  onOpenKnowledge: () => void;
  onOpenConnect: () => void;
  onInstallApp: () => void;
  canInstall: boolean;
  isInstalled: boolean;
  intentsCount: number;
  totalRecords?: number;
}

export const Header: React.FC<HeaderProps> = ({
  onClearChat,
  onOpenKnowledge,
  onOpenConnect,
  onInstallApp,
  canInstall,
  isInstalled,
  intentsCount,
  totalRecords = 11070
}) => {
  const formattedCount = totalRecords >= 1000 ? `${(totalRecords / 1000).toFixed(1)}k+` : totalRecords;

  return (
    <header className="sticky top-0 z-30 bg-[#e0e5ec] px-3 py-2 sm:px-6 sm:py-3 shadow-neu-extruded border-b border-white/60 shrink-0">
      <div className="max-w-5xl mx-auto flex items-center justify-between">
        
        {/* Left Branding */}
        <div className="flex items-center space-x-2 sm:space-x-3">
          <div className="w-8 h-8 sm:w-11 sm:h-11 rounded-xl sm:rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center shadow-neu-blue-glow border border-white/40 shrink-0">
            <Bot className="w-4 h-4 sm:w-6 sm:h-6 text-white drop-shadow-sm" />
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <h1 className="text-sm sm:text-lg font-extrabold text-slate-800 tracking-tight leading-tight">
                Kalinga University
              </h1>
              <span className="hidden md:inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#e0e5ec] text-blue-700 shadow-neu-pressed border border-white/50">
                <ShieldCheck className="w-3 h-3 mr-1 text-blue-600" /> Grounded AI
              </span>
            </div>
            <p className="text-[10px] sm:text-xs text-slate-500 font-semibold tracking-tight">
              AI Student Assistant <span className="hidden sm:inline">• NLP Minor Project</span>
            </p>
          </div>
        </div>

        {/* Right Action Buttons */}
        <div className="flex items-center space-x-1.5 sm:space-x-2">

          {/* Connect Other Devices / QR Button */}
          <button
            onClick={onOpenConnect}
            className="flex items-center space-x-1 sm:space-x-1.5 px-2.5 py-1.5 sm:px-3 sm:py-2 rounded-xl sm:rounded-2xl text-[11px] sm:text-xs font-bold text-slate-700 bg-gradient-to-br from-[#f0f5fc] to-[#d2d7de] shadow-neu-button active:shadow-neu-button-active hover:text-indigo-600 border border-white/70 transition-all"
            title="Connect Mobile & Other Devices (Scan QR)"
          >
            <QrCode className="w-3.5 h-3.5 text-indigo-600 shrink-0" />
            <span className="hidden sm:inline">Connect Devices</span>
            <span className="inline sm:hidden font-bold">QR</span>
          </button>

          {/* Install App Button / Badge */}
          {isInstalled ? (
            <div className="hidden sm:flex items-center space-x-1 px-2.5 py-1.5 rounded-xl text-[11px] font-bold text-emerald-700 bg-[#e0e5ec] shadow-neu-pressed border border-white/60">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              <span>App Installed</span>
            </div>
          ) : canInstall ? (
            <button
              onClick={onInstallApp}
              className="flex items-center space-x-1 sm:space-x-1.5 px-2.5 py-1.5 sm:px-3 sm:py-2 rounded-xl sm:rounded-2xl text-[11px] sm:text-xs font-black text-white bg-gradient-to-r from-blue-600 to-indigo-600 shadow-neu-blue-glow active:scale-95 border border-white/30 transition-all animate-pulse"
              title="Install Kalinga Chatbot to your Device"
            >
              <Download className="w-3.5 h-3.5 text-white shrink-0" />
              <span>Install App</span>
            </button>
          ) : null}

          {/* Database / Knowledge Button */}
          <button
            onClick={onOpenKnowledge}
            className="flex items-center space-x-1 sm:space-x-1.5 px-2.5 py-1.5 sm:px-3 sm:py-2 rounded-xl sm:rounded-2xl text-[11px] sm:text-xs font-bold text-slate-700 bg-gradient-to-br from-[#f0f5fc] to-[#d2d7de] shadow-neu-button active:shadow-neu-button-active hover:text-blue-700 border border-white/70 transition-all"
            title="Explore Knowledge Base & Database"
          >
            <Database className="w-3.5 h-3.5 text-blue-600 shrink-0" />
            <span className="hidden md:inline">Database ({formattedCount})</span>
            <span className="inline md:hidden font-bold">DB</span>
          </button>

          {/* Clear History Button */}
          <button
            onClick={onClearChat}
            className="flex items-center space-x-1 sm:space-x-1.5 px-2 py-1.5 sm:px-2.5 sm:py-2 rounded-xl sm:rounded-2xl text-[11px] sm:text-xs font-bold text-slate-600 bg-gradient-to-br from-[#f0f5fc] to-[#d2d7de] shadow-neu-button active:shadow-neu-button-active hover:text-rose-600 border border-white/70 transition-all"
            title="Clear Chat History"
          >
            <RefreshCw className="w-3.5 h-3.5 text-slate-500 shrink-0" />
            <span className="hidden sm:inline">Clear</span>
          </button>
        </div>

      </div>
    </header>
  );
};
