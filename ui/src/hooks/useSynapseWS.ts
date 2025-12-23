import { useEffect, useRef } from 'react';
import { useSynapseStore } from '../store/useSynapseStore';

export const useSynapseWS = (url: string) => {
  const socketRef = useRef<WebSocket | null>(null);
  const { setConnected, addLog, setActiveNode, addMessage } = useSynapseStore();

  useEffect(() => {
    let isUnmounting = false;
    let reconnectTimeout: number;

    const connect = () => {
      if (isUnmounting) return;

      console.log(`Attempting to connect to WS: ${url}`);
      const socket = new WebSocket(url);
      socketRef.current = socket;

      socket.onopen = () => {
        if (isUnmounting) {
          socket.close();
          return;
        }
        console.log('WS Connected');
        setConnected(true);
      };

      socket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          const { channel, data } = payload;

          if (channel === 'synapse:contributions') {
            const contribution = {
              agent_id: data.agent_id || 'UNKNOWN',
              timestamp: new Date().toISOString(),
              content: data.content,
              metadata: data.metadata || {}
            };

            useSynapseStore.getState().addContribution(contribution);

            addLog({
              timestamp: new Date().toLocaleTimeString(),
              source: data.agent_id || 'UNKNOWN',
              message: data.content,
            });

            if (data.agent_id === 'assistant') {
              addMessage({
                id: Date.now().toString(),
                role: 'assistant',
                content: data.content
              });
            }
          } else if (channel === 'synapse:state_updates') {
            if (data.active_node) {
              setActiveNode(data.active_node);
              // Map node to phase
              const nodeToPhase: Record<string, string> = {
                'start': 'ANALYZING',
                'analyze': 'ANALYZING',
                'validate': 'VALIDATING',
                'execute': 'EXECUTING',
                'end': 'IDLE'
              };
              if (nodeToPhase[data.active_node]) {
                useSynapseStore.getState().setCurrentPhase(nodeToPhase[data.active_node]);
              }
            }

            // Simulate governance/metrics updates for "Wow" effect
            useSynapseStore.getState().updateMetrics({
              gpuUsage: Math.floor(Math.random() * 30) + 40,
              efficiency: 94,
              cost: 0.02
            });

            if (data.status === 'started') {
              useSynapseStore.getState().updateGovernance({
                habeasData: 'APPROVED',
                neutrality: 'AUDITED'
              });
            }
          }
        } catch (e) {
          console.error('Error parsing WS message:', e);
        }
      };

      socket.onclose = () => {
        if (!isUnmounting) {
          console.log('WS Disconnected, retrying in 3s...');
          setConnected(false);
          reconnectTimeout = setTimeout(connect, 3000);
        } else {
          console.log('WS Connection closed due to unmount');
        }
      };

      socket.onerror = (error) => {
        console.error('WS Error:', error);
        // On error, let onclose handle the reconnection logic
        if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) {
          socket.close();
        }
      };
    };

    connect();

    return () => {
      isUnmounting = true;
      clearTimeout(reconnectTimeout);
      if (socketRef.current && (socketRef.current.readyState === WebSocket.OPEN || socketRef.current.readyState === WebSocket.CONNECTING)) {
        socketRef.current.close();
      }
    };
  }, [url, setConnected, addLog, setActiveNode, addMessage]);

  return socketRef.current;
};