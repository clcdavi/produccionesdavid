#!/usr/bin/env python3
"""
Cliente API para conectar Producciones David con el gestor de tareas Enfoco.
Endpoint: http://137.131.245.249:3000/api/integrations/tasks
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
CONFIG_FILE = BASE_DIR / ".enfoco_config.json"
DEFAULT_ENDPOINT = "http://137.131.245.249:3000/api/integrations/tasks"

def cargar_config() -> dict:
    cfg = {"endpoint": DEFAULT_ENDPOINT, "api_key": os.environ.get("ENFOCO_API_KEY", "")}
    if CONFIG_FILE.exists():
        try:
            stored = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            cfg.update(stored)
        except Exception:
            pass
    return cfg

def guardar_config(cfg: dict) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")

def enviar_tareas(tareas: list, api_key: str = None) -> dict:
    cfg = cargar_config()
    token = (api_key or cfg.get("api_key") or "").strip()
    if not token:
        raise ValueError(
            "Falta configurar la API Key de Enfoco (debe empezar con 'enf_live_'). "
            "Generala en http://137.131.245.249:3000/integrations y guardala."
        )

    endpoint = cfg.get("endpoint", DEFAULT_ENDPOINT)
    payload = {"tasks": tareas}
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "ProduccionesDavid-Sync/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="replace")
        try:
            err_json = json.loads(err_msg)
            return {"error": err_json.get("error", err_msg), "status_code": e.code}
        except Exception:
            return {"error": err_msg, "status_code": e.code}
    except Exception as e:
        return {"error": str(e), "status_code": 500}

def crear_tarea(
    title: str,
    external_id: str = None,
    area: str = "Trabajo",
    project: str = "Producciones David",
    notes: str = "",
    priority: int = 2,
    minutes: int = 30,
    status: str = "todo",
    plan_date: str = None,
    deadline: str = None,
    follow_up: str = None,
    api_key: str = None
) -> dict:
    t = {
        "title": title[:240],
        "area": area if area in ["Trabajo", "Proyectos", "Personal", "Estudio", "Iglesia"] else "Trabajo",
        "project": (project or "Producciones David")[:120],
        "notes": notes,
        "priority": priority if priority in [1, 2, 3] else 2,
        "minutes": max(5, min(1440, minutes)),
        "status": status if status in ["inbox", "todo", "doing", "waiting"] else "todo"
    }
    if external_id:
        t["externalId"] = external_id[:180]
    if plan_date:
        t["planDate"] = plan_date
    if deadline:
        t["deadline"] = deadline
    if follow_up:
        t["followUp"] = follow_up

    return enviar_tareas([t], api_key=api_key)

def pipeline_inicial_producciones_david() -> list:
    hoy = datetime.now().strftime("%Y-%m-%d")
    manana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    en_3_dias = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

    return [
        {
            "externalId": "pd-seguimiento-lanzamiento",
            "title": "Analizar métricas de lanzamiento en Instagram y TikTok",
            "area": "Trabajo",
            "project": "Producciones David",
            "notes": (
                "Revisión de interacción y alcance de los 5 videos públicos subidos hoy:\n"
                "- [ ] Comprobar reproducciones del Reel de Avatares Veo 3.1 en Instagram\n"
                "- [ ] Revisar retención y likes en TikTok Creator Center\n"
                "- [ ] Responder comentarios y mensajes directos solicitando precios de packs"
            ),
            "priority": 3,
            "minutes": 30,
            "status": "todo",
            "planDate": hoy,
            "deadline": manana
        },
        {
            "externalId": "pd-respuestas-md-promos",
            "title": "Armar plantilla de respuesta rápida a consultas de Packs",
            "area": "Trabajo",
            "project": "Producciones David",
            "notes": (
                "Guión para cerrar ventas por DM:\n"
                "- Detalle Pack Impulso Comercial (1 Reel master + versión WhatsApp + 3 historias)\n"
                "- Detalle Pack Presencia Mensual (3 videos comerciales + 9 tomas con avatares IA)\n"
                "- Link a cuenta de cobro / seña para reservar fecha de producción"
            ),
            "priority": 3,
            "minutes": 45,
            "status": "todo",
            "planDate": hoy,
            "deadline": manana
        },
        {
            "externalId": "pd-prospeccion-comercios",
            "title": "Contactar primeros 5 comercios de Zona Norte (Gastronomía / Tiendas)",
            "area": "Trabajo",
            "project": "Producciones David",
            "notes": (
                "Estrategia de prospección con avatar muestra:\n"
                "- [ ] Seleccionar 5 locales gastronómicos o indumentaria de San Fernando/Tigre\n"
                "- [ ] Generar demo gratuita de 10s con IA usando fotos de sus productos\n"
                "- [ ] Enviar por WhatsApp / Instagram con propuesta de valor"
            ),
            "priority": 2,
            "minutes": 60,
            "status": "todo",
            "planDate": manana,
            "deadline": en_3_dias
        },
        {
            "externalId": "pd-catalogo-avatares-veo",
            "title": "Crear catálogo de 3 nuevos estilos de presentadores IA",
            "area": "Proyectos",
            "project": "Producciones David",
            "notes": (
                "Variantes de presentadores virtuales para ampliar cartera de clientes:\n"
                "- Estilo Corporativo / Finanzas / Inmobiliaria\n"
                "- Estilo Dinámico Urbano para Tiendas y Moda\n"
                "- Estilo Gastronómico / Chef / Eventos"
            ),
            "priority": 2,
            "minutes": 90,
            "status": "inbox",
            "planDate": manana,
            "deadline": en_3_dias
        }
    ]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente CLI para Enfoco Tasks")
    parser.add_argument("--set-key", help="Guardar la API Key (enf_live_...) en la configuración local")
    parser.add_argument("--sync-pipeline", action="store_true", help="Cargar el pipeline inicial de tareas de Producciones David")
    parser.add_argument("--title", help="Título de la tarea a crear")
    parser.add_argument("--project", default="Producciones David", help="Nombre del proyecto")
    parser.add_argument("--notes", default="", help="Notas o checklist")
    parser.add_argument("--priority", type=int, default=2, help="Prioridad (1, 2 o 3)")
    parser.add_argument("--status", default="todo", help="Estado (inbox, todo, doing, waiting)")
    args = parser.parse_args()

    if args.set_key:
        cfg = cargar_config()
        cfg["api_key"] = args.set_key.strip()
        guardar_config(cfg)
        print(f"✅ API Key guardada exitosamente en: {CONFIG_FILE}")

    if args.sync_pipeline:
        tareas = pipeline_inicial_producciones_david()
        print(f"📤 Enviando {len(tareas)} tareas a Enfoco...")
        res = enviar_tareas(tareas)
        print("Resultado:", json.dumps(res, indent=2, ensure_ascii=False))

    elif args.title:
        res = crear_tarea(
            title=args.title,
            project=args.project,
            notes=args.notes,
            priority=args.priority,
            status=args.status
        )
        print("Resultado:", json.dumps(res, indent=2, ensure_ascii=False))
