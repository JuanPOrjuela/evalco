# -*- coding: utf-8 -*-
"""Genera informe/EvalCO_informe.html y el PDF a partir de resultados/.

Uso: python informe/generar.py
"""
import collections
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
from evalco.reporte import wilson  # noqa: E402

CATS = ["instrucciones", "razonamiento", "colombianismos", "soporte", "alucinaciones"]
NOMBRES = {"instrucciones": "Instrucciones", "razonamiento": "Razonamiento",
           "colombianismos": "Colombianismos", "soporte": "Soporte",
           "alucinaciones": "Alucinaciones"}
COMPLETOS = ["qwen3:8b", "hermes3:8b", "gemma3:4b"]
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def leer(ruta):
    with open(os.path.join(RAIZ, ruta), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def pct(k, n):
    return f"{100 * k / n:.0f}" if n else "—"


def celda_ic(k, n):
    lo, hi = wilson(k, n)
    return f"{pct(k, n)} <span class='ic'>[{100 * lo:.0f}–{100 * hi:.0f}]</span>"


def datos():
    cals = leer("resultados/calificaciones.jsonl")
    resp = {}
    for r in leer("resultados/respuestas.jsonl"):
        resp[(r["modelo"], r["id"])] = r
    muestra = set(open(os.path.join(RAIZ, "datos/muestra50.txt"), encoding="utf-8").read().split())
    t = collections.defaultdict(lambda: [0, 0])
    for c in cals:
        m = c["modelo"]
        if m in COMPLETOS:
            for clave in [(m, c["categoria"]), (m, "total"), (m, "d%d" % c["dificultad"])]:
                t[clave][0] += c["paso"]
                t[clave][1] += 1
        if c["id"] in muestra:
            for clave in [("m", m, c["categoria"]), ("m", m, "total")]:
                t[clave][0] += c["paso"]
                t[clave][1] += 1
    tiempos = {}
    for m in set(r[0] for r in resp):
        ts = [r.get("segundos") for (mm, i), r in resp.items() if mm == m and i in muestra and r.get("segundos")]
        tiempos[m] = sum(ts) / len(ts) if ts else None
    ds_n = t[("m", "deepseek-r1:8b", "total")][1]
    return t, tiempos, ds_n


def tabla_principal(t):
    filas = []
    for m in COMPLETOS:
        celdas = "".join(f"<td>{celda_ic(*t[(m, c)])}</td>" for c in CATS)
        filas.append(f"<tr><td>{m}</td>{celdas}<td><b>{celda_ic(*t[(m, 'total')])}</b></td></tr>")
    cab = "".join(f"<th>{NOMBRES[c]}</th>" for c in CATS)
    return (f"<table><thead><tr><th>Modelo</th>{cab}<th>Total</th></tr></thead>"
            f"<tbody>{''.join(filas)}</tbody></table>")


def tabla_dificultad(t):
    filas = []
    for m in COMPLETOS:
        celdas = "".join(f"<td>{celda_ic(*t[(m, 'd%d' % d)])}</td>" for d in (1, 2, 3))
        filas.append(f"<tr><td>{m}</td>{celdas}</tr>")
    return ("<table><thead><tr><th>Modelo</th><th>Dificultad 1 (n = 50)</th><th>Dificultad 2 (n = 60)</th>"
            f"<th>Dificultad 3 (n = 40)</th></tr></thead><tbody>{''.join(filas)}</tbody></table>")


def tabla_muestra(t, tiempos):
    mods = [m for m in COMPLETOS + ["deepseek-r1:8b"] if t[("m", m, "total")][1] == 50]
    filas = []
    for m in mods:
        celdas = "".join(f"<td>{pct(*t[('m', m, c)])}</td>" for c in CATS)
        tt = tiempos.get(m)
        filas.append(f"<tr><td>{m}</td>{celdas}<td><b>{pct(*t[('m', m, 'total')])}</b></td>"
                     f"<td>{'—' if tt is None else f'{tt:.0f}'}</td></tr>")
    cab = "".join(f"<th>{NOMBRES[c]}</th>" for c in CATS)
    return (f"<table><thead><tr><th>Modelo</th>{cab}<th>Total</th><th>s/resp.</th></tr></thead>"
            f"<tbody>{''.join(filas)}</tbody></table>"), mods


CSS = """
@page { size: A4; margin: 24mm 22mm 22mm; }
body { font-family: Cambria, Georgia, "Times New Roman", serif; font-size: 10.5pt; line-height: 1.5; color: #111; margin: 0; }
h1 { font-size: 20pt; font-weight: normal; margin: 0 0 4pt; letter-spacing: -0.01em; }
.autor { color: #444; margin: 0 0 18pt; }
h2 { font-size: 12pt; font-weight: bold; margin: 18pt 0 6pt; page-break-after: avoid; }
h3 { font-size: 10.5pt; font-style: italic; font-weight: normal; margin: 12pt 0 4pt; page-break-after: avoid; }
p { margin: 0 0 7pt; text-align: justify; hyphens: auto; }
.resumen { border-top: 0.6pt solid #111; border-bottom: 0.6pt solid #111; padding: 8pt 0; margin-bottom: 14pt; }
.resumen p { margin: 0; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0 4pt; font-size: 9pt; page-break-inside: avoid;
        font-variant-numeric: tabular-nums; }
thead th { border-top: 0.9pt solid #111; border-bottom: 0.5pt solid #111; font-weight: normal; text-align: right; padding: 4pt 5pt; }
tbody td { padding: 3pt 5pt; text-align: right; }
tbody tr:last-child td { border-bottom: 0.9pt solid #111; }
th:first-child, td:first-child { text-align: left; }
.ic { color: #666; font-size: 7.5pt; }
.pie { font-size: 8.5pt; color: #444; margin: 2pt 0 10pt; text-align: left; }
ul, ol { margin: 0 0 7pt; padding-left: 16pt; } li { margin: 0 0 3pt; }
code { font-family: Consolas, "Courier New", monospace; font-size: 9pt; }
blockquote { margin: 4pt 0 8pt 14pt; color: #333; font-size: 9.5pt; }
"""


def html(t, tiempos, ds_n):
    tm, mods_m = tabla_muestra(t, tiempos)
    ds = ""
    if "deepseek-r1:8b" in mods_m:
        q = t[("m", "qwen3:8b", "total")][0]
        d = t[("m", "deepseek-r1:8b", "total")][0]
        ds = (f"<p>deepseek-r1:8b razona por escrito antes de responder. En la muestra acertó {d} de 50 "
              f"casos, contra {q} de qwen3 sin razonamiento, con un tiempo medio de "
              f"{tiempos['deepseek-r1:8b']:.0f} s por respuesta frente a {tiempos['qwen3:8b']:.0f} s. "
              "Con 50 casos los intervalos son de unos ±13 puntos, así que la comparación es orientativa.</p>")
    else:
        ds = (f"<p>deepseek-r1:8b, que razona por escrito antes de responder, tardó varios minutos por caso "
              f"en esta GPU; al cierre de este informe llevaba {ds_n} de los 50 casos de la muestra, así que "
              "no se reporta su puntaje.</p>")
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>EvalCO: evaluación de modelos de lenguaje en español colombiano</title><style>{CSS}</style></head><body>
<h1>EvalCO: evaluación de modelos de lenguaje en español colombiano</h1>
<p class="autor">Juan Pablo Orjuela Rojas · Ciencias de la Computación e Inteligencia Artificial,
Universidad Sergio Arboleda · noviembre de 2026</p>

<div class="resumen"><p><b>Resumen.</b> Presento EvalCO, un banco de 150 casos para medir modelos de
lenguaje en tareas propias del español colombiano: seguir instrucciones verificables, razonar con pesos,
IVA y fechas, entender colombianismos, atender clientes bajo una política escrita y resistir premisas
falsas. El 73 % de los casos se califica con verificadores deterministas y el resto añade preguntas de
sí/no para un juez. Tres modelos abiertos corridos en local obtuvieron entre 54 % y 70 %. El hallazgo
principal es que el rendimiento no es parejo: el modelo más pequeño fue el mejor siguiendo políticas de
soporte y el peor ante premisas falsas, donde aceptó 21 de 24 con datos inventados. Un segundo juez
independiente coincidió con el primero en el 92 % de las preguntas (kappa = 0,82).</p></div>

<h2>1. Motivación</h2>
<p>Los bancos de evaluación más citados están en inglés. Sirven poco para decidir si un modelo puede
atender clientes en Colombia: ahí importa que calcule bien un descuento en pesos, que entienda
«me hicieron conejo», que trate de usted cuando la empresa lo exige y que diga «no sé» cuando le
preguntan por una ley que no existe. EvalCO busca medir esas habilidades con casos cortos, revisables
por una persona y calificables sin intervención manual.</p>

<h2>2. Diseño del banco</h2>
<p>Hay 30 casos por categoría (10 de dificultad 1, 12 de dificultad 2 y 8 de dificultad 3):</p>
<ul>
<li><b>Instrucciones:</b> dos a cuatro restricciones simultáneas y verificables (número exacto de palabras,
viñetas, JSON con claves fijas, palabras prohibidas, cierre exacto).</li>
<li><b>Razonamiento:</b> problemas cotidianos con respuesta única: propinas, descuentos encadenados, 4×1000,
nómina, días hábiles, Ley Emiliani, husos horarios, acertijos de orden y probabilidad.</li>
<li><b>Colombianismos:</b> opción múltiple con cuatro opciones plausibles y la respuesta correcta
balanceada entre A y D.</li>
<li><b>Soporte:</b> seis empresas ficticias, cada una con su política en el mensaje de sistema (plazos,
promesas prohibidas, cuándo escalar, trato de usted, máximo de palabras).</li>
<li><b>Alucinaciones:</b> 24 premisas falsas (una novela inexistente de García Márquez, un teorema
inventado, un método de pandas que no existe, un artículo 412 de la Constitución) y 6 controles con
premisa verdadera, para que negarse a todo no sea una estrategia ganadora.</li>
</ul>
<p>La calificación usa 16 tipos de verificador: extracción del último número con formato colombiano
(punto de miles, coma decimal), opción A-D, expresiones regulares, JSON, conteo de palabras, líneas y
viñetas, mayúsculas e idioma. Un caso pasa si pasan todos sus verificadores. En 41 casos se agregan
preguntas de sí/no para un juez, que solo se consulta si los verificadores ya pasaron.</p>
<p>Control de calidad: cada caso trae una respuesta modelo que pasa sus verificadores, y se escribieron
27 respuestas incorrectas a propósito para comprobar que fallan. Los 30 problemas de razonamiento se
resolvieron dos veces de forma independiente, con programas (fechas con <code>datetime</code>, acertijos
por fuerza bruta). Una revisión independiente del dataset encontró cuatro verificadores demasiado
permisivos y dos opciones ambiguas, que se corrigieron antes de calificar.</p>

<h2>3. Metodología</h2>
<p>Los modelos se corrieron con Ollama en una laptop con GPU RTX 3070 Ti de 8 GB, con temperatura 0,
semilla 42 y contexto de 4.096 tokens. qwen3:8b se corrió con el razonamiento desactivado. Los modelos
completos son qwen3:8b, hermes3:8b y gemma3:4b. El juez fue qwen3:8b, que también compite; por eso su
criterio se validó con un segundo juez (sección 6). Los intervalos son de Wilson al 95 %.</p>

<h2>4. Resultados</h2>
{tabla_principal(t)}
<p class="pie">Tabla 1. Porcentaje de casos aprobados por categoría (n = 30) y total (n = 150), con el
intervalo de Wilson al 95 % entre corchetes.</p>
{tabla_dificultad(t)}
<p class="pie">Tabla 2. Aciertos por nivel de dificultad. Los tres modelos bajan de forma monótona, lo
que indica que la escala de dificultad funciona.</p>

<h3>Muestra estratificada</h3>
<p>Para incluir un modelo de razonamiento sin correr los 150 casos se tomó una muestra de 50 (10 por
categoría, elegidos al azar con semilla fija).</p>
{tm}
<p class="pie">Tabla 3. Aciertos en la muestra de 50 casos y tiempo medio por respuesta en segundos.</p>
{ds}

<h2>5. Análisis de errores</h2>
<h3>Premisas falsas</h3>
<p>gemma3:4b solo rechazó 3 de las 24 premisas falsas. Ante la pregunta por el «segundo discurso del Nobel
de 1997» de García Márquez, lo aceptó y describió el discurso; le atribuyó tres Óscar a <i>El abrazo de la
serpiente</i>, escribió el coro de una canción de Carlos Vives y Shakira que no existe y dio dirección y
director de un instituto inventado en Leticia. hermes3:8b rechazó 17 de 24, la mejor marca, y qwen3:8b 14,
aunque acertó los 6 controles. Que gemma3 haya sido a la vez el mejor en soporte (80 %) muestra que seguir
bien una política escrita y reconocer lo que no se sabe son habilidades distintas.</p>
<h3>Razonamiento</h3>
<p>hermes3:8b acertó 10 de 30. Sus errores son de cálculo, no de formato: para unos zapatos de $200.000 con
20 % de descuento y otro 10 % por pago en efectivo respondió $176.000 en vez de $144.000, y dijo que el 7 de
agosto de 2026 cae lunes cuando cae viernes. En qwen3 hay errores de lógica (en una fila de cinco personas
puso a Carla en la posición 3, lo que viola una de las condiciones) y fallos de formato: respondió
<code>\\frac{{5}}{{14}}</code> cuando se pedía <code>a/b</code>. Se cuentan como fallo a propósito, porque en un
sistema real quien consume la salida espera el formato pedido.</p>
<h3>Soporte y colombianismos</h3>
<p>El error de soporte más grave fue de qwen3: a un paciente que preguntó si tomar ibuprofeno o amoxicilina,
le dijo que podía tomar ibuprofeno, aunque la política de la clínica prohíbe recomendar medicamentos. En
colombianismos ningún modelo pasó del 77 %; los errores tienden a elegir el sentido literal, como «que el
tendero le obsequie el pan» para «¿me regala dos mil de pan?».</p>
<h3>Instrucciones</h3>
<p>Los conteos exactos siguen siendo difíciles: pedida una oración de exactamente 12 palabras, qwen3 escribió
una de 14. Las restricciones combinadas (rango de palabras más cierre exacto más palabra prohibida) separan
mejor a los modelos que cualquiera de ellas por separado.</p>

<h2>6. Validación del juez</h2>
<p>Las 132 preguntas de rúbrica respondidas por el juez local se dieron también a un segundo juez (Claude
Haiku), que no vio los veredictos del primero. Coincidieron en 122 (92 %), con kappa de Cohen de 0,82. En 9
de los 10 desacuerdos el juez local fue más generoso; por ejemplo, aceptó que una respuesta negara el Nobel
de Física de Rodolfo Llinás aunque en la misma respuesta le atribuía el de Medicina. Con los veredictos del
segundo juez los totales cambian como mucho 3 puntos (51 %, 59 % y 69 %) y el orden de los modelos se
mantiene. Además, se preparó una muestra de 30 calificaciones al azar para revisión humana.</p>

<h2>7. Limitaciones y trabajo futuro</h2>
<ul>
<li>Con 30 casos por categoría los intervalos son de unos ±15 puntos: el banco distingue diferencias grandes,
no ordena modelos parecidos.</li>
<li>El español representado es sobre todo el de Bogotá y el uso más extendido; faltan variantes regionales.</li>
<li>Los casos se diseñaron con apoyo de asistentes de IA y se revisaron con un segundo modelo y por
programa; la revisión humana de la muestra es el siguiente paso.</li>
<li>Algunas referencias envejecen (por ejemplo, el estado del metro de Bogotá).</li>
<li>Siguientes pasos: ampliar a 300 casos, agregar modelos comerciales por API y medir el efecto de activar
el razonamiento en el mismo modelo.</li>
</ul>
<p>Código, datos y resultados: <code>github.com/JuanPOrjuela/evalco</code>.</p>
</body></html>"""


def main():
    t, tiempos, ds_n = datos()
    ruta_html = os.path.join(RAIZ, "informe", "EvalCO_informe.html")
    with open(ruta_html, "w", encoding="utf-8") as f:
        f.write(html(t, tiempos, ds_n))
    ruta_tmp = os.path.join(RAIZ, "informe", "_tmp.pdf")
    ruta_pdf = os.path.join(RAIZ, "informe", "EvalCO_informe.pdf")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={ruta_tmp}", "file:///" + ruta_html.replace("\\", "/")],
                   check=True, capture_output=True)
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter(clone_from=PdfReader(ruta_tmp))
    w.metadata = {"/Title": "EvalCO: evaluación de modelos de lenguaje en español colombiano",
                  "/Author": "Juan Pablo Orjuela Rojas", "/Creator": "Juan Pablo Orjuela Rojas",
                  "/Producer": "Juan Pablo Orjuela Rojas"}
    with open(ruta_pdf, "wb") as f:
        w.write(f)
    os.remove(ruta_tmp)
    print("escrito", ruta_pdf, "páginas:", len(PdfReader(ruta_pdf).pages))


if __name__ == "__main__":
    main()
