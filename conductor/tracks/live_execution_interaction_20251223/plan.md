# Plan: Live Execution & Interaction

## Fase 1: Instrumentación del Backend [checkpoint: 7631261]
- [x] Task: Crear endpoint `POST /api/v1/execute` en FastAPI para disparar el orquestador.
- [x] Task: Implementar el sistema de callbacks en `Orchestrator` para emitir cambios de estado a Redis.
- [x] Task: Asegurar que el `Blackboard` mantenga el estado de la sesión (logs y mensajes) en Redis.
- [x] Task: Conductor - User Manual Verification 'Fase 1: Instrumentación del Backend' (Protocol in workflow.md)

## Fase 2: Feedback Visual en Tiempo Real [checkpoint: TBD]
- [ ] Task: Actualizar el componente `NodeManager` para reaccionar al `activeNodeId` (cambio de color del agente activo).
- [ ] Task: Mejorar los estilos de resaltado en `GraphCanvas` para una transición suave entre nodos.
- [ ] Task: Conductor - User Manual Verification 'Fase 2: Feedback Visual en Tiempo Real' (Protocol in workflow.md)

## Fase 3: Integración del Ciclo de Chat [checkpoint: TBD]
- [ ] Task: Conectar el input del `ChatPanel` con el endpoint de ejecución.
- [ ] Task: Implementar la carga inicial de mensajes y logs desde el backend al abrir la UI.
- [ ] Task: Mostrar la respuesta final del orquestador en la burbuja de chat del asistente.
- [ ] Task: Conductor - User Manual Verification 'Fase 3: Integración del Ciclo de Chat' (Protocol in workflow.md)
