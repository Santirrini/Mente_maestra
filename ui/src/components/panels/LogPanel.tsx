import React from 'react';

const LogPanel: React.FC = () => {
  return (
    <section 
      data-testid="log-panel" 
      className="w-full h-full flex flex-col bg-slate-900/50"
    >
      <div className="p-4 border-b border-slate-800 font-bold tracking-tight">
        BLACKBOARD_LOGS
      </div>
      <div className="flex-1 overflow-y-auto p-3 font-mono text-[10px] space-y-2">
        <div className="flex gap-2">
          <span className="text-slate-600">[10:00:00]</span>
          <span className="text-blue-400">SYS:</span>
          <span className="text-slate-400">System initialized.</span>
        </div>
        <div className="flex gap-2">
          <span className="text-slate-600">[10:00:01]</span>
          <span className="text-purple-400">REDIS:</span>
          <span className="text-slate-400">Connected to blackboard.</span>
        </div>
      </div>
    </section>
  );
};

export default LogPanel;
