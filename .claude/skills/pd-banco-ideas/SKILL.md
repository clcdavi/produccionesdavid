---
name: pd-banco-ideas
description: Genera bancos de ideas de contenido para un cliente de Producciones David (10 o 50 ideas, por dolores, deseos, errores, preguntas frecuentes, números, opiniones, guardables) y marca cuáles pueden usarse para captar prospectos. Usala cuando David pida ideas, un banco de ideas o "qué contenido hacemos para X".
---

# Banco de ideas

## Reglas fijas
- Voseo rioplatense. Leé `clientes/<cliente>/` y `marca/` si existen. Sin datos del rubro o del cliente ideal, preguntá antes de generar.
- **No inventes** estadísticas ni casos. Si una idea necesita un dato, marcala `[dato a confirmar]`.
- Ideas distintas entre sí: cero variaciones superficiales del mismo tema.

## Modos
`ideas` (5-10), `10ideas`, `50ideas` (organizadas por dolor, deseo y nivel de consciencia), `viral`, `principiantes`, `errores`, `preguntas` (de preguntas frecuentes), `numeros`, `controversia` (opinión defendible), `guardar` (utilidad para guardar).

## Salida
Tabla con: `# | Idea | Formato (Reel/carrusel/historia) | Gancho de ejemplo | Objetivo (alcance/guardados/consulta/venta) | Etapa (descubre/compara/decide)`.

Al final, mezcla sugerida de la semana (alcance + autoridad + prueba social + venta) y enlazá con `ig-content-planner` para ubicarlas en el plan semanal.

## Ideas que sirven para vender la agencia
Marcá con 🎯 las ideas que responden a **algo que un negocio prospecto está buscando o sufriendo** (por ejemplo: "no sé qué publicar", "me sale caro un video", "me siguen pero no consultan"). Para cada 🎯 agregá:
- Qué negocio concreto (rubro, zona) tendría ese dolor.
- Un ángulo de video corto para mostrarle que lo entendemos.

Las 🎯 pasan a `pd-prospecto-video` para convertirlas en un video demo dirigido a un prospecto real.

Guardá en `planificacion/ideas-<cliente>-<fecha>.md`.
