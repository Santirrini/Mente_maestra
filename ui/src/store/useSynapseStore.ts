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

interface SynapseState {
  isConnected: boolean;
  activeNodeId: string | null;
  logs: LogEntry[];
  messages: ChatMessage[];
  setConnected: (status: boolean) => void;
  setActiveNode: (nodeId: string | null) => void;
  addLog: (log: LogEntry) => void;
  addMessage: (message: ChatMessage) => void;
}

export const useSynapseStore = create<SynapseState>((set) => ({
  isConnected: false,
  activeNodeId: null,
  logs: [],
  messages: [],
  setConnected: (status) => set({ isConnected: status }),
  setActiveNode: (nodeId) => set({ activeNodeId: nodeId }),
  addLog: (log) => set((state) => ({ logs: [...state.logs.slice(-50), log] })),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
}));
