# Guía de Desarrollo: Backend Python (Synapse)

Esta guía define los estándares para mantener el "SNC" de nuestra aplicación limpio, eficiente y homeostático. Al programar en Fedora, aprovecharemos el tipado fuerte y la validación rigurosa para evitar fallos sinápticos en producción.

## 1. Pydantic: La Homeostasis de Datos
En fisiología, la homeostasis mantiene las variables internas dentro de límites precisos. En Synapse, Pydantic es nuestro mecanismo homeostático. Si un dato no cumple con la estructura, el sistema lo rechaza antes de que cause una patología en el flujo.

- **Modelos Estrictos:** Usa `BaseModel` para definir cada entrada y salida de los agentes.
- **Valida Receptores:** Si el dato (ligando) no encaja perfectamente en el modelo (receptor), la función no se dispara.

```python
from pydantic import BaseModel, Field, field_validator

class ClinicalData(BaseModel):
    patient_id: str = Field(..., pattern=r"^PT-\d{4}-[A-Z]$")
    heart_rate: int = Field(..., gt=30, lt=220) # Límites fisiológicos
    
    @field_validator('heart_rate')
    @classmethod
    def validate_rhythm(cls, v: int) -> int:
        # Ejemplo de validación lógica compleja
        return v
```

## 2. FastAPI: Conducción Nerviosa Ultrarrápida
Nuestros endpoints deben responder con la latencia de una fibra nerviosa tipo A-alfa (120 m/s).

- **Asincronía (async/await):** Todo el IO (llamadas a Ollama, consultas a Redis) debe ser asíncrono para no bloquear el hilo principal.
- **Inyección de Dependencias:** Usa las dependencias de FastAPI para gestionar la base de datos y la autenticación, similar a cómo el sistema endocrino provee hormonas solo cuando se necesitan.

## 3. LangGraph: Circuitos de Retroalimentación
LangGraph no es una secuencia lineal; es un sistema de control motor con bucles de retroalimentación (Feedback Loops).

- **Nodos = Núcleos Neuronales:** Cada nodo realiza una tarea específica (Análisis, Validación, Guardián).
- **Aristas (Edges) = Axones:** Conectan los nodos. Usa aristas condicionales para decidir si el proceso continúa o vuelve atrás para corregirse (como un ajuste del cerebelo ante un error de marcha).

## 4. Estilo y Calidad (PEP 8 y Fedora)
Para que nuestro "tejido" de código sea sano:

- **Tipado Estricto:** Usa `typing` (`List`, `Dict`, `Optional`, `Annotated`) en todas las funciones. El código sin tipos es como un músculo denervado: pierde su función.
- **Entorno en Fedora:**
    - Usa siempre `python -m venv .venv` para aislar el proyecto.
    - Gestiona dependencias con `pip-tools` o `poetry`.
- **Documentación (Docstrings):** Explica el "porqué" de la lógica, no solo el "qué". Un código bien documentado es como un atlas de anatomía claro.

## 5. El "Arco Reflejo" del Desarrollador (Workflow)
1. **Definir el Esquema (Pizarra):** ¿Qué datos compartiremos?
2. **Escribir el Test:** ¿Cómo sabemos que el agente no está "alucinando"?
3. **Implementar el Nodo:** Código limpio y modular.
4. **Validación del Guardián:** Asegurar que el output cumple con la ética y la ley.

> "Un código limpio es la base de un sistema nervioso digital saludable. Sin estructura, la inteligencia es solo ruido."
