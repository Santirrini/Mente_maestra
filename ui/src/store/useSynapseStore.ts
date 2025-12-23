import { create } from 'zustand';

interface SynapseState {
  isConnected: boolean;
  setConnected: (status: boolean) => void;
}

export const useSynapseStore = create<SynapseState>((set) => ({
  isConnected: false,
  setConnected: (status) => set({ isConnected: status }),
}));
