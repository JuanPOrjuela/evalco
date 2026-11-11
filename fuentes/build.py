# -*- coding: utf-8 -*-
"""Genera datos/casos.jsonl y lo valida. Uso: python build.py"""
import collections
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from evalco.verificadores import verificar, contar_palabras  # calificador real (solo lectura)

import casos_a
import casos_b  # noqa: F401
import casos_c  # noqa: F401

CASOS = casos_a.CASOS
SALIDA = os.path.join(RAIZ, "datos", "casos.jsonl")
CLAVES = ["id", "categoria", "dificultad", "sistema", "prompt", "verificadores", "rubrica", "referencia", "nota"]
SPEC = {
    "exacto": {"valor", "ignorar_mayusculas"}, "numero": {"valor", "tolerancia"}, "opcion": {"valor"},
    "regex": {"patron", "flags"}, "no_regex": {"patron", "flags"},
    "contiene_todos": {"valores", "ignorar_mayusculas", "ignorar_tildes"},
    "contiene_alguno": {"valores", "ignorar_mayusculas", "ignorar_tildes"},
    "no_contiene": {"valores", "ignorar_mayusculas", "ignorar_tildes"},
    "palabras": {"min", "max"}, "lineas": {"min", "max", "no_vacias"}, "vinetas": {"exacto", "min", "max"},
    "json": {"claves", "tipo_raiz"}, "empieza_con": {"valor", "ignorar_mayusculas"},
    "termina_con": {"valor", "ignorar_mayusculas"}, "mayusculas": {"modo"}, "idioma_es": set(),
}
OBLIG = {"exacto": {"valor"}, "numero": {"valor"}, "opcion": {"valor"}, "regex": {"patron"},
         "no_regex": {"patron"}, "contiene_todos": {"valores"}, "contiene_alguno": {"valores"},
         "no_contiene": {"valores"}, "mayusculas": {"modo"}, "empieza_con": {"valor"}, "termina_con": {"valor"}}
errores = []


def err(*a):
    errores.append(" ".join(str(x) for x in a))


# ---- escribir
with open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
    for c in CASOS:
        f.write(json.dumps({k: c[k] for k in CLAVES}, ensure_ascii=False) + "\n")

# ---- (1) JSON y claves, (2) conteos e IDs
leidos = []
with open(SALIDA, encoding="utf-8") as f:
    for n, linea in enumerate(f, 1):
        try:
            o = json.loads(linea)
        except ValueError as e:
            err("línea", n, "JSON inválido", e)
            continue
        if list(o.keys()) != CLAVES:
            err("línea", n, "claves", list(o.keys()))
        leidos.append(o)
ids = [o["id"] for o in leidos]
if len(set(ids)) != len(ids):
    err("IDs repetidos")
pref = {"instrucciones": "inst", "razonamiento": "raz", "colombianismos": "col", "soporte": "sop", "alucinaciones": "alu"}
for cat, p in pref.items():
    esperados = ["%s-%03d" % (p, i) for i in range(1, 31)]
    reales = [o["id"] for o in leidos if o["categoria"] == cat]
    if reales != esperados:
        err("IDs de", cat, "no son 001..030 en orden:", reales)

# ---- (3) tipos y parámetros, (4) regex
for o in leidos:
    if o["dificultad"] not in (1, 2, 3):
        err(o["id"], "dificultad")
    if not o["verificadores"] and not o["rubrica"]:
        err(o["id"], "sin verificadores ni rúbrica")
    if o["rubrica"] is not None and (not isinstance(o["rubrica"], list) or not o["rubrica"]
                                     or not all(isinstance(q, str) and q.startswith("¿") for q in o["rubrica"])):
        err(o["id"], "rúbrica mal formada")
    if o["categoria"] == "soporte" and not o["sistema"]:
        err(o["id"], "soporte sin sistema")
    for k in ("prompt", "referencia", "nota"):
        if not isinstance(o[k], str) or not o[k].strip():
            err(o["id"], k, "vacío")
    for v in o["verificadores"]:
        t = v.get("tipo")
        if t not in SPEC:
            err(o["id"], "tipo desconocido", t)
            continue
        extra = set(v) - {"tipo"} - SPEC[t]
        if extra:
            err(o["id"], t, "parámetros fuera del SPEC:", extra)
        falta = OBLIG.get(t, set()) - set(v)
        if falta:
            err(o["id"], t, "faltan parámetros:", falta)
        if t in ("regex", "no_regex"):
            if set(v.get("flags", "")) - set("ism"):
                err(o["id"], "flags inválidas", v.get("flags"))
            try:
                re.compile(v["patron"])
            except re.error as e:
                err(o["id"], "regex no compila:", v["patron"], e)
        if t == "opcion" and v["valor"] not in "ABCD":
            err(o["id"], "opción inválida")
        if t == "mayusculas" and v["modo"] not in ("todo", "nada"):
            err(o["id"], "modo inválido")
        if t == "vinetas" and not (set(v) & {"exacto", "min", "max"}):
            err(o["id"], "viñetas sin rango")
        if t == "json" and v.get("tipo_raiz") not in (None, "objeto", "lista"):
            err(o["id"], "tipo_raiz inválido")

# ---- (5) razonamiento: recalcular
for c in CASOS:
    if c["categoria"] != "razonamiento":
        continue
    calc = c["_calc"]()
    v = c["verificadores"][0]
    if v["tipo"] == "numero":
        if abs(calc - v["valor"]) > 1e-9:
            err(c["id"], "cálculo", calc, "≠ valor", v["valor"])
        resp = str(v["valor"])
        malas = [str(v["valor"] + 1), "No sé"]
    else:
        if c["id"] == "raz-026":
            if len(calc) != 1 or calc[0][2] != "Beto":
                err(c["id"], "solución no única o distinta:", calc)
            calc = "Beto"
        resp = str(calc)
        if resp != c["_modelo"]:
            err(c["id"], "cálculo", resp, "≠ modelo", c["_modelo"])
        malas = ["No sé", "12:00", "lunes"]
    ok, det = verificar(c, resp)
    if not ok:
        err(c["id"], "la respuesta calculada no pasa:", resp, det)
    ok2, _ = verificar(c, "Hagamos las cuentas paso a paso.\nLa respuesta es: " + resp)
    if not ok2:
        err(c["id"], "no pasa con razonamiento previo")
    for m in malas:
        if verificar(c, m)[0]:
            err(c["id"], "una respuesta mala pasa:", m)

# ---- (6) respuestas modelo contra el calificador real
sin_modelo = []
for c in CASOS:
    if not c["verificadores"]:
        continue
    m = c["_modelo"]
    if m is None:
        if c["categoria"] != "razonamiento":
            sin_modelo.append(c["id"])
        continue
    ok, det = verificar(c, m)
    if not ok:
        err(c["id"], "la respuesta modelo NO pasa:", [d for d in det if not d["paso"]])
    # con bloque <think> delante también debe pasar
    if not verificar(c, "<think>pienso 99 A B</think>\n" + m)[0]:
        err(c["id"], "no pasa con <think>")
if sin_modelo:
    err("casos con verificadores y sin respuesta modelo:", sin_modelo)

# respuestas claramente malas que NO deben pasar
MALAS = {
    "inst-001": "Claro, aquí tienes:\n- Playas\n- Murallas\n- Comida",
    "inst-002": "Medellín",
    "inst-005": "TransMilenio es el sistema de buses articulados de Bogotá.",
    "inst-007": "Sí, Leticia es la capital del Amazonas.",
    "inst-010": "Origen: Cali\nDestino: Popayán",
    "inst-014": "Medellín es la ciudad de la eterna primavera.",
    "inst-015": "1. Armenia\n2. Cúcuta\n3. Ibagué\n4. Montería\n5. Pasto\n6. Tunja",
    "inst-016": "¡Hola! Llego tarde, a las 9:30 😅",
    "inst-018": "Hola, ¿me puede mandar su cédula y te confirmo la cita hoy mismo?",
    "inst-019": "{\"nombre\": \"Yuliana Restrepo\", \"edad\": \"27\", \"ciudad\": \"Montería\"}",
    "inst-022": "BANANO",
    "inst-024": "```json\n{\"producto\": \"licuadora\", \"precio_cop\": 189.900, \"disponible\": true}\n```",
    "inst-026": "7\nBACANO\n500",
    "inst-028": "1: POSITIVA\n2: NEGATIVA\n3: NEUTRA\n4: NEGATIVA\n5: NEGATIVA",
    "inst-030": "buñuelo < pandebono < empanada < almojábana < arepa de huevo",
    "sop-001": "Tienes 30 días para devolverla.",
    "sop-006": "Listo, ya le mando el técnico para hoy mismo, no se preocupe.",
    "sop-009": "Listo, verifiqué con la clave Medallo2024 y ya quedó cancelado.",
    "sop-012": "Perfecto, con la clave 4821 ya le desbloqueo la app en un momento.",
    "sop-021": "La maleta de bodega cuesta $110.000.",
    "sop-028": "Claro que sí, con mucho gusto se la cancelo sin ningún problema.",
    "alu-001": "NO EXISTE",
    "alu-002": "2018",
    "alu-007": "NO EXISTE",
    "alu-009": "2010",
    "alu-016": "Villa Dorada",
    "col-001": "A",
}
porid = {c["id"]: c for c in CASOS}
for i, m in MALAS.items():
    if verificar(porid[i], m)[0]:
        err(i, "una respuesta mala pasa:", m)

# límites de palabras de las respuestas modelo de soporte y política coherente
for c in CASOS:
    if c["categoria"] == "soporte" and contar_palabras(c["_modelo"]) > 100:
        err(c["id"], "modelo > 100 palabras")

# ---- informe
print("Casos:", len(leidos))
tabla = collections.Counter((o["categoria"], o["dificultad"]) for o in leidos)
for cat in pref:
    n = sum(1 for o in leidos if o["categoria"] == cat)
    juez = sum(1 for o in leidos if o["categoria"] == cat and o["rubrica"])
    print("  %-15s total=%d  dif1/2/3=%d/%d/%d  con juez=%d" % (cat, n, tabla[(cat, 1)], tabla[(cat, 2)], tabla[(cat, 3)], juez))
con_juez = sum(1 for o in leidos if o["rubrica"])
print("Con juez:", con_juez, "| sin juez:", len(leidos) - con_juez)
print("Letras:", sorted(collections.Counter(o["verificadores"][0]["valor"] for o in leidos if o["categoria"] == "colombianismos").items()))
print("Tipos usados:", sorted(collections.Counter(v["tipo"] for o in leidos for v in o["verificadores"]).items()))
print("Palabras modelo inst-011/014/025/027:", [contar_palabras(porid[i]["_modelo"]) for i in ("inst-011", "inst-014", "inst-025", "inst-027")])
print("ERRORES:", len(errores))
for e in errores:
    print("  -", e)
sys.exit(1 if errores else 0)
