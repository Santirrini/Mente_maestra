import React from 'react';
import { useSynapseStore } from '../../store/useSynapseStore';
import { CheckCircle2, Circle, PlayCircle, Loader2 } from 'lucide-react';

const phases = ['IDLE', 'ANALYZING', 'VALIDATING', 'EXECUTING'];

const StateMachineView: React.FC = () => {
    const currentPhase = useSynapseStore((state) => state.currentPhase);
    const currentIndex = phases.indexOf(currentPhase);

    return (
        <div className="p-4 h-full flex flex-col">
            <div className="flex items-center gap-2 mb-6">
                <Activity className="w-5 h-5 text-rose-400" />
                <h2 className="text-sm font-bold tracking-widest uppercase text-slate-400">
                    Máquina de Estados
                </h2>
            </div>

            <div className="space-y-6 relative ml-4 border-l border-slate-800 pl-8">
                {phases.map((phase, index) => {
                    const isDone = index < currentIndex;
                    const isActive = index === currentIndex;
                    const isPending = index > currentIndex;

                    return (
                        <div key={phase} className="relative group">
                            {/* Indicator */}
                            <div className={`absolute -left-[41px] top-1 p-1 rounded-full bg-slate-950 border-2 ${isDone ? 'border-emerald-500 text-emerald-500' :
                                    isActive ? 'border-cyan-500 text-cyan-500 glow-cyan' :
                                        'border-slate-800 text-slate-700'
                                }`}>
                                {isDone ? <CheckCircle2 className="w-4 h-4" /> :
                                    isActive ? <Loader2 className="w-4 h-4 animate-spin" /> :
                                        <Circle className="w-4 h-4" />}
                            </div>

                            <div>
                                <h3 className={`text-xs font-bold uppercase tracking-widest ${isDone ? 'text-slate-400' :
                                        isActive ? 'text-cyan-400' :
                                            'text-slate-600'
                                    }`}>
                                    {phase}
                                </h3>
                                {isActive && (
                                    <p className="text-[10px] text-cyan-500/60 font-mono mt-1 animate-pulse">
                                        AGENTES ACTIVOS...
                                    </p>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>

            <div className="mt-auto pt-6 border-t border-slate-800">
                <button className="w-full py-3 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg font-bold text-xs uppercase tracking-[0.2em] transition-all transform hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-cyan-900/20">
                    Iniciar Ciclo de Orquestación
                </button>
            </div>
        </div>
    );
};

// Temporal icons import workaround if not passed correctly
import { Activity as ActivityIcon } from 'lucide-react';
const Activity = ActivityIcon;

export default StateMachineView;
