import React from 'react';
import { useSynapseStore } from '../../store/useSynapseStore';
import { ShieldCheck, Lock, Activity, Zap } from 'lucide-react';

const GovernanceModule: React.FC = () => {
    const { governance, metrics } = useSynapseStore();

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'APPROVED': return 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20';
            case 'AUDITED': return 'text-cyan-400 bg-cyan-400/10 border-cyan-400/20';
            case 'REJECTED': return 'text-rose-400 bg-rose-400/10 border-rose-400/20';
            default: return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
        }
    };

    return (
        <div data-testid="governance-module" className="p-4 space-y-4">
            <div className="flex items-center gap-2 mb-4">
                <ShieldCheck className="w-5 h-5 text-emerald-400" />
                <h2 className="text-sm font-bold tracking-widest uppercase text-slate-400">
                    Módulo de Gobernanza (Guardian)
                </h2>
            </div>

            <div className="grid grid-cols-1 gap-3">
                {/* Habeas Data */}
                <div className="flex items-center justify-between p-3 synapse-glass rounded-lg border border-slate-800">
                    <div className="flex items-center gap-3">
                        <Lock className="w-4 h-4 text-slate-500" />
                        <span className="text-xs text-slate-300">Privacidad (Habeas Data)</span>
                    </div>
                    <span className={`synapse-badge border ${getStatusColor(governance.habeasData)}`}>
                        {governance.habeasData}
                    </span>
                </div>

                {/* Neutrality */}
                <div className="flex items-center justify-between p-3 synapse-glass rounded-lg border border-slate-800">
                    <div className="flex items-center gap-3">
                        <ShieldCheck className="w-4 h-4 text-slate-500" />
                        <span className="text-xs text-slate-300">Neutralidad y Sesgo</span>
                    </div>
                    <span className={`synapse-badge border ${getStatusColor(governance.neutrality)}`}>
                        {governance.neutrality}
                    </span>
                </div>
            </div>

            <div className="mt-6 pt-6 border-t border-slate-800">
                <div className="grid grid-cols-2 gap-4">
                    <div className="synapse-card p-3 flex flex-col items-center">
                        <Activity className="w-4 h-4 text-cyan-500 mb-2" />
                        <span className="text-[10px] text-slate-500 uppercase">GPU Usage</span>
                        <span className="text-xl font-bold font-mono text-slate-200">{metrics.gpuUsage}%</span>
                    </div>
                    <div className="synapse-card p-3 flex flex-col items-center">
                        <Zap className="w-4 h-4 text-emerald-500 mb-2" />
                        <span className="text-[10px] text-slate-500 uppercase">Efficiency</span>
                        <span className="text-xl font-bold font-mono text-slate-200">{metrics.efficiency}%</span>
                    </div>
                </div>

                <div className="mt-4 p-4 rounded-xl bg-emerald-500/5 border border-emerald-500/20 flex items-center gap-4">
                    <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                        <Activity className="w-5 h-5" />
                    </div>
                    <div>
                        <p className="text-[10px] uppercase font-bold text-emerald-500 tracking-wider">Resultado Validado</p>
                        <p className="text-xs text-slate-300 leading-tight">Sistema operando bajo parámetros de seguridad normativa corporativa.</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GovernanceModule;
