import json
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from evalco import reporte  # noqa: E402


class TestWilson(unittest.TestCase):
    def test_valores_conocidos(self):
        lo, hi = reporte.wilson(8, 10)
        self.assertAlmostEqual(lo, 0.4902, places=3)
        self.assertAlmostEqual(hi, 0.9433, places=3)

    def test_extremos(self):
        lo, hi = reporte.wilson(0, 10)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 0.2775, places=3)
        lo, hi = reporte.wilson(10, 10)
        self.assertAlmostEqual(lo, 0.7225, places=3)
        self.assertEqual(hi, 1.0)
        self.assertEqual(reporte.wilson(0, 0), (0.0, 0.0))


def escribir(ruta, filas):
    with open(ruta, "w", encoding="utf-8") as f:
        for x in filas:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")


class TestReporte(unittest.TestCase):
    def test_generar(self):
        with tempfile.TemporaryDirectory() as d:
            casos = [{"id": "r-1", "categoria": "razonamiento", "dificultad": 1,
                      "prompt": "2+2? <b>x</b>"},
                     {"id": "r-2", "categoria": "razonamiento", "dificultad": 2, "prompt": "3+3?"},
                     {"id": "c-1", "categoria": "colombianismos", "dificultad": 1, "prompt": "bacano?"}]
            escribir(os.path.join(d, "casos.jsonl"), casos)
            escribir(os.path.join(d, "respuestas.jsonl"), [
                {"modelo": "m1", "id": "r-1", "respuesta": "<think>x</think>5 <script>alert(1)</script>",
                 "segundos": 2.0, "think": "off"},
                {"modelo": "m1", "id": "r-2", "respuesta": "6", "segundos": 4.0, "think": "off"},
                {"modelo": "m1", "id": "c-1", "respuesta": "B", "segundos": 3.0, "think": "off"}])
            escribir(os.path.join(d, "calificaciones.jsonl"), [
                {"modelo": "m1", "id": "r-1", "categoria": "razonamiento", "dificultad": 1, "paso": False,
                 "verificadores": [{"tipo": "numero", "paso": False, "info": "esperado 4"}], "rubrica": []},
                {"modelo": "m1", "id": "r-2", "categoria": "razonamiento", "dificultad": 2, "paso": True,
                 "verificadores": [{"tipo": "numero", "paso": True, "info": "ok"}], "rubrica": []},
                {"modelo": "m1", "id": "c-1", "categoria": "colombianismos", "dificultad": 1, "paso": True,
                 "verificadores": [{"tipo": "opcion", "paso": True, "info": "ok"}], "rubrica": []}])
            self.assertEqual(reporte.main([d, "--casos", os.path.join(d, "casos.jsonl")]), 0)
            md = pathlib.Path(d, "resumen.md").read_text(encoding="utf-8")
            html_ = pathlib.Path(d, "index.html").read_text(encoding="utf-8")
            self.assertIn("m1", md)
            self.assertIn("50 % (1/2)", md)
            self.assertIn("esperado 4", md)
            self.assertIn("3.0", md)
            self.assertNotIn("<script>alert", html_)
            self.assertIn("&lt;script&gt;", html_)
            self.assertIn("&lt;b&gt;x&lt;/b&gt;", html_)
            self.assertIn("prefers-color-scheme:dark", html_)
            self.assertNotIn("http://", html_.replace("http://www", ""))


if __name__ == "__main__":
    unittest.main()
