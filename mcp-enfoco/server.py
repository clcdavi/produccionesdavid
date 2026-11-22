#!/usr/bin/env python3
"""
Servidor MCP para el sistema de gestión de tareas Enfoco (Stdio JSON-RPC 2.0).
Permite crear pendientes, sincronizar tareas de video y organizar la agencia.
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

# Añadir directorio local para importar enfoco_client
sys.path.insert(0, str(Path(__file__).parent.resolve()))
import enfoco_client

TOOLS = [
    {
        "name": "enfoco_estado",
        "description": "Verifica el estado de conexión con el servidor Enfoco (http://137.131.245.249:3000) y si la API Key está configurada.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "enfoco_configurar_api_key",
        "description": "Configura y guarda de forma persistente la API Key de Enfoco (token con prefijo enf_live_...).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "api_key": {
                    "type": "string",
                    "description": "API Key de Enfoco generada en /integrations (ej. enf_live_abc123...)"
                }
            },
            "required": ["api_key"]
        }
    },
    {
        "name": "enfoco_crear_o_actualizar_tarea",
        "description": "Crea una nueva tarea o pendiente en Enfoco (o actualiza si se especifica externalId existente).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Título del pendiente (1 a 240 caracteres)"
                },
                "externalId": {
                    "type": "string",
                    "description": "ID único en el sistema de videos para UPSERT (ej. video-104-edicion)"
                },
                "area": {
                    "type": "string",
                    "enum": ["Trabajo", "Proyectos", "Personal", "Estudio", "Iglesia"],
                    "description": "Área de vida/trabajo (por defecto 'Trabajo')",
                    "default": "Trabajo"
                },
                "project": {
                    "type": "string",
                    "description": "Nombre del proyecto, cliente o canal (por defecto 'Producciones David')",
                    "default": "Producciones David"
                },
                "notes": {
                    "type": "string",
                    "description": "Descripción, subtareas o checklist (formato Markdown '- [ ] ...')"
                },
                "priority": {
                    "type": "integer",
                    "enum": [1, 2, 3],
                    "description": "Prioridad: 1 (Baja), 2 (Media), 3 (Alta). Por defecto 2.",
                    "default": 2
                },
                "minutes": {
                    "type": "integer",
                    "description": "Estimación en minutos (5 a 1440). Por defecto 30.",
                    "default": 30
                },
                "status": {
                    "type": "string",
                    "enum": ["inbox", "todo", "doing", "waiting"],
                    "description": "Estado: 'inbox' (Backlog), 'todo' (Por hacer), 'doing' (En curso), 'waiting' (En revisión).",
                    "default": "todo"
                },
                "planDate": {
                    "type": "string",
                    "description": "Fecha planificada en formato AAAA-MM-DD (si es hoy, entra en planificación diaria)"
                },
                "deadline": {
                    "type": "string",
                    "description": "Fecha límite / vencimiento en formato AAAA-MM-DD"
                },
                "followUp": {
                    "type": "string",
                    "description": "Fecha de seguimiento / recordatorio en formato AAAA-MM-DD"
                }
            },
            "required": ["title"]
        }
    },
    {
        "name": "enfoco_cargar_pipeline_agencia",
        "description": "Sincroniza en lote las tareas prioritarias de lanzamiento, ventas y producción de Producciones David en Enfoco.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]

def handle_tool_call(name: str, args: dict) -> str:
    if name == "enfoco_estado":
        cfg = enfoco_client.cargar_config()
        key_configurada = bool(cfg.get("api_key"))
        key_preview = cfg["api_key"][:12] + "..." if key_configurada else "No configurada"
        return json.dumps({
            "servidor_url": cfg.get("endpoint"),
            "api_key_cargada": key_configurada,
            "api_key_preview": key_preview,
            "archivo_config": str(enfoco_client.CONFIG_FILE)
        }, indent=2, ensure_ascii=False)

    elif name == "enfoco_configurar_api_key":
        key = args["api_key"].strip()
        cfg = enfoco_client.cargar_config()
        cfg["api_key"] = key
        enfoco_client.guardar_config(cfg)
        return json.dumps({
            "ok": True,
            "mensaje": f"API Key guardada exitosamente ({key[:12]}...).",
            "archivo_config": str(enfoco_client.CONFIG_FILE)
        }, indent=2, ensure_ascii=False)

    elif name == "enfoco_crear_o_actualizar_tarea":
        res = enfoco_client.crear_tarea(
            title=args["title"],
            external_id=args.get("externalId"),
            area=args.get("area", "Trabajo"),
            project=args.get("project", "Producciones David"),
            notes=args.get("notes", ""),
            priority=args.get("priority", 2),
            minutes=args.get("minutes", 30),
            status=args.get("status", "todo"),
            plan_date=args.get("planDate"),
            deadline=args.get("deadline"),
            follow_up=args.get("followUp")
        )
        return json.dumps(res, indent=2, ensure_ascii=False)

    elif name == "enfoco_cargar_pipeline_agencia":
        tareas = enfoco_client.pipeline_inicial_producciones_david()
        res = enfoco_client.enviar_tareas(tareas)
        return json.dumps({
            "ok": True,
            "tareas_enviadas": len(tareas),
            "respuesta_enfoco": res
        }, indent=2, ensure_ascii=False)

    raise ValueError(f"Herramienta desconocida: {name}")

def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        req_id = req.get("id")
        method = req.get("method", "")
        params = req.get("params") or {}

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "enfoco-tareas", "version": "1.0.0"},
                },
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        elif method.startswith("notifications/"):
            continue
        elif method == "tools/list":
            resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        elif method == "tools/call":
            t_name = params.get("name", "")
            t_args = params.get("arguments") or {}
            try:
                out = handle_tool_call(t_name, t_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": out}], "isError": False},
                }
            except Exception as e:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True},
                }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        elif req_id is not None:
            resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
