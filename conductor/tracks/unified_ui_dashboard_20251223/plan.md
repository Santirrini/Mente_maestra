# Plan: Synapse Unified UI Dashboard

## Fase 1: Configuración del Entorno Frontend [checkpoint: TBD]
- [x] Task: Inicializar proyecto React con Vite, TypeScript y Tailwind CSS.
- [x] Task: Configurar librerías base (ReactFlow, Zustand, Lucide-React, Axios).
- [x] Task: Estructurar la jerarquía de componentes y definir el store de Zustand inicial.
- [ ] Task: Conductor - User Manual Verification 'Fase 1: Configuración del Entorno Frontend' (Protocol in workflow.md)

## Fase 2: Layout y Componentes Visuales (Estructura A) [checkpoint: TBD]
- [ ] Task: Implementar el Layout Unificado (Grid/Flexbox) con diseño minimalista.
- [ ] Task: Desarrollar el componente `ChatPanel` (Input y lista de mensajes).
- [ ] Task: Desarrollar el componente `LogPanel` para mostrar el flujo de la Pizarra.
- [ ] Task: Implementar el componente `NodeManager` para control de salud de agentes.
- [ ] Task: Conductor - User Manual Verification 'Fase 2: Layout y Componentes Visuales' (Protocol in workflow.md)

## Fase 3: Visualización del Grafo con ReactFlow [checkpoint: TBD]
- [ ] Task: Configurar el canvas de `ReactFlow` con estilos personalizados para Synapse.
- [ ] Task: Definir nodos y bordes personalizados que representen los agentes y el flujo de LangGraph.
- [ ] Task: Implementar lógica de resaltado de nodos basada en el estado de ejecución en el store de Zustand.
- [ ] Task: Conductor - User Manual Verification 'Fase 3: Visualización del Grafo con ReactFlow' (Protocol in workflow.md)

## Fase 4: Integración de Datos y WebSockets [checkpoint: TBD]
- [ ] Task: Implementar cliente de WebSocket en el frontend para conectar con FastAPI.
- [ ] Task: Vincular el flujo de mensajes del chat con el endpoint del orquestador.
- [ ] Task: Sincronizar el estado del grafo y los logs de la pizarra con los eventos de WebSocket vía Zustand.
- [ ] Task: Implementar toggles de control para habilitar/deshabilitar agentes desde la UI.
- [ ] Task: Conductor - User Manual Verification 'Fase 4: Integración de Datos y WebSockets' (Protocol in workflow.md)
