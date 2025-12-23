import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useSynapseStore } from '../../store/useSynapseStore';
import { Send, Terminal, Cpu, History } from 'lucide-react';

const ChatPanel: React.FC = () => {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { messages, addMessage, isConnected } = useSynapseStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const res = await axios.get('/api/v1/chat/history');
        if (Array.isArray(res.data)) {
          res.data.forEach((msg: any) => {
            const exists = useSynapseStore.getState().messages.some(m => m.id === msg.id);
            if (!exists) {
              addMessage(msg);
            }
          });
        }
      } catch (error) {
        console.error("Failed to load chat history", error);
      }
    };
    loadHistory();
  }, [addMessage]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const cmd = input;
    setInput('');
    setIsLoading(true);

    try {
      const userMsgId = Date.now().toString();
      addMessage({
        id: userMsgId,
        role: 'user',
        content: cmd,
      });

      await axios.post('/api/v1/execute', { command: cmd });

    } catch (error) {
      console.error('Error sending command:', error);
      addMessage({
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Error: Failed to execute command. Is the backend running?',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section
      data-testid="chat-panel"
      className="w-full h-full flex flex-col bg-slate-900/10 backdrop-blur-sm"
    >
      <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/40">
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-cyan-400" />
          <span className="text-[10px] font-bold tracking-widest text-slate-400 uppercase">Input Terminal</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[9px] font-mono text-slate-500 uppercase">{isConnected ? 'Operational' : 'Offline'}</span>
          <span className={`w-1.5 h-1.5 rounded-full ${isConnected ? 'bg-cyan-500 shadow-[0_0_8px_rgba(6,182,212,0.5)]' : 'bg-slate-700'}`}></span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
        {messages.length === 0 ? (
          <div className="p-4 rounded-xl border border-slate-800/50 bg-slate-900/40 text-center">
            <Cpu className="w-8 h-8 mx-auto mb-3 text-slate-700" />
            <p className="text-[10px] text-slate-500 uppercase font-bold tracking-tighter">Esperando instrucciones...</p>
          </div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`max-w-[90%] p-3 rounded-2xl text-[13px] leading-relaxed shadow-lg ${msg.role === 'user'
                  ? 'bg-cyan-600/20 border border-cyan-500/20 text-cyan-50 rounded-tr-none'
                  : 'bg-slate-800/80 border border-slate-700/50 text-slate-300 rounded-tl-none'
                }`}>
                {msg.content}
              </div>
              <span className="text-[9px] mt-1 text-slate-600 font-mono px-1 uppercase tracking-tighter">
                {msg.role}
              </span>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-slate-950/40 border-t border-slate-800/60">
        <div className="relative group">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            disabled={isLoading}
            placeholder={isLoading ? "Enviando pulso..." : "Escriba un comando..."}
            className="w-full bg-slate-900/80 border border-slate-700/50 rounded-xl p-3 pr-12 text-sm focus:outline-none focus:ring-1 focus:ring-cyan-500/50 transition-all disabled:opacity-50 placeholder:text-slate-600"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="absolute right-2 top-2 p-1.5 rounded-lg bg-cyan-600/10 text-cyan-500 hover:bg-cyan-600 hover:text-white transition-all disabled:opacity-0"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </section>
  );
};

export default ChatPanel;