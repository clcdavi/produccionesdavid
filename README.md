# 🎬 Producciones David

Sistema de producción, postproducción y publicación de contenido con IA para **Producciones David** ([@produccionesdavid.ar](https://www.instagram.com/produccionesdavid.ar/)): videos profesionales con IA para empresas e instituciones.

Este repo reúne cuatro cosas: la **marca**, el **código de producción y publicación**, los **negocios** atendidos (clientes y prospectos) y las **skills de Claude Code** que guían el trabajo de contenido y ventas.

> Instrucciones para Claude Code: `CLAUDE.md`. Pendientes y decisiones abiertas: [`docs/pendientes.md`](docs/pendientes.md).

---

## 🗂️ Estructura

```
producciones-david/
├── assets/
│   ├── branding/producciones-david/   # FUENTE OFICIAL de la marca (logos, tipografías, plantillas, brand_engine.py, outros)
│   └── david/                         # Fotos de referencia de David para avatares
├── negocios/<slug>/                   # Un negocio por carpeta (cliente o prospecto). Ver negocios/README.md
├── contenido/{reels,carruseles,historias}/   # Piezas propias nuevas
├── planificacion/                     # Planes semanales y bancos de ideas
├── campana-lanzamiento-pd/            # Campaña de lanzamiento de la agencia (scripts + piezas)
├── campana-publicitaria-nueva-marca/  # Campaña con la nueva identidad (carrusel, historias, reel, copetes)
├── scripts/                           # Pipelines de video: Seedance multiescena, voces, ensamblado, búsqueda de hooks
├── animaciones-programaticas/         # Motion graphics HTML renderizados a MP4
├── mcp-instagram/  mcp-tiktok/  mcp-enfoco/   # Servidores MCP
├── .claude/skills/pd-*/               # Skills del proyecto
├── docs/                              # Documentación (pendientes, decisiones)
├── brand_engine.py                    # Symlink a assets/branding/producciones-david/brand_engine.py
├── proyectos_costos.json              # Costo por generación y render (tasa ARS/USD)
├── requirements.txt
└── marca-producciones-david/          # LEGADO duplicado de la marca (usar assets/branding)
```

---

## 📦 Qué se versiona y qué es local

Este repo (público) contiene **solo**: documentación (`README.md`, `CLAUDE.md`, `docs/`), skills de Claude Code (`.claude/skills/`) y el código de los MCP (`mcp-*`), más `requirements.txt` y `negocios/README.md`.

Todo lo demás del árbol de arriba (marca, campañas, scripts, animaciones, `negocios/<slug>/`, renders, `proyectos_costos.json`) existe **solo en la máquina local** y está excluido por `.gitignore`. Ningún dato de clientes, prospectos ni producción de cliente se sube. Para versionar algo nuevo hay que habilitarlo explícitamente en `.gitignore` (lista blanca).

---

## 🧭 Flujo de trabajo

```
Idea / prospecto ──► Diagnóstico ──► Guion ──► Producción ──► Aprobación de David ──► Publicación
 (pd-banco-ideas,   (maps, IG,      (pd-reel-   (adrian-saenz-    (siempre en el chat)   (MCP Instagram /
  pd-prospecto-      dossier)        guion,      video-negocio,                           TikTok)
  video)                             pd-stories) motion-graphics)
```

**Para un cliente:** `negocios/<slug>/` → ideas → guion → video/carrusel/historia → copete → aprobación → publicación → `pd-auditar-pieza`.

**Para vender (prospecto → video demo):** ver `pd-prospecto-video`. Una idea marcada 🎯 en un banco de ideas (algo que un negocio está buscando o sufriendo) se convierte en un video demo hecho con **su** negocio, un mensaje de apertura y dos seguimientos. David envía el DM; nada sale sin su OK.

---

## 🧰 Skills del proyecto (`.claude/skills/pd-*`)

| Skill | Para qué |
|---|---|
| `pd-reel-guion` | Guiones de Reel: 15/30/60 s, hablando, b-roll, tutorial, historia, venta |
| `pd-stories` | Secuencias de Stories: venta, bastidores, encuesta, pregunta, caso, objeción, autoridad |
| `pd-dm-ventas` | DM y respuestas de venta: primer contacto, precio, objeciones, "lo pienso", seguimiento, cierre |
| `pd-oferta-precios` | Oferta, paquetes, anclaje, garantía, objeción de precio, rentabilidad |
| `pd-auditar-pieza` | Auditoría y diagnóstico de piezas antes o después de publicar |
| `pd-banco-ideas` | Bancos de ideas por cliente; marca con 🎯 las que sirven para captar prospectos |
| `pd-cta` | Llamadas a la acción por objetivo |
| `pd-prospecto-video` | Prospecto → video demo → mensaje → seguimiento |

Complementan a las skills globales `ig-*` (captions, carruseles, hashtags, plan semanal, perfil, humanizer, repurposer), `motion-graphics-engine` y `adrian-saenz-video-negocio`. Reglas comunes: voseo rioplatense, no inventar datos, confirmar antes de publicar.

---

## 🎨 Identidad visual (`assets/branding/producciones-david`)

- **Logotipo:** **Montserrat Black** (`DAVID`) con corte diagonal terracota en la V, `PRODUCCIONES` en espaciado amplio y bajada *"Videos profesionales con IA para empresas e instituciones"*.
- **Paleta:** Carbón `#191919` (fondos oscuros, tipografía), Marfil `#F5F2EC` (fondos claros), Terracota `#CD563C` (detalle, cortes, acentos).
- **Recursos:** `logo-principal`, `logo-horizontal`, `logo-inverso`, `isotipo` (avatar 2048×2048), `isotipo-squircle` (app icon), `watermark-blanco/oscuro` (SVG + PNG 4K), `outro-logo.mp4` (9:16) y `outro-logo-16x9.mp4`, plantillas de historia, portada de Reel y post cuadrado.
- **Brand Identity Engine (`brand_engine.py`):** distingue contenido propio (aplica marca) de contenido de cliente (100 % limpio); inyecta marca de agua respetando zonas seguras de Reels/TikTok; concatena el outro; genera plantillas y valida formato (dimensiones, codec, bitrate).

---

## 📸 MCP Instagram (`mcp-instagram`)

FastMCP sobre la **Meta Graph API** con System User Access Token. Herramientas:
`ig_estado_cuenta`, `ig_configurar_credenciales`, `ig_listar_publicaciones`, `ig_espiar_cliente` (lectura de perfiles), `ig_publicar_reel`, `ig_publicar_foto`, `ig_publicar_carrusel`, `ig_publicar_historia`, `ig_responder_comentario`.
Los Reels suben directo a Meta por carga resumible (sin hosting público intermedio).

## 🎵 MCP TikTok (`mcp-tiktok`)

`tiktok_estado_cuenta`, `tiktok_preparar_subida_web` (copete, hashtags y metadatos AIGC listos para Creator Center) y `tiktok_publicar_video` (Content Posting API). Incluye uploader web con Playwright como alternativa.

## ✅ MCP Enfoco (`mcp-enfoco`)

Cliente y servidor de tareas (`enfoco-tareas`) para llevar el pipeline de la agencia.

> Los MCP de Claude Code apuntan a `mcp-*/server.py` de este repo (migrado el 2026-11-22 desde `~/.gemini/antigravity/scratch/anuncios-san-fernando`). Hay que reiniciar Claude Code y validar los tres; ver `docs/pendientes.md`.

---

## 🎭 Motor de video y avatares

- **Veo 3.1** (`campana-lanzamiento-pd/generar_reel_veo31.py`): video con voz y lip-sync en español rioplatense.
- **Seedance multiescena + voz clonada** (`scripts/generar_video_seedance_multiescenario.py`, `generar_voces_multiescenario.py`, `ensamblar_reel_multiescenario.py`): avatares con varios looks.
- **Kling 3.0** (`lanzar_kling.py`, dentro de la carpeta del negocio): planos de producto; los costos quedan en `proyectos_costos.json`.
- **HyperFrames + GSAP** (`negocios/*/anuncio/video-anuncio/`): anuncios de negocio diseñados y renderizados desde HTML.
- **Zona segura:** subtítulos a más de 390 px de la base para no chocar con la interfaz de Instagram/TikTok.
- **Hooks:** `scripts/buscar_hook.py` consulta la base de 1000 hooks virales.

---

## 🛠️ Instalación

```bash
git clone https://github.com/clcdavi/produccionesdavid.git
cd produccionesdavid
pip install -r requirements.txt
```

Además se necesitan FFmpeg, Chromium/Playwright y Node (para los proyectos HyperFrames).

**Credenciales:** viven en archivos locales ignorados por git, nunca en el repo: `instagram_credenciales.json`, `tiktok_credenciales.json`, `claves_ia.json`, `.enfoco_config.json`, `.env`. Ver `.gitignore`.

---

© 2026 Producciones David — Todos los derechos reservados.
