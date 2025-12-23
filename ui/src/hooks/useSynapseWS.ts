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
              setActiveNode(null);
            }
          } else if (channel === 'synapse:state_updates') {
            setActiveNode(data.active_node || null);
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