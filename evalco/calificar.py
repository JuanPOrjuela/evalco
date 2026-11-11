"""Califica respuestas.jsonl -> calificaciones.jsonl."""
import argparse
import json
import os
import sys

from .juez import Juez
from .util import leer_jsonl, ultimas_respuestas
from .verificadores import verificar


def main(argv=None):
    ap = argparse.ArgumentParser(prog="evalco.calificar")
    ap.add_argument("carpeta")
    ap.add_argument("--casos", default="datos/casos.jsonl")
    ap.add_argument("--juez", default="qwen3:8b")
    a = ap.parse_args(argv)

    casos = {c["id"]: c for c in leer_jsonl(a.casos)}
    resp = ultimas_respuestas(a.carpeta)
    juez = None
    out = []
    for (modelo, cid), r in sorted(resp.items()):
        c = casos.get(cid)
        if c is None:
            continue
        texto = r.get("respuesta", "")
        if r.get("error"):
            paso, det, rub = False, [{"tipo": "error", "paso": False, "info": r["error"]}], []
        else:
            paso, det = verificar(c, texto)
            rub = []
            # La rúbrica solo se pregunta si los verificadores ya pasaron (ahorra llamadas).
            if c.get("rubrica") and paso:
                juez = juez or Juez(a.juez, a.carpeta)
                for q in c["rubrica"]:
                    v = juez.preguntar(c, texto, q)
                    rub.append({"pregunta": q, "paso": v["paso"], "sin_parsear": v["sin_parsear"]})
                paso = all(x["paso"] for x in rub)
            elif c.get("rubrica"):
                rub = [{"pregunta": q, "paso": None, "omitida": True} for q in c["rubrica"]]
        out.append({"modelo": modelo, "id": cid, "categoria": c["categoria"],
                    "dificultad": c["dificultad"], "paso": paso,
                    "verificadores": det, "rubrica": rub,
                    "juez": a.juez if c.get("rubrica") else None})
        print(f"{modelo} {cid} {'OK' if paso else 'FALLA'}", flush=True)
    ruta = os.path.join(a.carpeta, "calificaciones.jsonl")
    with open(ruta, "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    print(f"{len(out)} calificaciones -> {ruta}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
