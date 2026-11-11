"""Cliente mínimo de Ollama /api/chat."""
import json
import time
import urllib.error
import urllib.request

URL = "http://localhost:11434/api/chat"


class ErrorCliente(Exception):
    pass


def _post(payload, timeout):
    req = urllib.request.Request(
        URL, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def chat(modelo, prompt, sistema=None, think=None, timeout=180):
    """Devuelve dict: texto, segundos, tokens_in, tokens_out.

    think: None (no enviar), True o False.
    """
    msgs = []
    if sistema:
        msgs.append({"role": "system", "content": sistema})
    msgs.append({"role": "user", "content": prompt})
    payload = {"model": modelo, "messages": msgs, "stream": False,
               "options": {"temperature": 0, "seed": 42, "num_ctx": 4096}}
    if think is not None:
        payload["think"] = think
    t0 = time.time()
    ultimo = None
    for _ in range(2):  # un reintento ante error de red
        try:
            try:
                data = _post(payload, timeout)
            except urllib.error.HTTPError as e:
                cuerpo = e.read().decode("utf-8", "replace")
                if e.code == 400 and "think" in cuerpo.lower() and "think" in payload:
                    # el modelo no soporta "think": reintentar sin ese campo
                    payload.pop("think")
                    data = _post(payload, timeout)
                else:
                    raise ErrorCliente(f"HTTP {e.code}: {cuerpo[:200]}")
            msg = data.get("message", {})
            texto = msg.get("content", "") or ""
            if msg.get("thinking") and think is not False:
                texto = "<think>" + msg["thinking"] + "</think>" + texto
            return {"texto": texto, "segundos": round(time.time() - t0, 2),
                    "tokens_in": data.get("prompt_eval_count"),
                    "tokens_out": data.get("eval_count")}
        except ErrorCliente:
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            ultimo = e
            time.sleep(2)
    raise ErrorCliente(f"error de red: {ultimo!r}")
