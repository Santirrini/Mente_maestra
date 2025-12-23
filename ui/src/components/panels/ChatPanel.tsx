import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useSynapseStore } from '../../store/useSynapseStore';

const ChatPanel: React.FC = () => {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { messages, addMessage, isConnected } = useSynapseStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load history on mount
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
  }, []); // Run once on mount

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
      className="w-full h-full flex flex-col bg-slate-900/50"
    >
      <div className="p-4 border-b border-slate-800 font-bold tracking-tight flex items-center justify-between">
        <span>SYNPSE_CHAT</span>
        <span className={`w-2 h-2 rounded-full transition-colors ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></span>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="bg-slate-800/30 p-3 rounded-lg border border-slate-800 text-xs text-slate-400">
            Esperando instrucciones...
          </div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`max-w-[85%] p-3 rounded-lg text-xs leading-relaxed ${
                msg.role === 'user' 
                  ? 'bg-blue-600/20 border border-blue-500/30 text-blue-100' 
                  : 'bg-slate-800 border border-slate-700 text-slate-300'
              }`}>
                {msg.content}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="p-4 border-t border-slate-800">
        <div className="relative">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            disabled={isLoading}
            placeholder={isLoading ? "Procesando..." : "Enviar comando..."}
            className="w-full bg-slate-950 border border-slate-700 rounded-md p-2 pr-10 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 transition-all disabled:opacity-50"
          />
          <button 
            onClick={handleSend}
            disabled={isLoading}
            className="absolute right-2 top-1.5 text-slate-500 hover:text-blue-400 disabled:text-slate-700"
          >
            {isLoading ? '...' : '↵'}
          </button>
        </div>
      </div>
    </section>
  );
};

export default ChatPanel;