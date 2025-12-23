import { useEffect, useRef } from 'react';
import { useSynapseStore } from '../store/useSynapseStore';

export const useSynapseWS = (url: string) => {
  const socketRef = useRef<WebSocket | null>(null);
  const { setConnected, addLog, setActiveNode } = useSynapseStore();

  useEffect(() => {
    const connect = () => {
      const socket = new WebSocket(url);
      socketRef.current = socket;

      socket.onopen = () => {
        console.log('WS Connected');
        setConnected(true);
      };

      socket.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        const { channel, data } = payload;

        if (channel === 'synapse:contributions') {
          addLog({
            timestamp: new Date().toLocaleTimeString(),
            source: data.agent_id || 'UNKNOWN',
            message: data.content,
          });
        } else if (channel === 'synapse:state_updates') {
          setActiveNode(data.active_node || null);
        }
      };

      socket.onclose = () => {
        console.log('WS Disconnected');
        setConnected(false);
        // Attempt reconnect after 3 seconds
        setTimeout(connect, 3000);
      };

      socket.onerror = (error) => {
        console.error('WS Error:', error);
        socket.close();
      };
    };

    connect();

    return () => {
      socketRef.current?.close();
    };
  }, [url, setConnected, addLog, setActiveNode]);

  return socketRef.current;
};
