# Pendientes y decisiones abiertas

Estado al 2026-11-22.

## 1. Migración desde la copia original — hecha, falta validar
Hasta hoy el proyecto vivía en `~/.gemini/antigravity/scratch/anuncios-san-fernando` (misma `origin`). Qué se hizo:

- Se copió **todo** a este repo (incluido lo sin commitear): `mcp-enfoco/*`, `mcp-instagram/server.py`, `proyectos_costos.json`, `assets/david/*` nuevos, `campana-cinematica-david/`, un negocio nuevo en `negocios/` y `operacion-despedida-2026/`. **Los datos de clientes y prospectos quedaron solo en local**, ignorados por git.
- Se copiaron también los archivos locales ignorados por git: `instagram_credenciales.json`, `tiktok_credenciales.json`, `claves_ia.json`, `mcp-enfoco/.enfoco_config.json`, la sesión de navegador `mcp-tiktok/tiktok_user_session/` y los renders `.mp4/.mp3` (~1 GB, no se versionan).
- `~/.claude.json` ahora apunta los MCP `instagram-producciones-david`, `tiktok-producciones-david` y `enfoco-tareas` a `mcp-*/server.py` de este repo. Backup: `~/.claude.json.bak-antes-migracion-pd`.
- `mcp-instagram/server.py` y `mcp-tiktok/server.py` calculan su ruta desde `__file__` (ya no hay ruta fija). Los demás scripts de campañas tenían la ruta vieja fija; se reemplazó por la ruta de este repo (siguen siendo absolutas).
- La carpeta `prospectos/` se unificó dentro de `negocios/` (el material aportado era idéntico).

**Falta (requiere reiniciar Claude Code):**
1. Reiniciar y correr `ig_estado_cuenta`, `tiktok_estado_cuenta` y `enfoco_estado` para confirmar que los MCP levantan desde este repo. Las sesiones abiertas antes del cambio siguen usando la copia vieja.
2. Recién después, archivar o borrar la copia original. Se dejó intacta a propósito (incluye los `.bak` que no se copiaron: `mcp-enfoco/*.bak`).

## 2. Duplicados y legado
- `marca-producciones-david/` repite la marca de `assets/branding/producciones-david/` (el logo principal es idéntico byte a byte). Candidata a eliminarse tras confirmar que ningún script la referencia.
- `brand_engine.py` en la raíz es un symlink relativo a `assets/branding/producciones-david/brand_engine.py` (antes estaba roto, con ruta absoluta).
- `campana-lanzamiento-pd/` contiene overlays y escenas intermedias (`v_ov_*`, `veo_overlay_*`, `reel_scene_*`) que probablemente se pueden limpiar.
- `operacion-despedida-2026/` es un proyecto de cliente (solo local, ignorado por git): conviene moverlo a `negocios/` con la convención de `negocios/README.md`. No se movió porque su script usa rutas internas.

## 3. Portabilidad de rutas
Los scripts de `campana-*`, `negocios/*` y `operacion-despedida-2026` usan rutas absolutas a `/Users/davidcorrea/Documents/code_projects/producciones-david`. Funcionan en esta máquina; para otra máquina o carpeta hay que reemplazarlas (idealmente por una constante `RAIZ = Path(__file__).resolve().parents[N]`).

## 4. Dependencias
`requirements.txt` lista solo `mcp`, `Pillow`, `edge-tts`, `requests`. Los scripts también usan FFmpeg, Chromium/Playwright (TikTok y renders) y Node (proyectos HyperFrames de `negocios/*/anuncio/video-anuncio`). El MCP de TikTok corre con el entorno virtual de `adrian-saenz-video-negocio` (`~/Library/Application Support/adrian-saenz-video-negocio/.venv`). Falta documentar versiones exactas.

## 5. Privacidad y tamaño
- El repo pesa ~170 MB versionado (imágenes, fuentes, `reviews.db`, datos crudos de scraping); la carpeta local ~1,1 GB con los renders ignorados.
- **El repo de GitHub es público** (verificado el 2026-11-22). `negocios/*/maps/` de los tres negocios ya publicados incluye reseñas con nombre y foto de personas. Decidir si pasar el repo a privado o quitar esas carpetas del seguimiento (el historial seguiría público).
- Regla vigente: `negocios/*/` y `operacion-despedida-2026/` no se versionan (ver `.gitignore`).
- Evaluar mover `negocios/*/maps/_raw/` y `snapshots/` a `.gitignore` o a almacenamiento aparte.

## 6. Costos
`proyectos_costos.json` registra proveedor, modelo, créditos y USD por generación. Falta una vista resumen por negocio y mes.

**Ojo:** la versión local tiene entradas nuevas con nombres de clientes y quedó **sin commitear a propósito** (el archivo aparece modificado en `git status`). Para versionarlo hay que anonimizar el campo `cliente` o mover el registro a un archivo local ignorado.

## 7. Prospección (nuevo)
La skill `pd-prospecto-video` define el flujo idea → video demo → DM → seguimiento y guarda `negocios/<slug>/prospecto.md`. Falta probarla con un prospecto real y decidir dónde se lleva el estado global (por ejemplo, un tablero en `enfoco-tareas`).
