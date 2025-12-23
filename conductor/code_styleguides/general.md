# Guía General: Arquitectura, Despliegue y Ética (Synapse)

Esta guía representa la Homeostasis Global de Synapse. Aquí definimos cómo los "hemisferios" (Backend y Frontend) se comunican, cómo protegemos el sistema (Despliegue) y cómo aseguramos que nuestra IA actúe con principios humanos (Ética).

## 1. Integración Sistémica (El Eje Cerebro-Espinal)
La comunicación entre el Backend (FastAPI/LangGraph) y el Frontend (React) debe ser bidireccional y coordinada, similar al flujo de información entre la periferia y el centro.

- **API First:** El backend es el único punto de verdad. El frontend solo interpreta los datos y los presenta.
- **Flujos de Feedback:** Implementamos bucles de feedforward (predicción de la intención del usuario) y feedback (corrección del agente basada en la respuesta del usuario).
- **Contratos de Datos:** La Pizarra es el lenguaje común. Si el backend cambia un campo en Pydantic, TypeScript debe reflejarlo de inmediato para evitar una "desconexión sináptica".

## 2. Control de Versiones: Git (Herencia y Evolución)
En biología, la evolución ocurre mediante cambios en el código genético que se preservan. En Synapse, Git es nuestra memoria evolutiva.

- **Commits Atómicos:** Cada cambio debe ser pequeño y funcional, como una mutación puntual.
- **Branches (Ramas):**
    - `main`: El genoma estable (producción).
    - `develop`: El laboratorio de neurogénesis (desarrollo).
    - `feature/*`: Nuevas habilidades o "sentidos" para los agentes.
- **Workflow en Fedora:** Aprovecha el poder de la terminal de Fedora para gestionar tus repositorios con comandos claros y scripts de automatización.

## 3. Despliegue con Podman: Aislamiento Celular
Para garantizar la Soberanía de Datos y la seguridad, utilizaremos Podman en tu entorno de Fedora.

- **Contenedores = Células:** Cada servicio (Redis, FastAPI, React, Ollama) vive en su propio contenedor. Si una "célula" falla, la membrana (Podman) evita que el error se propague al resto del "tejido" (sistema operativo).
- **Local-First:** Priorizamos el despliegue en servidores locales o nubes privadas. Esto es como el sistema inmunológico: protege la información sensible del paciente o de la empresa de agentes externos (nubes públicas no seguras).
- **Orquestación:** Usaremos `podman-compose` para levantar todo el sistema con un solo comando.

## 4. Ética y Gobernanza (La Corteza Prefrontal)
La IA sin ética es como un sistema motor sin inhibición: peligrosa y descontrolada.

- **Human-in-the-loop (HITL):** El sistema nunca toma decisiones críticas solo. Siempre hay un "nodo de validación humana", especialmente en decisiones que afectan la salud o la legalidad de una persona.
- **Transparencia (Explicabilidad):** Debemos ser capaces de explicar por qué un agente tomó una decisión. Es el equivalente clínico al razonamiento diagnóstico.
- **Privacidad por Diseño:** Aplicamos la Ley 1581 (Habeas Data) desde la arquitectura. La anonimización de datos no es una opción, es un requisito funcional.

## 5. Principios de Mantenimiento (Homeostasis)
- **Monitoreo:** Observa el uso de GPU y RAM en Fedora para evitar el "estrés metabólico" del hardware.
- **Refactorización:** Limpia el código muerto. Un sistema con exceso de tejido innecesario se vuelve lento e ineficiente.
- **Documentación Continua:** El código es el cuerpo; la documentación es la historia clínica. No puede existir uno sin el otro.