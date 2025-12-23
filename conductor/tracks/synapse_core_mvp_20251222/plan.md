# Plan: Synapse Core MVP

## Fase 1: Infraestructura Base [checkpoint: 25c77fc]
- [x] Task: Configurar entorno de desarrollo con Podman y Redis local. [db9e80e]
- [x] Task: Implementar cliente de Pizarra (Blackboard) sobre Redis. [02f673e]
- [x] Task: Definir esquemas de datos base con Pydantic. [14b00e2]
- [x] Task: Conductor - User Manual Verification 'Fase 1: Infraestructura Base' (Protocol in workflow.md) [25c77fc]

## Fase 2: Orquestador y API
- [ ] Task: Implementar servidor FastAPI básico.
- [ ] Task: Configurar motor de orquestación con LangGraph.
- [ ] Task: Crear nodo de integración para Ollama.
- [ ] Task: Conductor - User Manual Verification 'Fase 2: Orquestador y API' (Protocol in workflow.md)

## Fase 3: Integración Multimodal y Guardianes
- [ ] Task: Desarrollar el Agente de Visión (Wrapper de Ollama).
- [ ] Task: Desarrollar el Agente Guardián (Lógica de validación).
- [ ] Task: Implementar flujo de feedback Visión -> Pizarra -> Guardián.
- [ ] Task: Conductor - User Manual Verification 'Fase 3: Integración Multimodal y Guardianes' (Protocol in workflow.md)
