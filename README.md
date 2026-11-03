# 🎬 Producciones David — Sistema Integral de Producción y Publicación IA

Plataforma integral de creación, postproducción y distribución automatizada de contenidos publicitarios impulsados por Inteligencia Artificial para **Producciones David** ([@produccionesdavid.ar](https://www.instagram.com/produccionesdavid.ar/)).

---

## 🌟 Estructura del Ecosistema

```
anuncios-san-fernando/
├── marca-producciones-david/      # Identidad visual oficial, logos vectoriales y avatar 1024x1024
├── campana-lanzamiento-pd/        # Scripts de generación de campañas, carruseles y Reels
├── mcp-instagram/                 # Servidor MCP para gestión y publicación automática en Instagram
├── mcp-tiktok/                    # Servidor MCP y automatización de publicación en TikTok
├── negocios/sw-store/             # Campaña comercial de muestra y recursos audiovisuales
└── proyectos_costos.json          # Control de costos exacto por generación y render
```

---

## 🚀 1. Identidad Visual Corporativa Oficial (`assets/branding/producciones-david`)

La marca se rige por su **Manual Oficial de Identidad Visual**:
- **Logotipo:** Construcción geométrica en **Montserrat Black** (`DAVID`) con corte diagonal terracota característico en la letra V, acompañado de `PRODUCCIONES` en espaciado amplio superior y bajada institucional: *"Videos profesionales con IA para empresas e instituciones"*.
- **Paleta Cromática Oficial:**
  - **Carbón (`#191919`):** Fondos oscuros, tipografía principal y placas cinematográficas.
  - **Marfil (`#F5F2EC`):** Fondos claros editoriales, contraste y aplicaciones institucionales.
  - **Terracota (`#CD563C`):** Detalle distintivo en la V, cortes diagonales de esquinas y líneas de acento.
- **Suite de Recursos Vectoriales y Master 4K:**
  - `logo-principal.svg` / `.png`: Isologotipo completo con bajada y filetes terracota.
  - `logo-horizontal.svg` / `.png`: Versión limpia horizontal.
  - `logo-inverso.svg` / `.png`: Placa corporativa sobre fondo carbón.
  - `isotipo.svg` / `isotipo-perfil.png`: Avatar circular 2048x2048 con el corte terracota sobre la letra D (para Instagram, TikTok y WhatsApp).
  - `isotipo-squircle.svg` / `isotipo-squircle.png`: Isotipo squircle (para App Icons y web).
  - `watermark-blanco.png` y `watermark-oscuro.png`: Marcas de agua transparentes calibradas.
  - `outro-logo.mp4` (9:16) y `outro-logo-16x9.mp4` (16:9): Cierres audiovisuales de 2.0s con audio estéreo AAC silencioso.
- **Brand Identity Engine (`brand_engine.py`):**
  - Distinción automática: Contenido propio (aplica marca) vs. Contenido de cliente (100% limpio).
  - Inyección de marca de agua con respeto estricto de zonas seguras en Reels/TikTok.
  - Generador de plantillas: Portadas de Reel 9:16 (*Detrás de Cámaras*), Post Cuadrado 1:1 (*Producción Audiovisual*) e Historias 9:16 (*Nuevo Proyecto*).

---

## 📸 2. Automatización Instagram MCP (`mcp-instagram`)
Servidor MCP basado en FastMCP conectado con la **Meta Graph API (v26.0)** mediante System User Access Token permanente (`SUAT`).
- **Herramientas disponibles:**
  - `ig_estado_cuenta`: Diagnóstico de cuenta comercial y métricas.
  - `ig_publicar_reel`: Publicación de videos 9:16 con `share_to_feed: true`.
  - `ig_publicar_carrusel`: Publicación de álbumes de hasta 10 placas (4:5).
  - `ig_publicar_historia`: Publicación en Historias de 24 hs.
  - `ig_responder_comentario`: Interacción automatizada con prospectos.

---

## 🎵 3. Automatización TikTok MCP (`mcp-tiktok`)
Servidor MCP para gestión y distribución en TikTok:
- **Herramientas disponibles:**
  - `tiktok_preparar_subida_web`: Formateo de videos verticales con copetes, hashtags y metadatos AIGC listos para el Creator Center.
  - `tiktok_publicar_video_api`: Integración con la Content Posting API oficial (`open.tiktokapis.com/v2`).
  - `tiktok_estado_cuenta`: Verificación de tokens y métricas de perfil.

---

## 🎭 4. Motor de Video y Avatares IA (`campana-lanzamiento-pd`)
Pipeline de generación con los modelos más avanzados de la industria:
- **Veo 3.1 (Google DeepMind):** Generación de video con voz humana nativa y lip-sync sincronizado en español rioplatense (sin locutores sintéticos externos).
- **Control de Zona Segura:** Subtítulos renderizados con Chromium headless a más de 390px de la base para evitar solapamientos con la interfaz de Instagram y TikTok.
- **Kling 3.0 / Recraft / Gemini Imagen:** Modelos auxiliares para placas de alta definición y motion graphics.

---

## 🛠️ Requisitos e Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/clcdavi/produccionesdavid.git
   cd produccionesdavid
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar credenciales en archivos locales ignorados (`instagram_credenciales.json` y `tiktok_credenciales.json`).

---

© 2026 Producciones David — Todos los derechos reservados.
