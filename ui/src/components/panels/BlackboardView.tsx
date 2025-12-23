import React from 'react';
import { useSynapseStore } from '../../store/useSynapseStore';
import { Brain, MessageSquare, Clock } from 'lucide-react';

const BlackboardView: React.FC = () => {
    const contributions = useSynapseStore((state) => state.contributions);

    return (
        <div className="flex flex-col h-full gap-4 p-4 overflow-y-auto">
            <div className="flex items-center gap-2 mb-2">
                <Brain className="w-5 h-5 text-cyan-400" />
                <h2 className="text-sm font-bold tracking-widest uppercase text-slate-400">
                    Pizarra Compartida (Shared State)
                </h2>
            </div>

            <div className="grid grid-cols-1 gap-4">
                {contributions.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-40 border border-dashed rounded-xl border-slate-800 bg-slate-900/20">
                        <Clock className="w-8 h-8 mb-2 text-slate-700" />
                        <p className="text-xs text-slate-500 font-mono">EN ESPERA DE CONTRIBUCIONES...</p>
                    </div>
                ) : (
                    contributions.map((contribution, index) => (
                        <div
                            key={index}
                            className="synapse-card group animate-in fade-in slide-in-from-bottom-2 duration-500"
                        >
                            <div className="p-3 bg-slate-800/50 flex items-center justify-between border-b border-slate-700">
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 rounded-full bg-cyan-500 pulse-cyan" />
                                    <span className="text-[10px] font-bold text-cyan-400 uppercase tracking-tighter">
                                        {contribution.agent_id}
                                    </span>
                                </div>
                                <span className="text-[9px] text-slate-500 font-mono">
                                    {new Date(contribution.timestamp).toLocaleTimeString()}
                                </span>
                            </div>
                            <div className="p-4 bg-slate-900/40">
                                <p className="text-sm text-slate-200 leading-relaxed font-sans">
                                    {contribution.content}
                                </p>
                                {contribution.metadata && Object.keys(contribution.metadata).length > 0 && (
                                    <div className="mt-3 pt-3 border-t border-slate-800 border-dashed">
                                        <div className="flex flex-wrap gap-2">
                                            {Object.entries(contribution.metadata).map(([key, value]) => (
                                                <span key={key} className="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-slate-400 font-mono border border-slate-700">
                                                    {key}: {String(value)}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default BlackboardView;
