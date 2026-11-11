"""Verificadores deterministas. Solo biblioteca estándar."""
import json
import re
import unicodedata


def limpiar(respuesta):
    """Quita bloques <think>...</think> (y un <think> sin cerrar) y espacios."""
    t = respuesta or ""
    t = re.sub(r"<think>.*?</think>", "", t, flags=re.S | re.I)
    # <think> sin cerrar: la respuesta se cortó pensando, no hay respuesta útil.
    t = re.sub(r"<think>.*\Z", "", t, flags=re.S | re.I)
    # </think> suelto (el <think> inicial lo puso la plantilla): quedarse con lo posterior.
    if re.search(r"</think>", t, flags=re.I):
        t = re.split(r"</think>", t, flags=re.I)[-1]
    return t.strip()


def _norm(s, tildes=True, mayus=True):
    if mayus:
        s = s.lower()
    if tildes:
        s = unicodedata.normalize("NFD", s)
        s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s


# ---------------------------------------------------------------- números

_TOKEN_RE = re.compile(r"(\d+(?:[.,]\d+)*)")


def _candidatos(tok):
    """Valores posibles de un token numérico con convención colombiana."""
    if "." in tok and "," in tok:
        dec = "." if tok.rfind(".") > tok.rfind(",") else ","
        mil = "," if dec == "." else "."
        return [float(tok.replace(mil, "").replace(dec, "."))]
    for sep in (".", ","):
        if sep in tok:
            partes = tok.split(sep)
            if len(partes) > 2:  # 1.234.567
                return [float("".join(partes))]
            if len(partes[1]) == 3 and partes[0] != "0":
                # ambiguo: miles (22.015) o decimal (3.141); se aceptan ambos
                return [float("".join(partes)), float(partes[0] + "." + partes[1])]
            return [float(partes[0] + "." + partes[1])]
    return [float(tok)]


def ultimo_numero(texto):
    """Valores candidatos del último número del texto, o None."""
    ms = list(_TOKEN_RE.finditer(texto))
    if not ms:
        return None
    m = ms[-1]
    cands = _candidatos(m.group(1))
    prev = texto[m.start() - 1] if m.start() > 0 else ""
    if prev == "-" and (m.start() < 2 or texto[m.start() - 2] in " \t\n($=:"):
        cands = [-c for c in cands]
    return cands


def v_numero(p, r):
    cands = ultimo_numero(r)
    if cands is None:
        return False, "no hay números en la respuesta"
    tol = p.get("tolerancia", 0) or 0
    for c in cands:
        if abs(c - p["valor"]) <= tol + 1e-9:
            return True, f"número {c:g}"
    vistos = "/".join(f"{c:g}" for c in cands)
    return False, f"último número {vistos}, esperado {p['valor']:g} (±{tol:g})"


# ----------------------------------------------------------------- opción

_OPC_ESTRICTO = re.compile(
    r"(?<![\w.])(?:"
    r"\(([A-D])\)"
    r"|\*\*([A-D])\*\*"
    r"|([A-D])[).:](?!\w)"
    r"|(?i:respuesta|opci[oó]n|alternativa|literal|letra|correcta)(?i:\s+correcta)?(?i:\s+es)?"
    r"\s*[:\-]?\s*(?i:la\s+|el\s+)?\**\(?([A-D])\b"
    r")"
)
_OPC_SUELTA = re.compile(r"(?<![\w])([A-D])(?![\w])")


def extraer_opcion(r):
    m = _OPC_ESTRICTO.search(r)
    if m:
        return next(g for g in m.groups() if g)
    for m in _OPC_SUELTA.finditer(r):
        letra = m.group(1)
        if letra == "A":
            resto = r[m.end():].lstrip(" \t")
            # "A las 5", "A Bogotá": preposición; solo vale si sigue puntuación o fin
            if resto and resto[0].isalnum():
                continue
        return letra
    return None


def v_opcion(p, r):
    got = extraer_opcion(r)
    ok = got == p["valor"].strip().upper()
    return ok, f"opción detectada {got!r}, esperada {p['valor']}"


# ------------------------------------------------------------- resto

def _flags(f):
    out = 0
    for c in (f or ""):
        out |= {"i": re.I, "s": re.S, "m": re.M}.get(c, 0)
    return out


def v_exacto(p, r):
    ign = p.get("ignorar_mayusculas", True)

    def prep(s):
        s = s.strip().strip("*\"'«»“”` \n")
        s = s.rstrip(".,;:!?¡¿ \n")
        s = s.strip("*\"'«»“”` ")
        return s.lower() if ign else s
    a, b = prep(r), prep(p["valor"])
    return a == b, f"obtenido {a[:60]!r}, esperado {b!r}"


def v_regex(p, r):
    ok = re.search(p["patron"], r, _flags(p.get("flags"))) is not None
    return ok, f"patrón {p['patron']!r} {'encontrado' if ok else 'no encontrado'}"


def v_no_regex(p, r):
    m = re.search(p["patron"], r, _flags(p.get("flags")))
    det = f"encontrado: {m.group(0)!r}" if m else "ausente"
    return m is None, f"patrón prohibido {p['patron']!r} {det}"


def _prep_lista(p, r):
    t = p.get("ignorar_tildes", True)
    m = p.get("ignorar_mayusculas", True)
    return _norm(r, t, m), [_norm(v, t, m) for v in p["valores"]], p["valores"]


def v_contiene_todos(p, r):
    txt, vals, orig = _prep_lista(p, r)
    faltan = [o for v, o in zip(vals, orig) if v not in txt]
    return not faltan, ("faltan: " + ", ".join(map(repr, faltan))) if faltan else "todos presentes"


def v_contiene_alguno(p, r):
    txt, vals, orig = _prep_lista(p, r)
    hay = [o for v, o in zip(vals, orig) if v in txt]
    return bool(hay), ("encontrado: " + ", ".join(map(repr, hay))) if hay else "ninguno presente"


def v_no_contiene(p, r):
    txt, vals, orig = _prep_lista(p, r)
    hay = [o for v, o in zip(vals, orig) if v in txt]
    return not hay, ("aparece prohibido: " + ", ".join(map(repr, hay))) if hay else "ninguno presente"


def _rango(n, p):
    lo, hi = p.get("min"), p.get("max")
    return (lo is None or n >= lo) and (hi is None or n <= hi)


def contar_palabras(r):
    return len([t for t in r.split() if re.search(r"\w", t)])


def v_palabras(p, r):
    n = contar_palabras(r)
    return _rango(n, p), f"{n} palabras (min={p.get('min')}, max={p.get('max')})"


def v_lineas(p, r):
    ls = r.splitlines()
    if p.get("no_vacias", True):
        ls = [l for l in ls if l.strip()]
    n = len(ls)
    return _rango(n, p), f"{n} líneas (min={p.get('min')}, max={p.get('max')})"


_VINETA = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+")


def v_vinetas(p, r):
    n = sum(1 for l in r.splitlines() if _VINETA.match(l))
    if "exacto" in p:
        return n == p["exacto"], f"{n} viñetas (esperadas {p['exacto']})"
    return _rango(n, p), f"{n} viñetas (min={p.get('min')}, max={p.get('max')})"


def v_json(p, r):
    candidatos = [r]
    m = re.search(r"```(?:json)?\s*(.*?)```", r, flags=re.S | re.I)
    if m:
        candidatos.append(m.group(1))
    obj, ok = None, False
    for c in candidatos:
        try:
            obj = json.loads(c.strip())
            ok = True
            break
        except ValueError:
            continue
    if not ok:
        return False, "no es JSON válido"
    tr = p.get("tipo_raiz")
    if tr == "objeto" and not isinstance(obj, dict):
        return False, "la raíz no es un objeto"
    if tr == "lista" and not isinstance(obj, list):
        return False, "la raíz no es una lista"
    claves = p.get("claves")
    if claves:
        if not isinstance(obj, dict):
            return False, "la raíz no es un objeto, no tiene claves"
        faltan = [k for k in claves if k not in obj]
        if faltan:
            return False, "faltan claves: " + ", ".join(faltan)
    return True, "JSON válido"


def v_empieza_con(p, r):
    ign = p.get("ignorar_mayusculas", True)
    a, b = (r.lower(), p["valor"].lower()) if ign else (r, p["valor"])
    return a.startswith(b), f"empieza con {r[:40]!r}, esperado {p['valor']!r}"


def v_termina_con(p, r):
    ign = p.get("ignorar_mayusculas", True)
    r = r.rstrip()
    a, b = (r.lower(), p["valor"].lower()) if ign else (r, p["valor"])
    return a.endswith(b), f"termina con {r[-40:]!r}, esperado {p['valor']!r}"


def v_mayusculas(p, r):
    letras = [c for c in r if c.isalpha()]
    if p.get("modo") == "todo":
        ok = bool(letras) and all(c.isupper() for c in letras)
        return ok, "todo en mayúsculas" if ok else "hay minúsculas o no hay letras"
    ok = not any(c.isupper() for c in letras)
    return ok, "sin mayúsculas" if ok else "hay mayúsculas"


_ES = set("de la el que y en los las un una por con para es se del al lo como pero mas su sus "
          "no muy esta este son esto ese cuando donde porque si le les me te nos hay fue ser tiene".split())
_EN = set("the and of to is are in that it for with on as was this you your have be not they "
          "from at by or an we can will would".split())


def v_idioma_es(p, r):
    toks = re.findall(r"[a-záéíóúñü]+", r.lower())
    toks_n = [_norm(t, True, False) for t in toks]
    es = sum(1 for t in toks_n if t in _ES)
    en = sum(1 for t in toks_n if t in _EN)
    return es > en, f"palabras funcionales es={es} en={en}"


DISPATCH = {
    "exacto": v_exacto, "numero": v_numero, "opcion": v_opcion, "regex": v_regex,
    "no_regex": v_no_regex, "contiene_todos": v_contiene_todos,
    "contiene_alguno": v_contiene_alguno, "no_contiene": v_no_contiene,
    "palabras": v_palabras, "lineas": v_lineas, "vinetas": v_vinetas, "json": v_json,
    "empieza_con": v_empieza_con, "termina_con": v_termina_con,
    "mayusculas": v_mayusculas, "idioma_es": v_idioma_es,
}


def verificar(caso, respuesta):
    """Devuelve (paso, detalle). detalle: lista de {tipo, paso, info} por verificador."""
    r = limpiar(respuesta)
    detalle = []
    for v in caso.get("verificadores") or []:
        tipo = v.get("tipo")
        f = DISPATCH.get(tipo)
        if f is None:
            detalle.append({"tipo": tipo, "paso": False, "info": "tipo de verificador desconocido"})
            continue
        try:
            ok, info = f(v, r)
        except Exception as e:  # parámetros mal escritos en el caso, etc.
            ok, info = False, f"error en verificador: {e!r}"
        detalle.append({"tipo": tipo, "paso": bool(ok), "info": info})
    return all(d["paso"] for d in detalle), detalle
