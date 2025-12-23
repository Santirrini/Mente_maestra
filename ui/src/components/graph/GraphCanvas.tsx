import React, { useMemo } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  ConnectionLineType
} from 'reactflow';
import type { Node, Edge } from 'reactflow';
import 'reactflow/dist/style.css';
import { useSynapseStore } from '../../store/useSynapseStore';

// Define base structure outside component to avoid recreation warnings
const BASE_NODES: Node[] = [
  { 
    id: 'start', 
    position: { x: 50, y: 150 }, 
    data: { label: 'START' },
    style: { borderRadius: '4px', fontSize: '10px' }
  },
  { 
    id: 'analyzer', 
    position: { x: 250, y: 150 }, 
    data: { label: 'ANALYZER' },
    style: { borderRadius: '4px', fontSize: '10px', fontWeight: 'bold' }
  },
  { 
    id: 'guardian', 
    position: { x: 450, y: 150 }, 
    data: { label: 'GUARDIAN' },
    style: { borderRadius: '4px', fontSize: '10px' }
  },
  { 
    id: 'responder', 
    position: { x: 650, y: 150 }, 
    data: { label: 'RESPONDER' },
    style: { borderRadius: '4px', fontSize: '10px' }
  },
];

const BASE_EDGES: Edge[] = [
  { id: 'e-start-analyzer', source: 'start', target: 'analyzer' },
  { id: 'e-analyzer-guardian', source: 'analyzer', target: 'guardian' },
  { id: 'e-guardian-responder', source: 'guardian', target: 'responder' },
  { id: 'e-guardian-analyzer', source: 'guardian', target: 'analyzer', animated: false, style: { stroke: '#1e293b', strokeDasharray: '5,5' }, label: 'retry', labelStyle: { fill: '#475569', fontSize: '8px' } },
];

const GraphCanvas: React.FC = () => {
  const activeNodeId = useSynapseStore((state) => state.activeNodeId);

  const nodes: Node[] = useMemo(() => {
    return BASE_NODES.map(node => {
      const isActive = node.id === activeNodeId;
      let colors = { bg: '#0f172a', border: '#1e293b', activeBorder: '#60a5fa', text: '#94a3b8' };

      if (node.id === 'analyzer') colors = { bg: '#1e1b4b', border: '#3730a3', activeBorder: '#818cf8', text: '#e2e8f0' };
      if (node.id === 'responder') colors = { bg: '#064e3b', border: '#064e3b', activeBorder: '#10b981', text: '#34d399' };

      return {
        ...node,
        style: {
          ...node.style,
          background: colors.bg,
          color: colors.text,
          border: isActive ? `1px solid ${colors.activeBorder}` : `1px solid ${colors.border}`,
          boxShadow: isActive ? `0 0 15px ${colors.activeBorder}66` : 'none',
        }
      };
    });
  }, [activeNodeId]);

  const edges: Edge[] = useMemo(() => {
    return BASE_EDGES.map(edge => {
      // Logic: If target node is active, animate the incoming edge
      const isTargetActive = edge.target === activeNodeId;
      
      // Specific logic for start edge
      if (edge.source === 'start' && activeNodeId === 'start') {
          return { ...edge, animated: true, style: { ...edge.style, stroke: '#60a5fa' } };
      }

      return {
        ...edge,
        animated: isTargetActive,
        style: { 
          ...edge.style, 
          stroke: isTargetActive ? '#60a5fa' : '#334155' 
        }
      };
    });
  }, [activeNodeId]);

  return (
    <div 
      data-testid="react-flow-wrapper" 
      className="h-full w-full bg-slate-950"
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        connectionLineType={ConnectionLineType.SmoothStep}
        fitView
        nodesDraggable={true}
        nodesConnectable={false}
      >
        <Background color="#1e293b" gap={20} />
        <Controls showInteractive={false} className="bg-slate-900 border-slate-800 fill-slate-400" />
      </ReactFlow>
    </div>
  );
};

export default GraphCanvas;