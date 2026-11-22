# Pendientes y decisiones abiertas

Estado al 2026-11-22, tras unir el repo con el historial de `origin/main`.

## 1. Dos copias del proyecto en la máquina
| Copia | Ruta | Rol |
|---|---|---|
| Repo de trabajo (este) | `~/Documents/code_projects/producciones-david` | estructura organizada, skills `pd-*`, documentación |
| Copia original | `~/.gemini/antigravity/scratch/anuncios-san-fernando` | **donde hoy corren los MCP** y están las credenciales |

La copia original tiene cambios sin commitear que **no están en el repo**: `mcp-enfoco/*`, `mcp-instagram/server.py`, `proyectos_costos.json`, `assets/david/*` nuevos, y carpetas sin versionar (`campana-cinematica-david/`, `operacion-despedida-2026/`, `prospectos/`).

**Para migrar sin perder nada:**
1. Commitear esos cambios en la copia original (sin los `*credenciales*.json` ni `claves_ia.json`, que ya están en `.gitignore`).
2. Traerlos a este repo (`git pull`).
3. Reapuntar los MCP de `~/.claude.json` (`instagram-producciones-david`, `tiktok-producciones-david`, `enfoco-tareas`) a `mcp-*/server.py` de este repo y copiar los archivos de credenciales locales.
4. Probar `ig_estado_cuenta` y `tiktok_estado_cuenta` antes de borrar la copia vieja.

Hasta entonces, **no editar los servidores MCP en este repo esperando que cambie su comportamiento**: los que corren son los de la copia original.

## 2. Duplicados y legado
- `marca-producciones-david/` repite la marca de `assets/branding/producciones-david/` (el logo principal es idéntico byte a byte). Candidata a eliminarse tras confirmar que ningún script la referencia.
- `brand_engine.py` en la raíz era un symlink roto con ruta absoluta de la copia original; ahora apunta en relativo a `assets/branding/producciones-david/brand_engine.py`.
- `campana-lanzamiento-pd/` contiene overlays y escenas intermedias (`v_ov_*`, `veo_overlay_*`, `reel_scene_*`) que probablemente se pueden limpiar.

## 3. Dependencias
`requirements.txt` lista solo `mcp`, `Pillow`, `edge-tts`, `requests`. Los scripts también usan FFmpeg, Chromium/Playwright (TikTok y renders) y Node (proyectos HyperFrames de `negocios/*/anuncio/video-anuncio`). Falta documentar versiones exactas.

## 4. Privacidad y tamaño
- El repo pesa ~120 MB comprimido (imágenes, fuentes, `reviews.db`, datos crudos de scraping).
- `negocios/*/maps/` incluye reseñas con nombre y foto de personas. Confirmar si el repo es privado en GitHub antes de compartirlo.
- Evaluar mover `negocios/*/maps/_raw/` y `snapshots/` a `.gitignore` o a almacenamiento aparte.

## 5. Costos
`proyectos_costos.json` registra proveedor, modelo, créditos y USD por generación. Falta una vista resumen por negocio y mes.

## 6. Prospección (nuevo)
La skill `pd-prospecto-video` define el flujo idea → video demo → DM → seguimiento y guarda `negocios/<slug>/prospecto.md`. Falta probarla con un prospecto real y decidir dónde se lleva el estado global (por ejemplo, un tablero en `enfoco-tareas`).
