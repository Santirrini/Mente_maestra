import React from 'react';

const ChatPanel: React.FC = () => {
  return (
    <section 
      data-testid="chat-panel" 
      className="w-full h-full flex flex-col bg-slate-900/50"
    >
      <div className="p-4 border-b border-slate-800 font-bold tracking-tight flex items-center justify-between">
        <span>SYNPSE_CHAT</span>
        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <div className="bg-slate-800/30 p-3 rounded-lg border border-slate-800 text-xs text-slate-400">
          Esperando instrucciones...
        </div>
      </div>
      <div className="p-4 border-t border-slate-800">
        <div className="relative">
          <input 
            type="text" 
            placeholder="Enviar comando..." 
            className="w-full bg-slate-950 border border-slate-700 rounded-md p-2 pr-10 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 transition-all"
          />
          <button className="absolute right-2 top-1.5 text-slate-500 hover:text-blue-400">
            ↵
          </button>
        </div>
      </div>
    </section>
  );
};

export default ChatPanel;
