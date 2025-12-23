# Spec: Synapse Core MVP

## Objetivo
Implementar la infraestructura base del Agentic Control Plane (ACP) para permitir la orquestación multimodal soberana.

## Requisitos Funcionales
- **Pizarra (Blackboard):** Sistema de mensajería asíncrona basado en Redis para el intercambio de datos entre agentes.
- **Orquestador (Corteza):** Lógica de control basada en LangGraph para gestionar flujos de trabajo cíclicos y máquinas de estados.
- **API Core:** Servidor FastAPI para la gestión de nodos y exposición de estados.
- **Agentes Iniciales:**
    - **Agente de Visión:** Integración con Ollama para procesar descripciones de imágenes.
    - **Agente Guardián:** Validador lógico que asegura la consistencia de los datos en la pizarra.

## Requisitos No Funcionales
- **Local-first:** Todo el procesamiento debe ser local en Fedora.
- **Baja Latencia:** Comunicación entre agentes < 50ms.
- **Validación de Datos:** Uso estricto de Pydantic.

## Arquitectura
- **Backend:** Python 3.12 + FastAPI.
- **Estado:** Redis.
- **Orquestación:** LangGraph.
- **Inferencia:** Ollama.
