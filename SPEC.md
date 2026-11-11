# EvalCO — especificación

Banco de evaluación de modelos de lenguaje en **español colombiano**. Mide cinco
habilidades con casos escritos a mano, la mayoría calificados por reglas
deterministas (sin juez) y el resto por un juez con rúbrica binaria. Corre contra
modelos locales de Ollama (gratis, reproducible) y produce una tabla comparativa,
un análisis de errores y una página estática de resultados.

## Categorías (30 casos cada una, 150 en total)

| Clave | Qué mide |
|---|---|
| `instrucciones` | Seguir restricciones verificables: formato, número de palabras o viñetas, idioma, JSON válido, palabras prohibidas u obligatorias, mayúsculas, orden. |
| `razonamiento` | Aritmética, lógica, fechas, unidades y problemas cotidianos colombianos (pesos COP, IVA 19 %, TransMilenio, horarios). Respuesta única verificable. |
| `colombianismos` | Comprensión de jerga y expresiones de Colombia (parce, bacano, camellar, dar papaya, echar los perros, etc.) y de contexto local (instituciones, festivos, regiones). Formato de opción múltiple A-D. |
| `soporte` | Respuestas de atención al cliente en español colombiano: cortesía, seguir la política dada en el mensaje de sistema, no inventar datos, escalar cuando corresponde. |
| `alucinaciones` | Premisas falsas o entidades inexistentes (leyes, libros, eventos, personas inventadas). El modelo debe señalar que no existe o que no tiene el dato, en vez de inventar. |

Dificultad 1-3 repartida más o menos 10/12/8 por categoría.

## Formato del dataset: `datos/casos.jsonl`

Un objeto JSON por línea, UTF-8:

```json
{
  "id": "raz-007",
  "categoria": "razonamiento",
  "dificultad": 2,
  "sistema": null,
  "prompt": "Un almuerzo cuesta $18.500 antes de IVA (19 %). ¿Cuánto se paga en total? Responde solo el número entero en pesos, sin puntos ni signos.",
  "verificadores": [
    {"tipo": "numero", "valor": 22015, "tolerancia": 0}
  ],
  "rubrica": null,
  "referencia": "18500 × 1,19 = 22015",
  "nota": "Por qué el caso es interesante o qué error típico detecta."
}
```

- `sistema`: mensaje de sistema opcional (string o null). Los casos de `soporte` lo usan para la política de la empresa ficticia.
- `verificadores`: lista; el caso PASA si TODOS pasan. Puede estar vacía solo si hay `rubrica`.
- `rubrica`: lista de preguntas de sí/no para el juez (todas deben ser "sí" para pasar), o null.
- Un caso puede tener verificadores Y rúbrica (pasa si ambos pasan).
- `referencia`: respuesta modelo o justificación (para humanos y para el juez).

### Tipos de verificador

Todos operan sobre la respuesta del modelo después de quitar bloques `<think>...</think>` y espacios en los extremos.

| tipo | parámetros | pasa si |
|---|---|---|
| `exacto` | `valor` (str), `ignorar_mayusculas` (bool, def. true) | la respuesta, sin puntuación final, es igual a `valor` |
| `numero` | `valor` (num), `tolerancia` (num, def. 0) | el ÚLTIMO número de la respuesta (acepta `22.015`, `22,015`, `22015`, `$22.015`, decimales con coma o punto; ver nota) está a ≤ tolerancia de `valor` |
| `opcion` | `valor` ("A"-"D") | la primera letra A-D que aparece sola (como `A`, `A)`, `(A)`, `A.`, `Respuesta: A`) es `valor` |
| `regex` | `patron`, `flags` (str opcional: "i", "s", "m") | `re.search` encuentra el patrón |
| `no_regex` | `patron`, `flags` | NO lo encuentra |
| `contiene_todos` | `valores` (lista), `ignorar_mayusculas` (def. true), `ignorar_tildes` (def. true) | aparecen todos |
| `contiene_alguno` | `valores`, igual | aparece al menos uno |
| `no_contiene` | `valores`, igual | no aparece ninguno |
| `palabras` | `min` (opcional), `max` (opcional) | el conteo de palabras está en el rango |
| `lineas` | `min`, `max`, `no_vacias` (def. true) | número de líneas en el rango |
| `vinetas` | `exacto` o `min`/`max` | número de líneas que empiezan con `-`, `*`, `•` o `N.` |
| `json` | `claves` (lista opcional), `tipo_raiz` ("objeto"/"lista", opcional) | la respuesta (o el primer bloque ```json```) es JSON válido y tiene esas claves |
| `empieza_con` | `valor`, `ignorar_mayusculas` | la respuesta empieza con `valor` |
| `termina_con` | `valor`, `ignorar_mayusculas` | termina con `valor` (ignorando espacios finales) |
| `mayusculas` | `modo`: "todo" / "nada" | todas las letras son mayúsculas / no hay ninguna mayúscula |
| `idioma_es` | — | heurística: proporción de palabras funcionales del español > inglés |

Nota sobre números: en Colombia el punto separa miles y la coma decimales. El
extractor debe tratar `22.015` como 22015 cuando hay exactamente 3 dígitos tras
el punto y el valor esperado es entero; en los casos, PEDIR siempre "solo el
número entero, sin puntos ni signos" o "con dos decimales usando punto" para
evitar ambigüedad.

## Juez

- Para `rubrica`, un modelo juez recibe: prompt original, sistema, referencia,
  respuesta del modelo y UNA pregunta de la rúbrica; debe contestar `SI` o `NO`.
- Juez por defecto: configurable (`--juez qwen3:8b`). Se reporta que el juez
  también compite (sesgo) y se valida con una muestra revisada a mano
  (`resultados/revision_humana.csv`).
- Meta: ≥ 70 % de los casos sin juez (solo verificadores).

## Ejecución

```
python -m evalco.correr --modelos qwen3:8b deepseek-r1:8b hermes3:8b --salida resultados/
python -m evalco.calificar resultados/
python -m evalco.reporte resultados/   # genera resultados/index.html y resumen.md
```

- Cliente: API HTTP de Ollama (`http://localhost:11434/api/chat`), temperatura 0,
  `seed` fijo, `num_ctx` 4096, sin streaming. Para qwen3, `think: false` opcional
  (se reporta). Timeout por caso 180 s.
- Guarda una línea por (modelo, caso) en `resultados/respuestas.jsonl` con
  respuesta cruda, tiempo y tokens; reanuda si se corta (salta lo ya hecho).
- Solo biblioteca estándar de Python 3.13 (urllib, json, re, unicodedata). Nada de pip.
- Pruebas con `python -m unittest` en `tests/` para cada verificador.

## Reporte

- `resultados/resumen.md` y `resultados/index.html` (una sola página, sin
  dependencias externas, sobria: blanco/negro/gris, tipografía del sistema,
  tablas simples, nada de degradados ni tarjetas de colores).
- Tabla modelo × categoría (% de aciertos con intervalo de Wilson 95 %),
  tiempo medio por respuesta y ejemplos de errores típicos por categoría.
