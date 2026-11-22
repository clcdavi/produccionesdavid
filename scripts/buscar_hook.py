#!/usr/bin/env python3
"""
Buscador y Recomendador de Hooks Virales para Producciones David
Accede al banco de 1000 hooks reales clasificados con enlaces a Instagram/TikTok.
"""
import argparse
import json
import random
import re
from pathlib import Path

HOOKS_FILE = Path.home() / ".gemini/config/skills-shared/instagram/references/1000-viral-hooks.json"

def load_hooks():
    if not HOOKS_FILE.exists():
        raise FileNotFoundError(f"No se encontró el archivo de hooks en: {HOOKS_FILE}")
    with open(HOOKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def search_hooks(query=None, category=None, limit=10, random_mode=False):
    hooks = load_hooks()
    results = []

    if category:
        cat_lower = category.lower()
        hooks = [h for h in hooks if cat_lower in h.get("category", "").lower()]

    if query:
        q_lower = query.lower()
        # Buscar en el texto del hook
        hooks = [h for h in hooks if q_lower in h.get("hook", "").lower()]

    if random_mode:
        results = random.sample(hooks, min(limit, len(hooks)))
    else:
        results = hooks[:limit]

    return results

def main():
    parser = argparse.ArgumentParser(description="Busca y explora hooks virales para Reels y carruseles.")
    parser.add_argument("query", nargs="?", default=None, help="Término o palabra clave a buscar")
    parser.add_argument("-c", "--category", default=None, help="Filtrar por categoría (ej: 'Verdades', 'Dolor', 'Transformación')")
    parser.add_argument("-l", "--limit", type=int, default=8, help="Cantidad de resultados (def: 8)")
    parser.add_argument("-r", "--random", action="store_true", help="Devolver ganchos aleatorios como disparadores creativos")
    parser.add_argument("--categories", action="store_true", help="Listar todas las categorías disponibles")

    args = parser.parse_args()

    if args.categories:
        hooks = load_hooks()
        from collections import Counter
        counts = Counter(h["category"] for h in hooks)
        print("\n📂 CATEGORÍAS DISPONIBLES EN EL BANCO DE 1000 HOOKS:")
        for cat, c in counts.most_common():
            print(f"  • {cat} ({c} hooks)")
        print()
        return

    results = search_hooks(query=args.query, category=args.category, limit=args.limit, random_mode=args.random)

    if not results:
        print(f"\n❌ No se encontraron hooks para la búsqueda: '{args.query}' (categoría: {args.category})")
        return

    title_str = f"Resultados para '{args.query}'" if args.query else "Hooks recomendados"
    if args.category:
        title_str += f" en categoría '{args.category}'"
    if args.random:
        title_str += " (aleatorios)"

    print(f"\n🎯 {title_str} ({len(results)} encontrados):\n")
    for idx, h in enumerate(results, 1):
        print(f"{idx:02d}. [{h['category']}]")
        print(f"    🪝 \"{h['hook']}\"")
        if h.get('url'):
            print(f"    🔗 Ejemplo real: {h['url']}")
        print()

if __name__ == "__main__":
    main()
