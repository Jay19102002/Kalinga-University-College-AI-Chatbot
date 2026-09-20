import React, { useState, useEffect } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { X, Smartphone, Copy, Check, Wifi, Globe, Share2, HelpCircle } from 'lucide-react';

interface ConnectModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ConnectModal: React.FC<ConnectModalProps> = ({ isOpen, onClose }) => {
  const [currentUrl, setCurrentUrl] = useState<string>('');
  const [copied, setCopied] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'mobile' | 'ios' | 'android'>('mobile');

  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Use current window location
      setCurrentUrl(window.location.origin);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(currentUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isLocalhost = currentUrl.includes('localhost') || currentUrl.includes('127.0.0.1');

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div 
        className="w-full max-w-lg bg-[#e0e5ec] rounded-3xl shadow-neu-extruded border border-white/80 p-5 sm:p-6 overflow-hidden flex flex-col max-h-[90vh]"
        onClick={(e) => e.stopPropagation()}
      >
        
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-300/60">
          <div className="flex items-center space-x-2.5">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center shadow-neu-blue-glow border border-white/40">
              <Smartphone className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-base sm:text-lg font-extrabold text-slate-800 tracking-tight">
                Connect Mobile & Other Devices
              </h3>
              <p className="text-[11px] sm:text-xs text-slate-500 font-semibold">
                Scan QR code to open & install on phones or tablets
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-[#e0e5ec] flex items-center justify-center text-slate-500 hover:text-slate-800 shadow-neu-button active:shadow-neu-button-active border border-white/60 transition-all"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto py-4 space-y-4 pr-1">
          
          {/* Wi-Fi Note Badge */}
          <div className="flex items-center space-x-2 p-2.5 rounded-2xl bg-blue-50/80 border border-blue-200/70 text-blue-900 text-xs font-semibold shadow-inner">
            <Wifi className="w-4 h-4 text-blue-600 shrink-0 animate-pulse" />
            <span>Ensure your phone is connected to the <strong>same Wi-Fi network</strong> as this computer.</span>
          </div>

          {/* QR Code Card */}
          <div className="flex flex-col items-center justify-center p-5 bg-[#e0e5ec] rounded-2xl shadow-neu-pressed border border-white/50">
            <div className="p-3 bg-white rounded-2xl shadow-md border border-slate-200/80">
              <QRCodeSVG
                value={currentUrl || 'http://localhost:5173'}
                size={175}
                level="M"
                includeMargin={true}
                imageSettings={{
                  src: "/favicon.svg",
                  x: undefined,
                  y: undefined,
                  height: 36,
                  width: 36,
                  excavate: true,
                }}
              />
            </div>
            <p className="mt-3 text-xs font-extrabold text-slate-700 tracking-wide text-center">
              Scan with your Phone Camera
            </p>
            <span className="text-[10px] text-slate-500 font-medium">
              No extra apps required • Opens instantly
            </span>
          </div>

          {/* URL & Copy Bar */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-700 flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Globe className="w-3.5 h-3.5 text-blue-600" /> Shareable Web Address
              </span>
              {isLocalhost && (
                <span className="text-[10px] font-normal text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200">
                  Tip: Use your LAN IP (e.g. 192.168.x.x) for phone access
                </span>
              )}
            </label>
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={currentUrl}
                onChange={(e) => setCurrentUrl(e.target.value)}
                placeholder="http://192.168.x.x:5173"
                className="flex-1 px-3.5 py-2 rounded-xl bg-[#e0e5ec] border border-white/70 shadow-neu-pressed text-xs font-mono font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              />
              <button
                onClick={handleCopy}
                className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-gradient-to-br from-[#f0f5fc] to-[#d2d7de] text-xs font-extrabold text-blue-700 shadow-neu-button active:shadow-neu-button-active border border-white/70 hover:text-blue-800 transition-all shrink-0"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-blue-600" />}
                <span>{copied ? 'Copied!' : 'Copy'}</span>
              </button>
            </div>
          </div>

          {/* Quick Install Guide Tabs */}
          <div className="bg-[#e0e5ec] rounded-2xl p-3.5 border border-white/70 shadow-neu-extruded-sm">
            <div className="flex items-center space-x-2 pb-2 mb-2 border-b border-slate-300/50">
              <HelpCircle className="w-3.5 h-3.5 text-blue-600" />
              <span className="text-xs font-extrabold text-slate-800">How to Install as App (1-Click)</span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="p-2.5 rounded-xl bg-white/40 border border-white/80">
                <p className="font-extrabold text-slate-800 flex items-center gap-1 mb-1">
                  <span>📱</span> Android Phone
                </p>
                <ol className="text-[11px] text-slate-600 space-y-1 list-decimal list-inside leading-tight font-medium">
                  <li>Scan QR in Chrome browser</li>
                  <li>Tap <strong>"Install App"</strong> prompt or Chrome menu (⋮)</li>
                  <li>Tap <strong>"Add to Home screen"</strong></li>
                </ol>
              </div>

              <div className="p-2.5 rounded-xl bg-white/40 border border-white/80">
                <p className="font-extrabold text-slate-800 flex items-center gap-1 mb-1">
                  <span>🍎</span> iPhone / iPad
                </p>
                <ol className="text-[11px] text-slate-600 space-y-1 list-decimal list-inside leading-tight font-medium">
                  <li>Scan QR & open in Safari</li>
                  <li>Tap Share button (<strong>⎋</strong>)</li>
                  <li>Scroll and tap <strong>"Add to Home Screen"</strong> (⊞)</li>
                </ol>
              </div>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="pt-3 border-t border-slate-300/60 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs font-bold text-slate-700 bg-gradient-to-br from-[#f0f5fc] to-[#d2d7de] shadow-neu-button active:shadow-neu-button-active border border-white/70 hover:text-slate-900 transition-all"
          >
            Done
          </button>
        </div>

      </div>
    </div>
  );
};
