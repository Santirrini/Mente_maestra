import React from 'react';
import { Shield, Eye, Cpu } from 'lucide-react';

const NodeManager: React.FC = () => {
  const agents = [
    { name: 'Vision', status: 'online', icon: <Eye size={14} /> },
    { name: 'Guardian', status: 'online', icon: <Shield size={14} /> },
    { name: 'Ollama', status: 'offline', icon: <Cpu size={14} /> },
  ];

  return (
    <div className="absolute top-4 right-4 z-10 flex flex-col gap-2">
      <div className="bg-slate-900/80 backdrop-blur-md border border-slate-800 rounded-md p-3 w-48 shadow-xl">
        <div className="text-[10px] font-bold text-slate-500 mb-3 tracking-widest uppercase">
          AGENTS_STATUS
        </div>
        <div className="space-y-3">
          {agents.map((agent) => (
            <div key={agent.name} className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs">
                <span className="text-slate-400">{agent.icon}</span>
                <span className="text-slate-300">{agent.name}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className={`w-1.5 h-1.5 rounded-full ${agent.status === 'online' ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <span className="text-[9px] text-slate-500 uppercase font-mono">{agent.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default NodeManager;
