# Specification: Live Execution & Interaction

## Overview
Este track cierra el ciclo de feedback entre la UI y el núcleo de orquestación. Permite enviar comandos desde el chat, disparar la lógica del orquestador y visualizar en tiempo real la activación de nodos y agentes mediante cambios de color y logs fluidos.

## Functional Requirements
- **Trigger de Ejecución:** Endpoint `POST /api/v1/execute` para iniciar flujos de agentes.
- **Instrumentación Automática:** Callbacks en LangGraph para reportar el `active_node` a Redis.
- **Feedback de Agentes (NodeManager):** Cambio de color (ej. verde -> azul brillante) cuando un agente está activo.
- **Persistencia Mínima:** Almacenamiento y recuperación de mensajes y logs recientes desde Redis.
- **Visualización del Grafo:** Resaltado dinámico del nodo en ejecución en `GraphCanvas`.

## Technical Decisions
- **Backend:** FastAPI + Redis Pub/Sub para eventos de estado.
- **Frontend:** Zustand para gestionar el estado global de ejecución.
- **Persistencia:** Uso de listas en Redis para el historial circular de la sesión.

## Acceptance Criteria
- [ ] El chat envía comandos que inician la ejecución del backend.
- [ ] Los nodos del grafo y los indicadores del NodeManager cambian de color según el agente activo.
- [ ] Los logs y mensajes persisten tras recargar la página (mientras Redis esté activo).
- [ ] La respuesta final del asistente aparece en el chat al terminar el flujo.
