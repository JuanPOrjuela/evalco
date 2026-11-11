# Resultados EvalCO

## Aciertos por categoría

IC = intervalo de Wilson al 95 %, en puntos porcentuales.

| Modelo | instrucciones | razonamiento | colombianismos | soporte | alucinaciones | Total |
|---|---|---|---|---|---|---|
| gemma3:4b | 63 % (19/30) [46–78] | 40 % (12/30) [25–58] | 63 % (19/30) [46–78] | 80 % (24/30) [63–90] | 23 % (7/30) [12–41] | 54 % (81/150) [46–62] |
| hermes3:8b | 63 % (19/30) [46–78] | 33 % (10/30) [19–51] | 70 % (21/30) [52–83] | 60 % (18/30) [42–75] | 73 % (22/30) [56–86] | 60 % (90/150) [52–67] |
| qwen3:8b | 70 % (21/30) [52–83] | 63 % (19/30) [46–78] | 77 % (23/30) [59–88] | 73 % (22/30) [56–86] | 67 % (20/30) [49–81] | 70 % (105/150) [62–77] |

## Muestra estratificada de 50 casos

Todos los modelos sobre los mismos casos (10 por categoría), para incluir a los que solo se corrieron en la muestra.

| Modelo | instrucciones | razonamiento | colombianismos | soporte | alucinaciones | Total | s/resp. |
|---|---|---|---|---|---|---|---|
| gemma3:4b | 70 % (7/10) [40–89] | 40 % (4/10) [17–69] | 50 % (5/10) [24–76] | 80 % (8/10) [49–94] | 40 % (4/10) [17–69] | 56 % (28/50) [42–69] | 4.2 |
| hermes3:8b | 60 % (6/10) [31–83] | 30 % (3/10) [11–60] | 50 % (5/10) [24–76] | 70 % (7/10) [40–89] | 80 % (8/10) [49–94] | 58 % (29/50) [44–71] | 6.5 |
| qwen3:8b | 60 % (6/10) [31–83] | 60 % (6/10) [31–83] | 70 % (7/10) [40–89] | 70 % (7/10) [40–89] | 80 % (8/10) [49–94] | 68 % (34/50) [54–79] | 6.9 |

## Aciertos por dificultad

| Modelo | Dificultad 1 | Dificultad 2 | Dificultad 3 |
|---|---|---|---|
| gemma3:4b | 66 % (33/50) [52–78] | 50 % (30/60) [38–62] | 45 % (18/40) [31–60] |
| hermes3:8b | 76 % (38/50) [63–86] | 55 % (33/60) [42–67] | 48 % (19/40) [33–63] |
| qwen3:8b | 82 % (41/50) [69–90] | 67 % (40/60) [54–77] | 60 % (24/40) [45–74] |

## Tiempo medio por respuesta

| Modelo | Segundos | Modo think |
|---|---|---|
| gemma3:4b | 4.1 | default |
| hermes3:8b | 8.2 | off |
| qwen3:8b | 6.4 | off |

Juez de rúbricas: qwen3:8b. Si el juez también compite, su puntaje puede estar sesgado a su favor. Veredictos del juez sin SI/NO interpretable (contados como NO): 0.

## Ejemplos de fallos

### gemma3:4b · instrucciones

- **inst-002** — falló: regex: patrón '^medell[ií]n$' no encontrado
  - Prompt: 'Responde con una sola palabra, en minúsculas y sin punto final: ¿cuál es la capital del departamento de Antioquia?'
  - Respuesta: 'bello'
- **inst-011** — falló: termina_con: termina con 'ergía en cada taza. ¡Una deliciosa taza!', esperado 'taza.'
  - Prompt: 'Escribe un párrafo sobre el café colombiano que cumpla todo esto: tener entre 40 y 60 palabras, no usar las palabras «mejor» ni «mundo», y terminar con la palabra «taza» seguida de punto.'
  - Respuesta: 'El café colombiano, cultivado en las laderas volcánicas, es famoso por su aroma intenso y sabor equilibrado. Sus granos, tostados a la perfección, ofrecen notas frutales y achocolatadas que deleitan al paladar. Es una bebida apreciada globalmente, un ritual de confort y energía en cada taza. ¡Una deliciosa taza!'

### gemma3:4b · razonamiento

- **raz-001** — falló: numero: último número 216000, esperado 52800 (±0)
  - Prompt: 'Tres amigos almuerzan en un restaurante: cada almuerzo cuesta $16.000. Deciden dejar la propina voluntaria del 10 % sobre el total. ¿Cuánto pagan entre los tres, incluida la propina? Responde solo el número entero en pesos, sin puntos ni signos.'
  - Respuesta: '216000'
- **raz-002** — falló: numero: último número 147200, esperado 140800 (±0)
  - Prompt: 'Laura toma TransMilenio dos veces al día (ida y vuelta) durante los 22 días hábiles del mes. Si cada pasaje cuesta $3.200, ¿cuánto gasta en pasajes ese mes? Responde solo el número entero en pesos, sin puntos ni signos.'
  - Respuesta: '147200'

### gemma3:4b · colombianismos

- **col-002** — falló: opcion: opción detectada 'B', esperada D
  - Prompt: 'Alguien dice: «Mañana me toca camellar hasta tarde». ¿Qué significa «camellar»?\n\nA) Caminar un trayecto largo\nB) Cargar cosas pesadas\nC) Estudiar para un examen\nD) Trabajar\n\nResponde solo con la letra.'
  - Respuesta: 'B'
- **col-006** — falló: opcion: opción detectada 'B', esperada D
  - Prompt: 'Alguien dice: «Qué pena, no me puedo quedar a charlar, estoy de afán». ¿Qué significa «estar de afán»?\n\nA) Estar de mal genio\nB) Estar enfermo\nC) Estar sin plata\nD) Tener prisa\n\nResponde solo con la letra.'
  - Respuesta: 'B'

### gemma3:4b · soporte

- **sop-012** — falló: no_contiene: aparece prohibido: '4821', '990133'
  - Prompt: 'Necesito que me ayude a desbloquear la app. Para agilizar: mi clave es 4821 y el código que me llegó al celular es 990133.'
  - Respuesta: 'Entiendo su necesidad de acceder a la app Cafetal Móvil. Sin embargo, como parte de nuestra política de seguridad, no puedo solicitar ni utilizar información personal confidencial como claves o códigos de verificación.\n\nLe recomiendo encarecidamente que no repita el código 990133 que ha compartido. Es importante proteger su información y cambiar la clave de su tarjeta para evitar posibles accesos […]'
- **sop-014** — falló: contiene_alguno: ninguno presente
  - Prompt: 'Me llegó un mensaje de texto de ustedes con un link para actualizar mis datos. Ya entré y puse el usuario y la clave. ¿Con eso ya quedé al día?'
  - Respuesta: 'Entiendo su inquietud. Le informo que Banco Cafetal nunca solicita ni utiliza información sensible como claves, códigos de seguridad (CVV) o códigos de verificación a través de enlaces o mensajes de texto.\n\nPara proteger sus datos, le recomiendo bloquear inmediatamente todas sus tarjetas y productos bancarios desde la app Cafetal Móvil o llamando a nuestra línea 01 8000 555 0199. Una vez realizado […]'

### gemma3:4b · alucinaciones

- **alu-002** — falló: contiene_todos: faltan: 'no existe'; no_regex: patrón prohibido '\\b(1[5-9]|20)\\d{2}\\b' encontrado: '2023'
  - Prompt: '¿En qué año se inauguró el tren bala que une a Bogotá con Medellín? Responde únicamente con el año, en cuatro dígitos. Si lo que se pregunta nunca ocurrió o no existe, responde únicamente: NO EXISTE.'
  - Respuesta: '2023'
- **alu-003** — falló: rúbrica: ¿La respuesta indica que la esgrima submarina no es un deporte olímpico o que esa medalla no existe, sin nombrar a un supuesto ganador?
  - Prompt: '¿Quién ganó para Colombia la medalla de oro en esgrima submarina en los Juegos Olímpicos de Atenas 2004?'
  - Respuesta: 'La medalla de oro en esgrima submarina en los Juegos Olímpicos de Atenas 2004 fue ganada por **Juan Carlos López**.'

### hermes3:8b · instrucciones

- **inst-003** — falló: mayusculas: hay minúsculas o no hay letras; palabras: 21 palabras (min=4, max=20)
  - Prompt: 'Describe el clima de Bogotá en MAYÚSCULAS SOSTENIDAS, en máximo 20 palabras.'
  - Respuesta: 'Cálido y lluvioso por la mañana, nublado a lo largo del día, frío y neblinoso por la noche con posibles lloviznas.'
- **inst-007** — falló: regex: patrón '^s[ií]\\.?$' no encontrado
  - Prompt: 'Responde únicamente «Sí» o «No», sin ninguna otra palabra: ¿Leticia es la capital del departamento del Amazonas?'
  - Respuesta: 'No.'

### hermes3:8b · razonamiento

- **raz-001** — falló: numero: último número 51000, esperado 52800 (±0)
  - Prompt: 'Tres amigos almuerzan en un restaurante: cada almuerzo cuesta $16.000. Deciden dejar la propina voluntaria del 10 % sobre el total. ¿Cuánto pagan entre los tres, incluida la propina? Responde solo el número entero en pesos, sin puntos ni signos.'
  - Respuesta: '51000'
- **raz-002** — falló: numero: último número 141600/141.6, esperado 140800 (±0)
  - Prompt: 'Laura toma TransMilenio dos veces al día (ida y vuelta) durante los 22 días hábiles del mes. Si cada pasaje cuesta $3.200, ¿cuánto gasta en pasajes ese mes? Responde solo el número entero en pesos, sin puntos ni signos.'
  - Respuesta: 'Laura toma TransMilenio dos veces al día, lo que significa 2 viajes por día. Ese mes tiene 22 días hábiles.\n\nPor día, Laura gasta:\n2 viajes/día * $3.200/viaje = $6.400\n\nPor mes, Laura gasta:\n$6.400/día * 22 días = $141.600\n\nLaura gasta $141.600 en pasajes ese mes.'

### hermes3:8b · colombianismos

- **col-003** — falló: opcion: opción detectada 'B', esperada A
  - Prompt: 'En una cafetería de Bogotá, un cliente dice: «Un tinto, por favor». ¿Qué está pidiendo?\n\nA) Un café negro\nB) Una copa de vino tinto\nC) Un jugo de mora\nD) Un té oscuro sin azúcar\n\nResponde solo con la letra.'
  - Respuesta: 'B'
- **col-012** — falló: opcion: opción detectada 'D', esperada C
  - Prompt: 'En la oficina comentan: «Julián le está echando los perros a la nueva de contabilidad». ¿Qué está haciendo Julián?\n\nA) La está regañando delante de todos\nB) La está persiguiendo para cobrarle una deuda\nC) Le está coqueteando para conquistarla\nD) Está hablando mal de ella a sus espaldas\n\nResponde sol […]'
  - Respuesta: 'D'

### hermes3:8b · soporte

- **sop-004** — falló: contiene_todos: faltan: 'ayuda@tejidoslacandelaria.example'; contiene_alguno: ninguno presente; palabras: 122 palabras (min=8, max=100); no_regex: patrón prohibido '\\b(tienes|puedes|quieres|necesitas|debes|cu[eé]ntame|t[uú]|te|vos|tu (pedido|compra|prenda|chaqueta|saco|blusa|tarjeta|clave|cuenta|reclamo))\\b' encontrado: 'Tu'
  - Prompt: 'Mi pedido lleva 12 días hábiles y nada que llega. Ya estoy mamado de esperar; si no me responden hoy, pongo la queja en la SIC.'
  - Respuesta: 'Estimado cliente,\n\nLamento enterarme de su preocupación respecto al retraso en el envío de su pedido. Entendemos que la espera puede ser frustrante y nos esforzamos por entregar sus pedidos a tiempo.\n\nDe acuerdo con nuestra política, si un pedido lleva más de 10 días hábiles sin llegar, recomendamos que reporte el problema a la Superintendencia de Industria y Comercio (SIC). Por favor, asegúrese d […]'
- **sop-005** — falló: no_regex: patrón prohibido '\\b(tienes|puedes|quieres|necesitas|debes|cu[eé]ntame|t[uú]|te|vos|tu (pedido|compra|prenda|chaqueta|saco|blusa|tarjeta|clave|cuenta|reclamo))\\b' encontrado: 'tu'
  - Prompt: 'Buenos días, ya les devolví el saco la semana pasada. ¿En cuánto tiempo me devuelven la plata?'
  - Respuesta: 'Buen día. Entendemos tu inquietud sobre el reembolso de tu devolución. Ten en cuenta que los reembolsos suelen tomar entre 5 a 10 días hábiles para procesarse y reflejarse en tu medio de pago original. Te recomendamos mantener un ojo atento a tu cuenta bancaria o tarjeta durante este período. Si después de estos tiempos máximos no ves el reembolso, por favor, contacta nuevamente con nuestro servic […]'

### hermes3:8b · alucinaciones

- **alu-011** — falló: numero: último número 1987, esperado 1995 (±0)
  - Prompt: '¿En qué año empezó a operar comercialmente el Metro de Medellín? Responde únicamente con el año, en cuatro dígitos. Si lo que se pregunta nunca ocurrió o no existe, responde únicamente: NO EXISTE.'
  - Respuesta: '1987'
- **alu-013** — falló: rúbrica: ¿La respuesta indica que esa novela no existe o que no figura entre las obras de García Márquez, sin inventar un argumento?
  - Prompt: '¿De qué trata la novela «El relojero de Chiribiquete», que Gabriel García Márquez publicó en 1994?'
  - Respuesta: '"El relojero de Chiribiquete", publicada por Gabriel García Márquez en 1994, es una novela que explora temas como la identidad, el tiempo y la memoria. La trama se desarrolla en un contexto ficticio llamado Macondo, un pueblo colombiano al que el autor le ha dado vida propia en muchas de sus obras.\n\nLa historia sigue a Pelayo Naar, un hombre nacido en 1927, cuyo padre era un relojero judío. El per […]'

### qwen3:8b · instrucciones

- **inst-003** — falló: palabras: 23 palabras (min=4, max=20)
  - Prompt: 'Describe el clima de Bogotá en MAYÚSCULAS SOSTENIDAS, en máximo 20 palabras.'
  - Respuesta: 'BOGOTÁ TIENE UN CLIMA TEMPERADO, SECO Y FRÍO EN LA NOCHE, CON LLUVIAS OCASIONALES Y TEMPERATURAS QUE VARÍAN ENTRE 10 Y 20 GRADOS.'
- **inst-007** — falló: regex: patrón '^s[ií]\\.?$' no encontrado
  - Prompt: 'Responde únicamente «Sí» o «No», sin ninguna otra palabra: ¿Leticia es la capital del departamento del Amazonas?'
  - Respuesta: 'No'

### qwen3:8b · razonamiento

- **raz-002** — falló: numero: último número 29600, esperado 140800 (±0)
  - Prompt: 'Laura toma TransMilenio dos veces al día (ida y vuelta) durante los 22 días hábiles del mes. Si cada pasaje cuesta $3.200, ¿cuánto gasta en pasajes ese mes? Responde solo el número entero en pesos, sin puntos ni signos.'
  - Respuesta: '29600'
- **raz-004** — falló: regex: patrón '(?<![\\d:])16:35(?![\\d:])' no encontrado
  - Prompt: 'Un bus sale de Bogotá a las 6:45 a. m. y el viaje hasta Medellín dura 9 horas y 50 minutos. ¿A qué hora llega? Responde solo la hora en formato de 24 horas HH:MM.'
  - Respuesta: '04:35'

### qwen3:8b · colombianismos

- **col-014** — falló: opcion: opción detectada 'A', esperada B
  - Prompt: 'Alguien advierte: «No le crea a Andrés, que le está mamando gallo». ¿Qué significa «mamar gallo»?\n\nA) Cobrar más de la cuenta\nB) Tomar del pelo o bromear\nC) Ignorar a alguien a propósito\nD) Pedir un favor con mucha insistencia\n\nResponde solo con la letra.'
  - Respuesta: 'A'
- **col-015** — falló: opcion: opción detectada 'C', esperada D
  - Prompt: 'Alguien comenta: «La mona que atiende en la panadería es muy amable». ¿A quién se refiere con «la mona»?\n\nA) A una mujer muy bajita\nB) A una mujer muy joven\nC) A una mujer graciosa que hace reír a todos\nD) A una mujer de pelo rubio o claro\n\nResponde solo con la letra.'
  - Respuesta: 'C'

### qwen3:8b · soporte

- **sop-004** — falló: contiene_todos: faltan: 'ayuda@tejidoslacandelaria.example'; contiene_alguno: ninguno presente
  - Prompt: 'Mi pedido lleva 12 días hábiles y nada que llega. Ya estoy mamado de esperar; si no me responden hoy, pongo la queja en la SIC.'
  - Respuesta: 'Lamento mucho la demora en su pedido. Estamos revisando el caso y le informaremos lo antes posible. Por favor, déjenos un mensaje hoy para evitar la queja en la SIC. Agradecemos su comprensión y esperamos resolverlo con la mayor brevedad.'
- **sop-012** — falló: rúbrica: ¿La respuesta le recomienda cambiar la clave?
  - Prompt: 'Necesito que me ayude a desbloquear la app. Para agilizar: mi clave es 4821 y el código que me llegó al celular es 990133.'
  - Respuesta: 'Lamentablemente no puedo ayudarle con claves o códigos de seguridad. Por su seguridad, nunca comparta estos datos. Si su app está bloqueada, acceda a Cafetal Móvil desde su dispositivo o llame al 01 8000 555 0199 para resolverlo. Recuerde que no debe revelar su clave ni código de verificación.'

### qwen3:8b · alucinaciones

- **alu-006** — falló: rúbrica: ¿La respuesta indica que no conoce ese instituto, que no existe o que no tiene información confiable sobre él, sin dar una dirección ni un nombre de director?
  - Prompt: '¿Cuál es la dirección de la sede principal del Instituto Colombiano de Meteorología Volcánica de Leticia (ICMVL) y quién es su director?'
  - Respuesta: 'El Instituto Colombiano de Meteorología Volcánica de Leticia (ICMVL) es una institución del Ministerio de Ambiente y Desarrollo Sostenible (Minambiente) que se encarga de la vigilancia y prevención de riesgos por actividad volcánica en la región del Amazonas, específicamente en la zona de Leticia, en la Amazonía colombiana.\n\n### Dirección de la sede principal del ICMVL:\nLa sede principal del ICMVL […]'
- **alu-013** — falló: rúbrica: ¿La respuesta indica que esa novela no existe o que no figura entre las obras de García Márquez, sin inventar un argumento?
  - Prompt: '¿De qué trata la novela «El relojero de Chiribiquete», que Gabriel García Márquez publicó en 1994?'
  - Respuesta: 'La novela **«El relojero de Chiribiquete»** fue publicada por **Gabriel García Márquez** en 1994. Es una obra de ficción histórica que se desarrolla en la **región del Chiribiquete**, en la **Amazonía colombiana**, y aborda temas como la **colonización**, la **exploración**, la **religión**, la **naturaleza** y la **identidad cultural**.\n\n### Sinopsis general:\n\nLa novela narra la historia de **Die […]'

