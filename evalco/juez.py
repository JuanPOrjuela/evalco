"""Juez con rúbrica binaria: una pregunta por llamada, respuesta SI/NO."""
import hashlib
import os
import re

from . import cliente
from .util import agregar_jsonl, leer_jsonl
from .verificadores import _norm, limpiar

PLANTILLA = """Eres un evaluador estricto. Debes decidir si una respuesta cumple un criterio.

MENSAJE DE SISTEMA DADO AL MODELO:
{sistema}

PREGUNTA DEL USUARIO:
{prompt}

REFERENCIA (respuesta modelo o justificación):
{referencia}

RESPUESTA DEL MODELO A EVALUAR:
{respuesta}

CRITERIO (responde solo sobre esto):
{pregunta}

¿Se cumple el criterio? Responde únicamente con una palabra: SI o NO."""


def parsear(texto):
    """Devuelve True/False, o None si no se puede interpretar."""
    t = _norm(limpiar(texto), True, False).upper()
    m = re.match(r"^\W*(SI|NO)\b", t)
    if m:
        return m.group(1) == "SI"
    ms = re.findall(r"\b(SI|NO)\b", t)
    if ms:
        return ms[0] == "SI"
    return None


class Juez:
    def __init__(self, modelo, carpeta):
        self.modelo = modelo
        self.ruta = os.path.join(carpeta, "juez.jsonl")
        self.cache = {r["clave"]: r for r in leer_jsonl(self.ruta)}

    @staticmethod
    def _clave(modelo, caso_id, pregunta, respuesta):
        h = hashlib.sha1("\x1f".join([modelo, caso_id, pregunta, respuesta]).encode("utf-8"))
        return h.hexdigest()

    def preguntar(self, caso, respuesta, pregunta):
        """Devuelve dict: pregunta, paso, sin_parsear, bruto."""
        resp = limpiar(respuesta)
        clave = self._clave(self.modelo, caso["id"], pregunta, resp)
        if clave in self.cache:
            return self.cache[clave]
        prompt = PLANTILLA.format(sistema=caso.get("sistema") or "(ninguno)",
                                  prompt=caso["prompt"],
                                  referencia=caso.get("referencia") or "(sin referencia)",
                                  respuesta=resp or "(respuesta vacía)", pregunta=pregunta)
        try:
            bruto = cliente.chat(self.modelo, prompt, think=False)["texto"]
        except cliente.ErrorCliente as e:
            bruto = f"ERROR: {e}"
        v = parsear(bruto)
        reg = {"clave": clave, "juez": self.modelo, "id": caso["id"], "pregunta": pregunta,
               "paso": bool(v), "sin_parsear": v is None, "bruto": bruto[:300]}
        agregar_jsonl(self.ruta, reg)
        self.cache[clave] = reg
        return reg
