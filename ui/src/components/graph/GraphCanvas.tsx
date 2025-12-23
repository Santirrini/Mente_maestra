import React, { useMemo } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  Node, 
  Edge,
  ConnectionLineType
} from 'reactflow';
import 'reactflow/dist/style.css';
import { useSynapseStore } from '../../store/useSynapseStore';

const GraphCanvas: React.FC = () => {
  const activeNodeId = useSynapseStore((state) => state.activeNodeId);

  const initialNodes: Node[] = useMemo(() => [
    { 
      id: 'start', 
      position: { x: 100, y: 150 }, 
      data: { label: 'START' },
      style: { 
        background: '#0f172a', 
        color: '#94a3b8', 
        border: activeNodeId === 'start' ? '1px solid #60a5fa' : '1px solid #1e293b', 
        boxShadow: activeNodeId === 'start' ? '0 0 15px rgba(96, 165, 250, 0.4)' : 'none',
        borderRadius: '4px', 
        fontSize: '10px' 
      }
    },
    { 
      id: 'orchestrator', 
      position: { x: 300, y: 150 }, 
      data: { label: 'ORCHESTRATOR' },
      style: { 
        background: '#1e1b4b', 
        color: '#e2e8f0', 
        border: activeNodeId === 'orchestrator' ? '1px solid #818cf8' : '1px solid #3730a3', 
        boxShadow: activeNodeId === 'orchestrator' ? '0 0 20px rgba(129, 140, 248, 0.5)' : 'none',
        borderRadius: '4px', 
        fontSize: '10px', 
        fontWeight: 'bold' 
      }
    },
    { 
      id: 'vision', 
      position: { x: 500, y: 80 }, 
      data: { label: 'VISION_AGENT' },
      style: { 
        background: '#0f172a', 
        color: '#94a3b8', 
        border: activeNodeId === 'vision' ? '1px solid #60a5fa' : '1px solid #1e293b', 
        boxShadow: activeNodeId === 'vision' ? '0 0 15px rgba(96, 165, 250, 0.4)' : 'none',
        borderRadius: '4px', 
        fontSize: '10px' 
      }
    },
    { 
      id: 'guardian', 
      position: { x: 500, y: 220 }, 
      data: { label: 'GUARDIAN_AGENT' },
      style: { 
        background: '#0f172a', 
        color: '#94a3b8', 
        border: activeNodeId === 'guardian' ? '1px solid #60a5fa' : '1px solid #1e293b', 
        boxShadow: activeNodeId === 'guardian' ? '0 0 15px rgba(96, 165, 250, 0.4)' : 'none',
        borderRadius: '4px', 
        fontSize: '10px' 
      }
    },
  ], [activeNodeId]);

  const initialEdges: Edge[] = useMemo(() => [
    { id: 'e1-2', source: 'start', target: 'orchestrator', animated: activeNodeId === 'start', style: { stroke: activeNodeId === 'start' ? '#60a5fa' : '#334155' } },
    { id: 'e2-3', source: 'orchestrator', target: 'vision', animated: activeNodeId === 'orchestrator', style: { stroke: activeNodeId === 'orchestrator' ? '#818cf8' : '#334155' } },
    { id: 'e2-4', source: 'orchestrator', target: 'guardian', animated: activeNodeId === 'orchestrator', style: { stroke: activeNodeId === 'orchestrator' ? '#818cf8' : '#334155' } },
  ], [activeNodeId]);

  return (
    <div 
      data-testid="react-flow-wrapper" 
      className="h-full w-full bg-slate-950"
    >
      <ReactFlow
        nodes={initialNodes}
        edges={initialEdges}
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