import React from 'react';
import { Shield, Eye, Cpu } from 'lucide-react';
import { useSynapseStore } from '../../store/useSynapseStore';

const NodeManager: React.FC = () => {
  const activeNodeId = useSynapseStore((state) => state.activeNodeId);

  const agents = [
    { 
      name: 'Vision', 
      node: 'analyzer',
      icon: <Eye size={14} />,
      status: activeNodeId === 'analyzer' ? 'active' : 'online'
    },
    { 
      name: 'Guardian', 
      node: 'guardian',
      icon: <Shield size={14} />,
      status: activeNodeId === 'guardian' ? 'active' : 'online'
    },
    { 
      name: 'Ollama', 
      node: 'none',
      icon: <Cpu size={14} />,
      status: 'offline' 
    },
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
                <span className={`${agent.status === 'active' ? 'text-blue-400' : 'text-slate-400'} transition-colors`}>
                  {agent.icon}
                </span>
                <span className={`${agent.status === 'active' ? 'text-blue-200 font-bold' : 'text-slate-300'} transition-colors`}>
                  {agent.name}
                </span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                  agent.status === 'active' 
                    ? 'bg-blue-400 shadow-[0_0_8px_rgba(96,165,250,0.8)] scale-125' 
                    : agent.status === 'online' 
                      ? 'bg-green-500' 
                      : 'bg-red-500'
                }`}></span>
                <span className={`text-[9px] uppercase font-mono transition-colors ${
                  agent.status === 'active' ? 'text-blue-400 font-bold' : 'text-slate-500'
                }`}>
                  {agent.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default NodeManager;