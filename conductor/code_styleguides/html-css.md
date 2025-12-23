# Guía de Diseño: Estética y Estructura (Synapse)

Esta guía define los estándares visuales para la interfaz de Synapse. Buscamos una estética de "Centro de Control" que sea funcional, sofisticada y que refleje la precisión de un entorno científico-tecnológico.

## 1. El Sistema Tegumentario (Diseño Atómico)

Nuestra "piel" digital debe ser resistente pero sensible. Utilizaremos **Tailwind CSS** para garantizar que el diseño sea coherente en todos los dispositivos (responsive).

- **Dark Mode por Defecto:** Para reducir la fatiga visual del clínico o investigador. Usaremos una paleta de grises profundos y azules medianoche (`slate-900`, `zinc-950`).

### Tokens de Diseño:
- **Fondo Principal:** `bg-slate-950`
- **Contenedores (Fascia):** `bg-slate-900/50` con bordes `border-slate-800`.
- **Acentos (Sinapsis):** `blue-500` para acciones primarias, `emerald-500` para estados saludables, y `rose-500` para alertas (dolor/error).

## 2. Glassmorphism: El Espacio Sináptico

Para dar profundidad multidimensional a la interfaz, aplicaremos efectos de "cristal" (glassmorphism). Esto permite al usuario percibir capas de información, similar a cómo percibimos la profundidad en los tejidos corporales.

```html
<!-- Ejemplo de contenedor con efecto de profundidad -->
<div class="bg-slate-900/40 backdrop-blur-md border border-white/10 rounded-2xl p-6 shadow-xl">
  <h3 class="text-slate-100 font-semibold">Estado del Agente</h3>
  <p class="text-slate-400 text-sm">Procesando señales sensoriales...</p>
</div>
```

## 3. Layout: Organización Somatotópica

Al igual que la corteza somatosensorial tiene un mapa del cuerpo, nuestra interfaz debe tener una jerarquía clara:

- **Sidebar (El Tronco Encefálico):** Control de navegación y estados vitales del sistema.
- **Header (El Sistema Reticular):** Alertas rápidas, búsqueda y perfil de usuario.
- **Main Area (La Corteza):** Donde ocurre el procesamiento real (la Pizarra y los Grafos de agentes).
- **Panel de Detalles (Receptores):** Información profunda de cada agente seleccionado.

## 4. Tipografía: Legibilidad Científica

La información en Synapse debe ser legible bajo cualquier condición de estrés operativo.

- **Fuente Principal:** San Serif (Inter o Geist). Refleja modernidad y limpieza.
- **Fuente Monoespaciada:** Para logs de agentes y datos técnicos (JetBrains Mono o Fira Code). Muy apreciada por usuarios de Fedora.

### Escala Visual:
- `text-xs`: Para metadatos y logs (densidad de información).
- `text-base`: Para contenido principal.
- `text-xl/2xl`: Solo para títulos de sección o métricas críticas (ROAI).

## 5. Micro-interacciones (Reflejos Visuales)

La interfaz debe reaccionar a la intención del usuario.

- **Hover States:** Cambios sutiles de opacidad o brillo.
- **Transiciones:** Usa `transition-all duration-300 ease-in-out` para que el movimiento de los componentes se sienta orgánico, no mecánico.
- **Loading States:** Esqueletos de carga (`animate-pulse`) para mantener la calma del usuario mientras los agentes "piensan".

## 6. Accesibilidad (Vías Aferentes)

No olvides que la multidimensionalidad incluye la diversidad funcional:

- **Contraste Elevado:** Asegura que el texto sobre fondos oscuros supere el ratio de 4.5:1.
- **Focus States:** El "foco" del teclado debe ser claramente visible (`ring-2 ring-blue-500`).
- **Semántica HTML:** Usa `<main>`, `<nav>`, `<aside>` y `<article>`. Un HTML bien estructurado es como un esqueleto bien alineado: todo lo demás funciona mejor.

> "El diseño no es lo que se ve, es cómo funciona la conexión entre el usuario y el sistema. Una interfaz limpia reduce la carga cognitiva, permitiendo que la inteligencia del usuario y la de la IA se sincronicen sin fricción."
