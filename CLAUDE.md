# Producciones David

Agencia de contenido y video con IA para negocios e instituciones ([@produccionesdavid.ar](https://www.instagram.com/produccionesdavid.ar/)). Este repo concentra marca, código de producción y publicación, negocios atendidos y planificación de contenido. Documentación completa en `README.md`; pendientes en `docs/pendientes.md`.

## Estructura
- `assets/branding/producciones-david/`: **fuente oficial de la marca** (logos, isotipos, Montserrat, plantillas, `brand_engine.py`, outros). `brand_engine.py` en la raíz es un symlink a ese archivo.
- `negocios/<slug>/`: **una carpeta por negocio** (cliente o prospecto). Convención en `negocios/README.md`.
- `contenido/reels|carruseles|historias/`: piezas propias nuevas por formato.
- `planificacion/`: planes semanales y bancos de ideas.
- `campana-lanzamiento-pd/`, `campana-publicitaria-nueva-marca/`: campañas históricas de la propia agencia (con sus scripts). No mover: los scripts usan rutas relativas.
- `scripts/`, `animaciones-programaticas/`: pipelines de video (Seedance, voces, ensamblado, motion graphics).
- `mcp-instagram/`, `mcp-tiktok/`, `mcp-enfoco/`: código de los servidores MCP.
- `assets/david/`: fotos de referencia de David para avatares.
- `proyectos_costos.json`: costo por generación y render (tasa ARS/USD).
- `marca-producciones-david/`: **legado duplicado** de la marca; usar `assets/branding/`.

## Marca
- Paleta: Carbón `#191919`, Marfil `#F5F2EC`, Terracota `#CD563C`. Tipografía: Montserrat.
- Tono comercial argentino, español rioplatense (voseo). Horarios en GMT-3.
- Contenido propio lleva la marca; contenido de cliente va 100 % limpio (lo resuelve `brand_engine.py`).

## Herramientas (disponibles en Claude Code)
- MCP: `instagram-producciones-david`, `tiktok-producciones-david`, `enfoco-tareas`, `stitch`.
- Skills globales: `ig-*` (captions, carruseles, hashtags, plan semanal, perfil, humanizer, repurposer), `motion-graphics-engine`, `adrian-saenz-video-negocio`.
- Skills del proyecto (`.claude/skills/pd-*`): `pd-reel-guion`, `pd-stories`, `pd-dm-ventas`, `pd-oferta-precios`, `pd-auditar-pieza`, `pd-banco-ideas`, `pd-cta`, `pd-prospecto-video` (idea de prospecto → video demo para vender).

## Reglas
- Confirmar con el usuario antes de publicar en Instagram o TikTok.
- Nada se envía por DM en nombre de David: se redacta y él lo manda.
- No inventar precios, reseñas, cifras ni resultados de clientes o prospectos.
- No versionar credenciales: viven en archivos locales ignorados por git (`*credenciales*.json`, `claves_*.json`, `.env`) o variables de entorno.
