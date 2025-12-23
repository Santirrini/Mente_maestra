import React from 'react';
import ChatPanel from './components/panels/ChatPanel';
import LogPanel from './components/panels/LogPanel';
import NodeManager from './components/panels/NodeManager';

import GraphCanvas from './components/graph/GraphCanvas';

function App() {
  return (
    <div className="flex h-screen w-full bg-slate-950 text-slate-50 overflow-hidden font-sans">
      {/* Panel Izquierdo: Chat */}
      <aside className="w-80 flex-shrink-0 border-r border-slate-800">
        <ChatPanel />
      </aside>

      {/* Panel Central: Grafo */}
      <main 
        data-testid="graph-panel" 
        className="flex-1 relative bg-slate-950 overflow-hidden"
      >
        <div className="absolute top-4 left-4 z-10 bg-slate-900/80 backdrop-blur-md border border-slate-800 rounded-md p-2 px-3 text-xs font-mono text-slate-400">
          ORCHESTRATOR_GRAPH
        </div>
        
        <NodeManager />

        <div className="h-full w-full">
          <GraphCanvas />
        </div>
      </main>

      {/* Panel Derecho: Logs/Pizarra */}
      <aside className="w-80 flex-shrink-0 border-l border-slate-800">
        <LogPanel />
      </aside>
    </div>
  );
}

export default App;
