import React from 'react';
import ChatPanel from './components/panels/ChatPanel';
import BlackboardView from './components/panels/BlackboardView';
import GovernanceModule from './components/panels/GovernanceModule';
import StateMachineView from './components/panels/StateMachineView';
import GraphCanvas from './components/graph/GraphCanvas';
import { useSynapseWS } from './hooks/useSynapseWS';
import { Zap, Brain, Shield } from 'lucide-react';

function App() {
  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${wsProtocol}//${window.location.host}/ws`;

  useSynapseWS(wsUrl);

  return (
    <div className="flex flex-col h-screen w-full bg-slate-950 text-slate-50 overflow-hidden selection:bg-cyan-500/30">
      {/* Top Header */}
      <header className="h-16 flex-shrink-0 border-b border-slate-800/60 bg-slate-900/40 backdrop-blur-md flex items-center justify-between px-6 z-50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
                Synapse Control Plane
              </h1>
              <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 font-bold">
                v1.0 (Hybrid MAS)
              </span>
            </div>
            <p className="text-[10px] text-slate-500 font-medium uppercase tracking-wider">
              Orquestación de Agentes con Gobernanza en Tiempo Real
            </p>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs font-mono text-emerald-500 uppercase">System Optimal</span>
          </div>
          <button className="px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-xs font-bold uppercase tracking-widest transition-colors">
            Configuración
          </button>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Left Section: Chat & Control */}
        <aside className="w-80 flex-shrink-0 border-r border-slate-800/60 flex flex-col bg-slate-900/20">
          <ChatPanel />
        </aside>

        {/* Middle Section: Blackboard & Graph */}
        <main className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 min-h-0 relative">
            <div className="absolute inset-0 opacity-20 pointer-events-none bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:16px_16px]" />
            <div className="h-full w-full overflow-hidden flex flex-col">
              <div className="flex-1 overflow-hidden">
                <BlackboardView />
              </div>
              <div className="h-[300px] border-t border-slate-800/60 bg-slate-900/10 relative">
                <div className="absolute top-4 left-4 z-20 text-[10px] font-mono text-slate-500 flex items-center gap-2">
                  <Brain className="w-3 h-3" /> GRAPH_TOPOLOGY_VIEW
                </div>
                <GraphCanvas />
              </div>
            </div>
          </div>
        </main>

        {/* Right Section: Governance & State Machine */}
        <aside className="w-96 flex-shrink-0 border-l border-slate-800/60 flex flex-col bg-slate-900/20">
          <div className="flex-1 border-b border-slate-800/60 overflow-y-auto">
            <StateMachineView />
          </div>
          <div className="h-fit">
            <GovernanceModule />
          </div>
        </aside>
      </div>
    </div>
  );
}

export default App;