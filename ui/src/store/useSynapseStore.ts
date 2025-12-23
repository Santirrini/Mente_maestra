import { create } from 'zustand';

interface SynapseState {
  isConnected: boolean;
  activeNodeId: string | null;
  setConnected: (status: boolean) => void;
  setActiveNode: (nodeId: string | null) => void;
}

export const useSynapseStore = create<SynapseState>((set) => ({
  isConnected: false,
  activeNodeId: null,
  setConnected: (status) => set({ isConnected: status }),
  setActiveNode: (nodeId) => set({ activeNodeId: nodeId }),
}));