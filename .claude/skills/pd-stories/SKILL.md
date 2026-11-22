---
name: pd-stories
description: Diseña secuencias de Stories de Instagram para clientes de Producciones David (venta, bastidores, encuesta, caja de preguntas, caso de cliente, objeción, autoridad). Usala cuando David pida stories, historias o una secuencia de 3 a 7 placas.
---

# Secuencias de Stories

## Reglas fijas
- Voseo rioplatense. Marca: Marfil, Carbón, Terracota, Montserrat. Formato 9:16.
- Leé `clientes/<cliente>/` si existe. **No inventes** datos, testimonios ni resultados; si falta algo, preguntá.
- Nada se publica sin confirmación de David (las historias se publican con `ig_publicar_historia` solo tras aprobación).

## Tipos
| Tipo | Objetivo | Estructura típica |
|---|---|---|
| `venta` | deseo + consulta | problema → producto en acción → prueba → oferta → CTA |
| `bastidores` | confianza y autoridad | cómo se hace, proceso real, detalle que nadie ve |
| `encuesta` | interacción | pregunta de dolor + 2 opciones + respuesta a los 2 lados |
| `pregunta` | descubrir necesidades | caja de preguntas con consigna que invite a contar un problema |
| `caso` | prueba social | situación → qué se hizo → resultado real |
| `objecion` | derribar freno | "me dicen que…" → verdad → ejemplo → CTA |
| `autoridad` | experiencia sin presumir | trabajo, proceso o aprendizaje concreto |

## Salida
Por cada placa: `N° | Imagen o video | Texto en pantalla (máx. 12 palabras) | Sticker (encuesta, pregunta, link, cuenta regresiva) | Duración`.
Cerrá siempre con **una** CTA (ver `pd-cta` para variantes). Por defecto 5 placas; ajustá si piden otra cantidad.

## Criterios
- Cada placa se entiende sola y empuja a ver la siguiente.
- Texto grande, contraste alto sobre Marfil/Carbón, acento Terracota.
- Evitá más de un sticker por placa.
- En `encuesta` y `pregunta`, planificá cómo se usan las respuestas (de ahí salen ideas para Reels, ver `pd-banco-ideas`).

Guardá en `contenido/historias/<cliente>-<tema>.md`.
