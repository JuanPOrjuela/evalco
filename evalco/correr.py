"""Corre los casos contra modelos de Ollama y guarda respuestas.jsonl."""
import argparse
import os
import sys

from . import cliente
from .util import agregar_jsonl, leer_jsonl


def main(argv=None):
    ap = argparse.ArgumentParser(prog="evalco.correr")
    ap.add_argument("--casos", default="datos/casos.jsonl")
    ap.add_argument("--modelos", nargs="+", required=True)
    ap.add_argument("--salida", default="resultados/")
    ap.add_argument("--think-off", action="store_true", help="enviar think:false")
    ap.add_argument("--limite", type=int, default=None, help="solo los primeros N casos")
    a = ap.parse_args(argv)

    casos = leer_jsonl(a.casos)
    if a.limite:
        casos = casos[:a.limite]
    os.makedirs(a.salida, exist_ok=True)
    ruta = os.path.join(a.salida, "respuestas.jsonl")
    hechos = {(r["modelo"], r["id"]) for r in leer_jsonl(ruta) if not r.get("error")}
    think = False if a.think_off else None

    for modelo in a.modelos:
        pend = [c for c in casos if (modelo, c["id"]) not in hechos]
        print(f"== {modelo}: {len(pend)} pendientes de {len(casos)}", flush=True)
        for i, c in enumerate(pend, 1):
            reg = {"modelo": modelo, "id": c["id"], "think": "off" if a.think_off else "default"}
            try:
                r = cliente.chat(modelo, c["prompt"], c.get("sistema"), think=think)
                reg.update(respuesta=r["texto"], segundos=r["segundos"],
                           tokens_in=r["tokens_in"], tokens_out=r["tokens_out"])
                print(f"[{modelo}] {i}/{len(pend)} {c['id']} {r['segundos']}s "
                      f"{r['tokens_out']} tok", flush=True)
            except cliente.ErrorCliente as e:
                reg.update(respuesta="", segundos=None, tokens_in=None, tokens_out=None,
                           error=str(e))
                print(f"[{modelo}] {i}/{len(pend)} {c['id']} ERROR {e}", flush=True)
            agregar_jsonl(ruta, reg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
