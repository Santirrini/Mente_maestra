import { create } from 'zustand';

export interface LogEntry {
  timestamp: string;
  source: string;
  message: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

export interface AgentContribution {
  agent_id: string;
  timestamp: string;
  content: string;
  metadata: Record<string, any>;
}

export interface GovernanceState {
  habeasData: 'APPROVED' | 'PENDING' | 'REJECTED';
  neutrality: 'AUDITED' | 'PENDING' | 'WAITING';
  isSafe: boolean;
}

export interface SynapseMetrics {
  gpuUsage: number;
  efficiency: number;
  cost: number;
}

interface SynapseState {
  isConnected: boolean;
  activeNodeId: string | null;
  currentPhase: string;
  logs: LogEntry[];
  messages: ChatMessage[];
  contributions: AgentContribution[];
  governance: GovernanceState;
  metrics: SynapseMetrics;

  setConnected: (status: boolean) => void;
  setActiveNode: (nodeId: string | null) => void;
  setCurrentPhase: (phase: string) => void;
  addLog: (log: LogEntry) => void;
  addMessage: (message: ChatMessage) => void;
  setContributions: (contributions: AgentContribution[]) => void;
  addContribution: (contribution: AgentContribution) => void;
  updateGovernance: (gov: Partial<GovernanceState>) => void;
  updateMetrics: (metrics: Partial<SynapseMetrics>) => void;
}

export const useSynapseStore = create<SynapseState>((set) => ({
  isConnected: false,
  activeNodeId: null,
  currentPhase: 'IDLE',
  logs: [],
  messages: [],
  contributions: [],
  governance: {
    habeasData: 'PENDING',
    neutrality: 'PENDING',
    isSafe: true,
  },
  metrics: {
    gpuUsage: 0,
    efficiency: 0,
    cost: 0,
  },

  setConnected: (status) => set({ isConnected: status }),
  setActiveNode: (nodeId) => set({ activeNodeId: nodeId }),
  setCurrentPhase: (phase) => set({ currentPhase: phase }),
  addLog: (log) => set((state) => ({ logs: [...state.logs.slice(-50), log] })),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setContributions: (contributions) => set({ contributions }),
  addContribution: (contribution) => set((state) => ({
    contributions: [...state.contributions, contribution]
  })),
  updateGovernance: (gov) => set((state) => ({
    governance: { ...state.governance, ...gov }
  })),
  updateMetrics: (metrics) => set((state) => ({
    metrics: { ...state.metrics, ...metrics }
  })),
}));
