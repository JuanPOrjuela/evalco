import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from evalco.verificadores import extraer_opcion, limpiar, ultimo_numero, verificar  # noqa: E402
from evalco.juez import parsear  # noqa: E402


def v(tipo, resp, **kw):
    kw["tipo"] = tipo
    return verificar({"verificadores": [kw]}, resp)[0]


class TestLimpiar(unittest.TestCase):
    def test_think(self):
        self.assertEqual(limpiar("<think>hmm\nmás</think>\n  42 "), "42")

    def test_think_sin_cerrar(self):
        self.assertEqual(limpiar("<think>sigo pensando y se cortó"), "")

    def test_think_suelto(self):
        self.assertEqual(limpiar("pensando...</think>Hola"), "Hola")

    def test_sin_think(self):
        self.assertEqual(limpiar("  hola \n"), "hola")


class TestNumero(unittest.TestCase):
    def num(self, resp, valor, tol=0):
        return v("numero", resp, valor=valor, tolerancia=tol)

    def test_formatos_colombianos(self):
        self.assertTrue(self.num("22015", 22015))
        self.assertTrue(self.num("$22.015", 22015))
        self.assertTrue(self.num("Son 22.015 pesos.", 22015))
        self.assertTrue(self.num("1.234.567", 1234567))
        self.assertTrue(self.num("$1.234.567,50", 1234567.5))
        self.assertTrue(self.num("3,5", 3.5))
        self.assertTrue(self.num("3.50", 3.5))
        self.assertTrue(self.num("22,015", 22015))
        self.assertTrue(self.num("1,234,567", 1234567))

    def test_ultimo_numero(self):
        self.assertTrue(self.num("Primero 5, luego 10, total 15.", 15))
        self.assertFalse(self.num("Total 15 pesos, son 2 personas", 15))

    def test_decimal_con_tres_digitos(self):
        self.assertTrue(self.num("3.141", 3.141, 0.0001))

    def test_negativo(self):
        self.assertTrue(self.num("Quedan -5 grados", -5))
        self.assertFalse(self.num("Quedan -5 grados", 5))

    def test_tolerancia(self):
        self.assertTrue(self.num("3.14", 3.1416, 0.01))
        self.assertFalse(self.num("3.2", 3.1416, 0.01))

    def test_incorrecto_y_sin_numero(self):
        self.assertFalse(self.num("22.016", 22015))
        self.assertFalse(self.num("no sé", 3))
        self.assertIsNone(ultimo_numero("sin números"))

    def test_con_think(self):
        self.assertTrue(self.num("<think>2 + 2 = 5?</think>4", 4))


class TestOpcion(unittest.TestCase):
    def test_formatos(self):
        for r in ["A", "A)", "(A)", "A.", "Respuesta: A", "**A**", "La respuesta correcta es la A.",
                  "A) Algo porque sí", "Opción A", "A: significa"]:
            self.assertEqual(extraer_opcion(r), "A", r)
        self.assertEqual(extraer_opcion("**B. Genial**"), "B")
        self.assertEqual(extraer_opcion("D"), "D")

    def test_no_confunde_a_minuscula(self):
        self.assertEqual(extraer_opcion("Es una expresión que va a la B)"), "B")
        self.assertEqual(extraer_opcion("Respuesta: C porque va a casa"), "C")
        self.assertIsNone(extraer_opcion("a veces es así, pero no sé"))

    def test_preposicion_a_mayuscula(self):
        self.assertEqual(extraer_opcion("A Bogotá se llega por la B)"), "B")

    def test_verificador(self):
        self.assertTrue(v("opcion", "Respuesta: B", valor="B"))
        self.assertFalse(v("opcion", "Respuesta: B", valor="A"))
        self.assertFalse(v("opcion", "no sé la respuesta", valor="A"))


class TestTextuales(unittest.TestCase):
    def test_exacto(self):
        self.assertTrue(v("exacto", "bogotá.", valor="Bogotá"))
        self.assertFalse(v("exacto", "Bogotá D.C.", valor="Bogotá"))
        self.assertFalse(v("exacto", "bogotá", valor="Bogotá", ignorar_mayusculas=False))

    def test_regex(self):
        self.assertTrue(v("regex", "Hola PARCE", patron="parce", flags="i"))
        self.assertFalse(v("regex", "Hola", patron="parce", flags="i"))
        self.assertTrue(v("no_regex", "Hola", patron="parce", flags="i"))
        self.assertFalse(v("no_regex", "Hola parce", patron="parce"))

    def test_contiene(self):
        self.assertTrue(v("contiene_todos", "El café y la sabana", valores=["cafe", "SABANA"]))
        self.assertFalse(v("contiene_todos", "El café", valores=["cafe", "sabana"]))
        self.assertTrue(v("contiene_alguno", "Medellín", valores=["Cali", "medellin"]))
        self.assertFalse(v("contiene_alguno", "Pasto", valores=["Cali", "medellin"]))
        self.assertTrue(v("no_contiene", "hola", valores=["chao"]))
        self.assertFalse(v("no_contiene", "Chao", valores=["chao"]))
        self.assertFalse(v("contiene_todos", "cafe", valores=["café"], ignorar_tildes=False))

    def test_palabras(self):
        self.assertTrue(v("palabras", "uno dos tres", min=3, max=3))
        self.assertFalse(v("palabras", "uno dos tres cuatro", max=3))
        self.assertFalse(v("palabras", "uno", min=2))
        self.assertTrue(v("palabras", "uno - dos", max=2))

    def test_lineas(self):
        self.assertTrue(v("lineas", "a\n\nb\nc", min=3, max=3))
        self.assertFalse(v("lineas", "a\n\nb\nc", min=5, no_vacias=False))
        self.assertFalse(v("lineas", "a\n\nb\nc", max=2))
        self.assertTrue(v("lineas", "a\n\nb", min=3, max=3, no_vacias=False))

    def test_vinetas(self):
        t = "- uno\n* dos\n• tres\n4. cuatro\n**negrita**"
        self.assertTrue(v("vinetas", t, exacto=4))
        self.assertFalse(v("vinetas", t, exacto=3))
        self.assertTrue(v("vinetas", t, min=2, max=5))

    def test_json(self):
        self.assertTrue(v("json", '{"a": 1, "b": 2}', claves=["a", "b"], tipo_raiz="objeto"))
        self.assertTrue(v("json", 'Aquí:\n```json\n{"a": 1}\n```', claves=["a"]))
        self.assertFalse(v("json", '{"a": 1}', claves=["a", "b"]))
        self.assertFalse(v("json", "no es json"))
        self.assertFalse(v("json", "[1, 2]", tipo_raiz="objeto"))
        self.assertTrue(v("json", "[1, 2]", tipo_raiz="lista"))

    def test_empieza_termina(self):
        self.assertTrue(v("empieza_con", "buenas tardes, señor", valor="Buenas tardes"))
        self.assertFalse(v("empieza_con", "Hola. Buenas tardes", valor="Buenas tardes"))
        self.assertTrue(v("termina_con", "Gracias.  \n", valor="gracias."))
        self.assertFalse(v("termina_con", "Gracias. Adiós", valor="Gracias."))

    def test_mayusculas(self):
        self.assertTrue(v("mayusculas", "HOLA, MUNDO 123", modo="todo"))
        self.assertFalse(v("mayusculas", "HOLA mundo", modo="todo"))
        self.assertTrue(v("mayusculas", "hola mundo", modo="nada"))
        self.assertFalse(v("mayusculas", "Hola mundo", modo="nada"))

    def test_idioma(self):
        self.assertTrue(v("idioma_es", "El café de la región es muy suave y se cultiva en las montañas"))
        self.assertFalse(v("idioma_es", "The coffee of the region is very soft and it is grown in the mountains"))

    def test_desconocido_y_vacio(self):
        self.assertFalse(v("inventado", "x"))
        self.assertEqual(verificar({"verificadores": []}, "x")[0], True)

    def test_detalle(self):
        ok, det = verificar({"verificadores": [{"tipo": "numero", "valor": 1},
                                               {"tipo": "palabras", "max": 1}]}, "1 2")
        self.assertFalse(ok)
        self.assertEqual([d["paso"] for d in det], [False, False])


class TestJuezParseo(unittest.TestCase):
    def test_parseo(self):
        self.assertIs(parsear("SI"), True)
        self.assertIs(parsear("Sí."), True)
        self.assertIs(parsear("**NO**"), False)
        self.assertIs(parsear("<think>x</think>no"), False)
        self.assertIs(parsear("Respuesta: SI"), True)
        self.assertIsNone(parsear("tal vez"))


if __name__ == "__main__":
    unittest.main()
