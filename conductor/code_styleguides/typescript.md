# Guía de Desarrollo: Frontend TypeScript (Synapse)

Esta guía define los estándares para construir la interfaz de Synapse. En nuestro ecosistema, TypeScript no es solo un lenguaje, es el sistema somatosensorial que garantiza que la información de los agentes se procese con total integridad.

## 1. Tipado como Propriocepción
La propriocepción nos permite conocer la posición de nuestro cuerpo sin mirarlo. En Synapse, los Interfaces y Types nos permiten conocer la forma de los datos sin ejecutar el código.

- **Contratos con el Backend:** Cada modelo de Pydantic en Python debe tener su espejo exacto en TypeScript.
- **Regla de Oro:** **Prohibido el uso de `any`**. Usar `any` es equivalente a una neuropatía sensorial: el sistema sigue funcionando, pero no tiene idea de qué está tocando, aumentando el riesgo de caídas (crashes).

```typescript
// Definición de la Pizarra (Blackboard)
export type AgentPhase = 'IDLE' | 'ANALYZING' | 'VALIDATING' | 'EXECUTING';

export interface AgentContribution {
  agentId: string;
  timestamp: number;
  content: string;
  metadata?: Record<string, unknown>;
}

export interface SynapseState {
  currentPhase: AgentPhase;
  blackboard: {
    contributions: AgentContribution[];
    isCompliant: boolean;
    logs: string[];
  };
}
```

## 2. Zustand: La Memoria Sináptica (Pizarra)
Para la arquitectura de Pizarra, utilizaremos **Zustand**. Es un gestor de estado atómico que permite a cualquier componente (neurona) acceder a la información global sin necesidad de pasar props por niveles intermedios.

- **Sincronización:** El estado de Zustand debe reflejar lo que ocurre en el backend de FastAPI en tiempo real.
- **Acciones:** Define funciones claras para modificar el estado, evitando mutaciones directas.

```typescript
import { create } from 'zustand';

interface SynapseStore extends SynapseState {
  addContribution: (contribution: AgentContribution) => void;
  setPhase: (phase: AgentPhase) => void;
}

export const useSynapseStore = create<SynapseStore>((set) => ({
  currentPhase: 'IDLE',
  blackboard: { contributions: [], isCompliant: false, logs: [] },
  
  addContribution: (newEntry) => set((state) => ({
    blackboard: {
      ...state.blackboard,
      contributions: [...state.blackboard.contributions, newEntry]
    }
  })),
  setPhase: (phase) => set({ currentPhase: phase }),
}));
```

## 3. Componentes: Sinergias Musculares
Un movimiento fluido es el resultado de sinergias musculares. En React, nuestros componentes deben ser modulares y altamente tipados.

- **Props Tipadas:** Todo componente debe definir sus entradas.
- **Hooks de Reacción:** Usa `useEffect` para reaccionar a cambios en la "Pizarra" y disparar animaciones o actualizaciones visuales.

## 4. Tipado de Agentes Multimodales
Dado que Synapse gestiona video, audio e imágenes, debemos tipar los inputs sensoriales:

```typescript
type MediaType = 'IMAGE' | 'VIDEO' | 'AUDIO';

interface MultimodalInput {
  type: MediaType;
  sourceUrl: string;
  samplingRate?: number; // Específico para audio
  resolution?: { width: number; height: number }; // Específico para video/imagen
}
```

## 5. Workflow en Fedora
Al desarrollar en tu entorno de Fedora, asegúrate de:
- **Strict Mode:** Mantén `"strict": true` en tu `tsconfig.json`. Es nuestro control de calidad fisiológico.
- **Linter como Guardián:** Utiliza ESLint con reglas de TypeScript para detectar "arritmias" en el código antes de compilar.
- **Vite HMR:** Aprovecha la recarga rápida de Vite para probar ajustes en la interfaz con la velocidad de un impulso nervioso.

> "Un sistema sin tipos es un cuerpo sin sensibilidad. TypeScript nos da la seguridad de que, cuando un agente envía una señal, la interfaz sabe exactamente cómo reaccionar, transformando datos crudos en movimiento coordinado."
