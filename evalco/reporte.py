"""Genera resumen.md e index.html a partir de calificaciones.jsonl."""
import argparse
import html
import math
import os
import sys

from .util import leer_jsonl, ultimas_respuestas
from .verificadores import limpiar

CATEGORIAS = ["instrucciones", "razonamiento", "colombianismos", "soporte", "alucinaciones"]


def wilson(k, n, z=1.96):
    """Intervalo de Wilson (bajo, alto) como proporciones; (0, 0) si n == 0."""
    if n == 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / d
    mar = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, centro - mar), min(1.0, centro + mar)


def _fmt(k, n):
    if n == 0:
        return "—"
    lo, hi = wilson(k, n)
    return f"{100 * k / n:.0f} % ({k}/{n}) [{100 * lo:.0f}–{100 * hi:.0f}]"


def _recorta(s, n):
    s = (s or "").strip()
    return s if len(s) <= n else s[:n].rstrip() + " […]"


def _fallo_texto(cal):
    partes = []
    for d in cal.get("verificadores", []):
        if not d["paso"]:
            partes.append(f"{d['tipo']}: {d['info']}")
    for q in cal.get("rubrica", []):
        if q.get("paso") is False:
            extra = " (juez no devolvió SI/NO)" if q.get("sin_parsear") else ""
            partes.append(f"rúbrica: {q['pregunta']}{extra}")
    return "; ".join(partes) or "sin detalle"


def construir(carpeta, casos_ruta):
    casos = {c["id"]: c for c in leer_jsonl(casos_ruta)}
    cals = leer_jsonl(os.path.join(carpeta, "calificaciones.jsonl"))
    resp = ultimas_respuestas(carpeta)
    modelos = sorted({c["modelo"] for c in cals})
    cats = [c for c in CATEGORIAS if any(x["categoria"] == c for x in cals)]
    cats += sorted({x["categoria"] for x in cals} - set(cats))
    difs = sorted({x["dificultad"] for x in cals})
    datos = {"modelos": modelos, "cats": cats, "difs": difs, "tabla": {}, "total": {},
             "dif": {}, "tiempo": {}, "think": {}, "fallos": {}, "juez": set(), "sin_parsear": 0}
    for m in modelos:
        mine = [c for c in cals if c["modelo"] == m]
        for cat in cats:
            sub = [c for c in mine if c["categoria"] == cat]
            datos["tabla"][(m, cat)] = (sum(c["paso"] for c in sub), len(sub))
        datos["total"][m] = (sum(c["paso"] for c in mine), len(mine))
        for d in difs:
            sub = [c for c in mine if c["dificultad"] == d]
            datos["dif"][(m, d)] = (sum(c["paso"] for c in sub), len(sub))
        ts = [resp[(m, c["id"])].get("segundos") for c in mine if (m, c["id"]) in resp]
        ts = [t for t in ts if t is not None]
        datos["tiempo"][m] = sum(ts) / len(ts) if ts else None
        thinks = {resp[(m, c["id"])].get("think", "default") for c in mine if (m, c["id"]) in resp}
        datos["think"][m] = ", ".join(sorted(thinks)) or "—"
        for cat in cats:
            ej = []
            for c in sorted((c for c in mine if c["categoria"] == cat and not c["paso"]),
                            key=lambda c: c["id"])[:2]:
                caso = casos.get(c["id"], {})
                r = resp.get((m, c["id"]), {})
                ej.append({"id": c["id"], "prompt": _recorta(caso.get("prompt"), 300),
                           "respuesta": _recorta(limpiar(r.get("respuesta", "")) or
                                                 ("(error: " + r["error"] + ")" if r.get("error") else "(vacía)"), 400),
                           "fallo": _fallo_texto(c)})
            datos["fallos"][(m, cat)] = ej
        for c in mine:
            if c.get("juez"):
                datos["juez"].add(c["juez"])
            datos["sin_parsear"] += sum(1 for q in c.get("rubrica", []) if q.get("sin_parsear"))
    return datos


def _tabla_filas(datos, claves, getter):
    return [[m] + [_fmt(*getter(m, k)) for k in claves] for m in datos["modelos"]]


def a_markdown(datos):
    L = ["# Resultados EvalCO", ""]
    ms = datos["modelos"]
    nota = "IC = intervalo de Wilson al 95 %, en puntos porcentuales."
    L += ["## Aciertos por categoría", "", nota, ""]
    L += ["| Modelo | " + " | ".join(datos["cats"]) + " | Total |",
          "|---|" + "---|" * (len(datos["cats"]) + 1)]
    for m in ms:
        celdas = [_fmt(*datos["tabla"][(m, c)]) for c in datos["cats"]] + [_fmt(*datos["total"][m])]
        L.append(f"| {m} | " + " | ".join(celdas) + " |")
    L += ["", "## Aciertos por dificultad", ""]
    L += ["| Modelo | " + " | ".join(f"Dificultad {d}" for d in datos["difs"]) + " |",
          "|---|" + "---|" * len(datos["difs"])]
    for m in ms:
        L.append(f"| {m} | " + " | ".join(_fmt(*datos["dif"][(m, d)]) for d in datos["difs"]) + " |")
    L += ["", "## Tiempo medio por respuesta", "", "| Modelo | Segundos | Modo think |", "|---|---|---|"]
    for m in ms:
        t = datos["tiempo"][m]
        L.append(f"| {m} | {'—' if t is None else f'{t:.1f}'} | {datos['think'][m]} |")
    if datos["juez"]:
        L += ["", f"Juez de rúbricas: {', '.join(sorted(datos['juez']))}. "
              "Si el juez también compite, su puntaje puede estar sesgado a su favor. "
              f"Veredictos del juez sin SI/NO interpretable (contados como NO): {datos['sin_parsear']}."]
    L += ["", "## Ejemplos de fallos", ""]
    for m in ms:
        for cat in datos["cats"]:
            ej = datos["fallos"].get((m, cat)) or []
            if not ej:
                continue
            L += [f"### {m} · {cat}", ""]
            for e in ej:
                L += [f"- **{e['id']}** — falló: {e['fallo']}",
                      f"  - Prompt: {e['prompt']!r}",
                      f"  - Respuesta: {e['respuesta']!r}"]
            L.append("")
    return "\n".join(L) + "\n"


CSS = """
:root{--fg:#1a1a1a;--mut:#666;--bg:#fff;--line:#d8d8d8;--code:#f5f5f5}
@media (prefers-color-scheme:dark){:root{--fg:#e6e6e6;--mut:#999;--bg:#141414;--line:#3a3a3a;--code:#1e1e1e}}
*{box-sizing:border-box}
body{margin:0 auto;max-width:60rem;padding:1.5rem 1rem 4rem;background:var(--bg);color:var(--fg);
font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
h1{font-size:1.6rem;margin:0 0 .25rem}h2{font-size:1.2rem;margin:2.2rem 0 .6rem;border-bottom:1px solid var(--line);padding-bottom:.25rem}
h3{font-size:1rem;margin:1.4rem 0 .4rem}
p,li{max-width:46rem}.mut{color:var(--mut);font-size:.9rem}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:.9rem;font-variant-numeric:tabular-nums}
th,td{border-bottom:1px solid var(--line);padding:.4rem .6rem;text-align:left;vertical-align:top;white-space:nowrap}
th{font-weight:600;border-bottom:1px solid var(--fg)}
.fallo{margin:.6rem 0 1rem;padding-left:.8rem;border-left:2px solid var(--line)}
.fallo pre{margin:.2rem 0;white-space:pre-wrap;word-break:break-word;background:var(--code);padding:.4rem .6rem;font:13px/1.4 ui-monospace,Consolas,monospace}
details summary{cursor:pointer}
"""


def _e(s):
    return html.escape(str(s))


def _html_tabla(cab, filas):
    h = ["<div class='scroll'><table><thead><tr>"]
    h += [f"<th>{_e(c)}</th>" for c in cab]
    h.append("</tr></thead><tbody>")
    for f in filas:
        h.append("<tr>" + "".join(f"<td>{_e(c)}</td>" for c in f) + "</tr>")
    h.append("</tbody></table></div>")
    return "".join(h)


def a_html(datos):
    ms, cats, difs = datos["modelos"], datos["cats"], datos["difs"]
    H = ["<!doctype html><html lang='es'><head><meta charset='utf-8'>",
         "<meta name='viewport' content='width=device-width,initial-scale=1'>",
         "<title>EvalCO: resultados</title><style>", CSS, "</style></head><body>",
         "<h1>EvalCO</h1><p class='mut'>Banco de evaluación de modelos de lenguaje en español colombiano.</p>",
         "<h2>Aciertos por categoría</h2>",
         "<p class='mut'>Porcentaje de casos aprobados, aprobados/total y, entre corchetes, el "
         "intervalo de Wilson al 95 % en puntos porcentuales.</p>"]
    filas = [[m] + [_fmt(*datos["tabla"][(m, c)]) for c in cats] + [_fmt(*datos["total"][m])] for m in ms]
    H.append(_html_tabla(["Modelo"] + cats + ["Total"], filas))
    H.append("<h2>Aciertos por dificultad</h2>")
    H.append(_html_tabla(["Modelo"] + [f"Dificultad {d}" for d in difs],
                         [[m] + [_fmt(*datos["dif"][(m, d)]) for d in difs] for m in ms]))
    H.append("<h2>Tiempo medio por respuesta</h2>")
    H.append(_html_tabla(["Modelo", "Segundos", "Modo think"],
                         [[m, "—" if datos["tiempo"][m] is None else f"{datos['tiempo'][m]:.1f}",
                           datos["think"][m]] for m in ms]))
    if datos["juez"]:
        H.append(f"<p class='mut'>Juez de rúbricas: {_e(', '.join(sorted(datos['juez'])))}. Si el juez "
                 f"también compite, su puntaje puede estar sesgado a su favor. Veredictos sin SI/NO "
                 f"interpretable (contados como NO): {datos['sin_parsear']}.</p>")
    H.append("<h2>Ejemplos de fallos</h2>")
    for m in ms:
        for cat in cats:
            ej = datos["fallos"].get((m, cat)) or []
            if not ej:
                continue
            H.append(f"<h3>{_e(m)} · {_e(cat)}</h3>")
            for e in ej:
                H.append(f"<div class='fallo'><strong>{_e(e['id'])}</strong> — falló: {_e(e['fallo'])}"
                         f"<pre>Prompt: {_e(e['prompt'])}</pre><pre>Respuesta: {_e(e['respuesta'])}</pre></div>")
    H.append("</body></html>")
    return "".join(H)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="evalco.reporte")
    ap.add_argument("carpeta")
    ap.add_argument("--casos", default="datos/casos.jsonl")
    a = ap.parse_args(argv)
    datos = construir(a.carpeta, a.casos)
    with open(os.path.join(a.carpeta, "resumen.md"), "w", encoding="utf-8") as f:
        f.write(a_markdown(datos))
    with open(os.path.join(a.carpeta, "index.html"), "w", encoding="utf-8") as f:
        f.write(a_html(datos))
    print(f"escrito {a.carpeta}/resumen.md e index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
