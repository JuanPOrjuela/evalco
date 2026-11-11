import json
import os


def leer_jsonl(ruta):
    if not os.path.exists(ruta):
        return []
    out = []
    with open(ruta, encoding="utf-8") as f:
        for n, linea in enumerate(f, 1):
            linea = linea.strip()
            if not linea:
                continue
            try:
                out.append(json.loads(linea))
            except ValueError:
                print(f"aviso: línea {n} de {ruta} no es JSON, se omite")
    return out


def agregar_jsonl(ruta, obj):
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def ultimas_respuestas(carpeta):
    """Última línea por (modelo, id) de respuestas.jsonl."""
    d = {}
    for r in leer_jsonl(os.path.join(carpeta, "respuestas.jsonl")):
        d[(r["modelo"], r["id"])] = r
    return d
