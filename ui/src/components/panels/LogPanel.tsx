import React from 'react';
import { useSynapseStore } from '../../store/useSynapseStore';

const LogPanel: React.FC = () => {
  const logs = useSynapseStore((state) => state.logs);

  return (
    <section 
      data-testid="log-panel" 
      className="w-full h-full flex flex-col bg-slate-900/50"
    >
      <div className="p-4 border-b border-slate-800 font-bold tracking-tight">
        BLACKBOARD_LOGS
      </div>
      <div className="flex-1 overflow-y-auto p-3 font-mono text-[10px] space-y-2">
        {logs.length === 0 ? (
          <div className="text-slate-700 italic">No logs recorded yet.</div>
        ) : (
          logs.map((log, i) => (
            <div key={i} className="flex gap-2">
              <span className="text-slate-600">[{log.timestamp}]</span>
              <span className="text-blue-400 font-bold">{log.source}:</span>
              <span className="text-slate-400 break-words flex-1">{log.message}</span>
            </div>
          ))
        )}
      </div>
    </section>
  );
};

export default LogPanel;