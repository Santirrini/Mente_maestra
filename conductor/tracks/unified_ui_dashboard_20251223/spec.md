# Specification: Synapse Unified UI Dashboard

## Overview
Este track tiene como objetivo implementar la interfaz de usuario inicial para el Synapse Control Plane. Se desarrollará un panel de control unificado y minimalista utilizando **React (TypeScript)**, **Tailwind CSS** y **Zustand** para la gestión de estado, permitiendo la observabilidad en tiempo real y el control interactivo del sistema multiagente.

## Functional Requirements
- **Unified Control Panel (Layout A):**
    - **Sección Izquierda (Interacción):** Chat interactivo para enviar prompts al orquestador y recibir respuestas paso a paso.
    - **Sección Central (Grafo de Orquestación):** Visualización dinámica de los nodos de LangGraph usando **ReactFlow**, resaltando el nodo activo durante la ejecución.
    - **Sección Derecha (Pizarra en Tiempo Real):** Feed de logs detallados provenientes de Redis, mostrando la actividad interna de los agentes.
- **Gestión de Nodos:**
    - Indicadores de salud (online/offline) para cada agente (Visión, Guardián, Ollama).
    - Interruptores (toggles) para habilitar/deshabilitar agentes manualmente.
- **Comunicación en Tiempo Real:**
    - Integración mediante **WebSockets** para recibir actualizaciones de la Pizarra y el estado del grafo sin necesidad de refrescar la página.

## Non-Functional Requirements
- **Estética:** Diseño minimalista "vanguardista" alineado con la identidad de Synapse.
- **Rendimiento:** Latencia mínima en la actualización de logs (vía WebSockets).
- **Tipado:** Uso estricto de TypeScript para garantizar la integridad de los datos entre el frontend y el backend.
- **Estado:** Gestión de estado centralizada con Zustand para manejar flujos asíncronos y actualizaciones de tiempo real.

## Acceptance Criteria
- [ ] El usuario puede enviar un mensaje y ver la respuesta del orquestador en la interfaz.
- [ ] El grafo visual se actualiza indicando qué agente está procesando la información.
- [ ] Los logs de Redis aparecen en la sección de la Pizarra en tiempo real.
- [ ] Se puede cambiar el estado (on/off) de al menos un agente desde la UI.

## Out of Scope
- Configuración avanzada de parámetros de modelos LLM desde la UI en esta fase.
- Persistencia de historial de chat en base de datos.
