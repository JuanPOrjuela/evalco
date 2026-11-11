# EvalCO

**Banco de evaluación de modelos de lenguaje en español colombiano.**
150 casos diseñados uno por uno, calificación automática reproducible y resultados
de modelos abiertos corridos en local.

> *English summary below.*

## Por qué

Los bancos de evaluación más usados están en inglés. Dicen poco sobre si un
modelo calcula bien el IVA en pesos, entiende «me hicieron conejo», trata de
usted a un cliente cuando la política lo exige o reconoce que una ley, un
libro o un premio no existen. EvalCO mide eso con casos cortos y verificables.

## Qué mide

| Categoría | Casos | Qué evalúa |
|---|---|---|
| Instrucciones | 30 | Restricciones verificables y combinadas: número de palabras o viñetas, JSON válido, palabras prohibidas, mayúsculas, cierre exacto. |
| Razonamiento | 30 | Aritmética con pesos e IVA, nómina, fechas y días hábiles, horarios, lógica de orden y probabilidad. Respuesta única. |
| Colombianismos | 30 | Expresiones y contexto local (SOAT, Icetex, Ley Emiliani, «dar papaya», «puente»…). Opción múltiple balanceada A-D. |
| Soporte | 30 | Agente de atención de 6 empresas ficticias con una política en el mensaje de sistema: plazos, qué no puede prometer, cuándo escalar, trato de usted. |
| Alucinaciones | 30 | 24 premisas falsas (leyes, novelas, premios, teoremas y métodos de pandas inventados) y 6 controles con premisa verdadera, para que negarse siempre no sirva. |

Cada categoría tiene 10 casos de dificultad 1, 12 de dificultad 2 y 8 de dificultad 3.

## Cómo se califica

- **109 casos sin juez:** 16 tipos de verificador determinista (número con formato
  colombiano, opción, regex, JSON, conteo de palabras, líneas o viñetas, etc.).
  Un caso pasa si pasan todos sus verificadores.
- **41 casos con juez:** además de los verificadores, preguntas de sí/no objetivas
  (por ejemplo «¿La respuesta evita prometer un descuento en la factura?»). El juez
  solo se consulta si los verificadores ya pasaron.
- Intervalos de confianza de Wilson al 95 %.
- Control de calidad del dataset: cada caso tiene una respuesta modelo que pasa
  sus verificadores y 27 respuestas malas escritas a propósito que fallan;
  los 30 problemas de razonamiento se resolvieron de forma independiente por
  programa (fechas con `datetime`, acertijos por fuerza bruta).

## Resultados (11 de noviembre de 2026)

Ollama en una laptop con RTX 3070 Ti de 8 GB, temperatura 0, semilla 42.
qwen3 se corrió con el razonamiento desactivado (`think: false`).

| Modelo | Instrucciones | Razonamiento | Colombianismos | Soporte | Alucinaciones | **Total** |
|---|---|---|---|---|---|---|
| qwen3:8b | 70 % | 63 % | 77 % | 73 % | 67 % | **70 %** [62–77] |
| hermes3:8b | 63 % | 33 % | 70 % | 60 % | 73 % | **60 %** [52–67] |
| gemma3:4b | 63 % | 40 % | 63 % | 80 % | 23 % | **54 %** [46–62] |

Tabla completa con intervalos, desglose por dificultad y ejemplos de fallos:
[`resultados/resumen.md`](resultados/resumen.md) (o `resultados/index.html`).

<!-- MUESTRA_DEEPSEEK -->

### Hallazgos

1. **gemma3:4b inventa con total seguridad.** Solo rechazó 3 de las 24 premisas
   falsas: le atribuyó a García Márquez un «segundo Nobel en 1997», le dio tres
   Óscar a *El abrazo de la serpiente*, escribió el coro de una canción de Vives y
   Shakira que no existe y dio la dirección de un instituto inventado en Leticia.
   Aun así fue el mejor en soporte (80 %): sigue bien una política escrita, pero
   no sabe decir «no sé».
2. **hermes3:8b es el más prudente, pero no sabe hacer cuentas.** Rechazó 17 de 24
   premisas falsas, la mejor marca, y solo acertó 10 de 30 problemas de
   razonamiento (por ejemplo, unos zapatos de $200.000 con 20 % de descuento y
   otro 10 % por pago en efectivo le dieron $176.000 en vez de $144.000).
3. **qwen3:8b es el más parejo.** No bajó del 63 % en ninguna categoría y acertó
   los 6 controles de premisa verdadera, así que su prudencia no es negarse a todo.
4. **Los colombianismos no son un problema resuelto.** Ningún modelo pasó del 77 %.
   Los errores típicos confunden el sentido literal con el coloquial (qwen3 eligió
   «Que el tendero le obsequie el pan» para «¿me regala dos mil de pan?»).
5. **El formato pesa.** Varios fallos de razonamiento son respuestas correctas con el
   formato equivocado (qwen3 respondió 5/14 en LaTeX cuando se pedía `a/b`). Se
   cuentan como fallo a propósito: en un sistema real, quien consume la salida
   espera el formato pedido.

### ¿Se puede confiar en el juez?

El juez local (qwen3:8b) respondió 132 preguntas de rúbrica. Un segundo juez
independiente (Claude Haiku, que no vio los veredictos del primero) respondió
las mismas:

- **Acuerdo: 122 de 132 (92 %), kappa de Cohen = 0,82** (acuerdo casi perfecto).
- En 9 de los 10 desacuerdos el juez local fue más generoso. Por ejemplo, aceptó que
  qwen3 negara que Rodolfo Llinás ganó el Nobel de Física aunque en la misma
  respuesta afirmara que ganó el de Medicina en 2009.
- Con los veredictos del segundo juez, los totales cambian como mucho 3 puntos
  (gemma3 51 %, hermes3 59 %, qwen3 69 %) y el orden de los modelos no cambia.
  El juez local no favoreció de forma visible a su propio modelo: con qwen3
  solo hubo 1 desacuerdo de 45.

Detalle en `resultados/validacion_juez/`. Además, `resultados/revision_humana.csv`
trae 30 calificaciones al azar (3 aprobadas y 3 falladas por categoría) para
revisión humana.

## Limitaciones

- 30 casos por categoría dan intervalos anchos (±15 puntos): sirven para ver
  diferencias grandes, no para ordenar modelos parecidos.
- El juez local (qwen3:8b) también compite. Se validó contra un segundo juez
  (kappa 0,82), pero la revisión humana de la muestra todavía está pendiente.
- Los casos los escribió y revisó una sola persona con apoyo de asistentes de IA;
  el español «colombiano» aquí es sobre todo el de Bogotá y el uso más extendido.
- Algunas referencias envejecen (por ejemplo, el metro de Bogotá).

## Cómo correrlo

Requiere Python 3.10+ (solo biblioteca estándar) y [Ollama](https://ollama.com).

```bash
ollama pull qwen3:8b
python -m evalco.correr --modelos qwen3:8b --think-off --salida resultados/
python -m evalco.calificar resultados/ --juez qwen3:8b
python -m evalco.reporte resultados/
python -m unittest discover -s tests
```

`correr` reanuda donde quedó si se interrumpe. `--ids datos/muestra50.txt` corre
solo la muestra estratificada de 50 casos y `--timeout` sube el tiempo por respuesta.

El dataset está en `datos/casos.jsonl` y se genera desde `fuentes/`
(`python fuentes/build.py`, que también lo valida). El formato está en `SPEC.md`.

## Estructura

```
datos/        casos.jsonl (150 casos), muestra50.txt, ejemplo.jsonl
fuentes/      generador y validador del dataset
evalco/       cliente de Ollama, verificadores, juez, calificación y reporte
resultados/   respuestas, calificaciones, resumen.md, index.html, revisión humana
tests/        pruebas de los verificadores y del reporte
```

---

## English summary

EvalCO is a 150-item benchmark for LLMs in **Colombian Spanish**, covering
instruction following, everyday reasoning (COP prices, 19 % VAT, dates),
Colombian slang and local context, customer-support policy compliance and
hallucination resistance (24 false premises plus 6 true-premise controls).
73 % of items are graded by deterministic checkers; the rest add binary rubric
questions answered by an LLM judge. On a local RTX 3070 Ti, qwen3:8b scored 70 %,
hermes3:8b 60 % and gemma3:4b 54 %. gemma3:4b accepted 21 of 24 false premises
with confident fabrications, while hermes3:8b was the most cautious but failed
two thirds of the arithmetic items. Standard-library Python only; runs against
any Ollama model.

Autor: Juan Pablo Orjuela Rojas — Universidad Sergio Arboleda, Bogotá.
