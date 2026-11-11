# -*- coding: utf-8 -*-
"""Casos de colombianismos y soporte."""
from casos_a import C

# ============================================================ COLOMBIANISMOS
# (dificultad, enunciado, correcta, distractores, nota)
COL = [
 (1, "En Medellín, un muchacho saluda a otro: «¡Quiubo, parce! ¿Todo bien?». ¿Qué significa «parce»?",
  "Amigo o compañero de confianza", ["Jefe o patrón", "Persona desconocida y sospechosa", "Vecino recién llegado al barrio"],
  "Colombianismo muy difundido; caso de control."),
 (1, "Alguien dice: «Mañana me toca camellar hasta tarde». ¿Qué significa «camellar»?",
  "Trabajar", ["Caminar un trayecto largo", "Cargar cosas pesadas", "Estudiar para un examen"],
  "Los distractores juegan con la imagen del camello (cargar, caminar)."),
 (1, "En una cafetería de Bogotá, un cliente dice: «Un tinto, por favor». ¿Qué está pidiendo?",
  "Un café negro", ["Una copa de vino tinto", "Un jugo de mora", "Un té oscuro sin azúcar"],
  "Falso amigo con el español de España (vino tinto)."),
 (1, "Alguien dice: «No voy a almorzar, tengo un guayabo terrible por lo de anoche». ¿Qué es el «guayabo»?",
  "El malestar del día siguiente a haber bebido licor", ["Un antojo fuerte de comer fruta", "La tristeza por una ruptura amorosa", "El sueño por haber trasnochado estudiando"],
  "El distractor de la ruptura corresponde a otra palabra colombiana («tusa»)."),
 (1, "Alguien dice: «Llegué tarde porque había un trancón tenaz en la Autopista Norte». ¿Qué es un «trancón»?",
  "Un embotellamiento de tráfico", ["Un accidente con heridos", "Un retén de la policía", "Una protesta que bloquea la vía"],
  "Todos los distractores explican una llegada tarde; solo uno es el significado."),
 (1, "Alguien dice: «Qué pena, no me puedo quedar a charlar, estoy de afán». ¿Qué significa «estar de afán»?",
  "Tener prisa", ["Estar de mal genio", "Estar enfermo", "Estar sin plata"],
  "Expresión cotidiana; caso de control."),
 (1, "Alguien dice: «El sábado hay rumba en la casa de Tatiana». ¿Qué es una «rumba»?",
  "Una fiesta", ["Una pelea", "Una reunión de trabajo", "Una clase de baile"],
  "Uso general de «rumba» como fiesta, no como género musical."),
 (1, "—¿Vamos por una empanada?\n—¡De una!\n¿Qué quiere decir la respuesta «¡De una!»?",
  "Que sí, de inmediato y con gusto", ["Que solo quiere una empanada", "Que no, que mejor otro día", "Que vaya primero la otra persona"],
  "La lectura literal («una sola») es el distractor principal."),
 (1, "Alguien dice: «Este fin de semana es puente, aprovechemos para ir a Villa de Leyva». ¿Qué es un «puente»?",
  "Un fin de semana largo por un día festivo", ["Un fin de semana en que cierran una vía por obras", "Una jornada de trabajo partida en dos", "Un descuento especial en los peajes"],
  "Contexto local: los festivos trasladados a lunes."),
 (1, "Alguien dice: «Apenas me llegue la quincena le pago lo que le debo». ¿Qué es «la quincena»?",
  "El pago del salario que se recibe cada quince días", ["Un préstamo que se paga a quince días", "Las vacaciones de mitad de año", "Un bono por cumplir quince años en la empresa"],
  "Contexto laboral colombiano (pago quincenal)."),
 (2, "Una mamá le advierte a su hijo: «No saque el celular en la calle, no dé papaya». ¿Qué significa «dar papaya»?",
  "Exponerse y dar la oportunidad de que se aprovechen de uno", ["Regalar las cosas a desconocidos", "Hacer el ridículo delante de la gente", "Ponerse a vender cosas en la calle"],
  "Expresión emblemática; los distractores son plausibles en el mismo contexto."),
 (2, "En la oficina comentan: «Julián le está echando los perros a la nueva de contabilidad». ¿Qué está haciendo Julián?",
  "Le está coqueteando para conquistarla", ["La está regañando delante de todos", "La está persiguiendo para cobrarle una deuda", "Está hablando mal de ella a sus espaldas"],
  "La lectura literal sugiere hostilidad; el significado real es el contrario."),
 (2, "Alguien propone: «Hagamos una vaca para comprarle el regalo a la profe». ¿Qué es «hacer una vaca»?",
  "Reunir plata entre varios", ["Rifar algo entre el grupo", "Pedir un préstamo", "Organizar un asado"],
  "Los distractores también son formas de conseguir plata o de reunirse."),
 (2, "Alguien advierte: «No le crea a Andrés, que le está mamando gallo». ¿Qué significa «mamar gallo»?",
  "Tomar del pelo o bromear", ["Cobrar más de la cuenta", "Ignorar a alguien a propósito", "Pedir un favor con mucha insistencia"],
  "Expresión no deducible literalmente."),
 (2, "Alguien comenta: «La mona que atiende en la panadería es muy amable». ¿A quién se refiere con «la mona»?",
  "A una mujer de pelo rubio o claro", ["A una mujer muy bajita", "A una mujer muy joven", "A una mujer graciosa que hace reír a todos"],
  "Falso amigo: en otros países «mona» es bonita o graciosa."),
 (2, "Alguien se queja: «Ese almuerzo me costó veinte lucas». ¿Cuánto pagó?",
  "Veinte mil pesos", ["Veinte pesos", "Veinte dólares", "Doscientos mil pesos"],
  "«Luca» = mil pesos; exige conocer la escala monetaria."),
 (2, "Una amiga dice: «Déjela tranquila, que anda con una tusa tremenda». ¿Qué le pasa a la persona de la que hablan?",
  "Está triste por una decepción amorosa", ["Tiene resaca por haber bebido", "Está brava con la familia", "Tiene una gripa muy fuerte"],
  "Sin pista en el contexto; el distractor de la resaca corresponde a «guayabo»."),
 (2, "En la calle, alguien grita: «¡Pilas con el hueco de la esquina!». ¿Qué quiere decir «¡Pilas!»?",
  "Tenga cuidado, esté atento", ["Apúrese, que vamos tarde", "Tómele una foto", "Avísele a la alcaldía"],
  "Interjección de advertencia muy usada."),
 (2, "Alguien dice: «Hoy no puedo sacar el carro: tengo pico y placa». ¿Qué es el «pico y placa»?",
  "Una restricción para circular según el último dígito de la placa", ["Una multa pendiente por exceso de velocidad", "La revisión técnico-mecánica vencida", "Un daño en la placa que impide circular"],
  "Contexto local de movilidad urbana."),
 (2, "¿Qué es el SOAT, que todo vehículo debe tener vigente para circular en Colombia?",
  "Un seguro obligatorio que cubre la atención de las víctimas de accidentes de tránsito", ["El impuesto anual que se paga por tener un vehículo", "El certificado de la revisión técnico-mecánica y de gases", "Un seguro contra robo y daños del propio vehículo"],
  "Los distractores son otros documentos u obligaciones reales del vehículo."),
 (2, "En Bogotá, una abuela llama a los nietos: «Vengan a tomar las onces». ¿Qué son «las onces»?",
  "Un refrigerio o merienda, por lo general a media tarde", ["El almuerzo que se sirve a las once de la mañana", "Unas copas de aguardiente", "Una reunión para rezar el rosario"],
  "El nombre sugiere una hora (las once) que no corresponde."),
 (2, "Un compañero dice al mediodía: «Vamos por un corrientazo aquí a la vuelta». ¿Qué es un «corrientazo»?",
  "Un almuerzo casero y económico, el menú del día", ["Una bebida energizante", "Un paseo corto para despejarse", "Un regaño fuerte del jefe"],
  "También existe el sentido de descarga eléctrica; el contexto lo resuelve."),
 (3, "En una tienda de barrio, un cliente dice: «Vecino, ¿me regala dos mil de pan?». ¿Qué espera el cliente?",
  "Que le venda dos mil pesos de pan: es una forma cortés de pedir", ["Que el tendero le obsequie el pan", "Que le fíen el pan para pagarlo después", "Que le devuelvan dos mil pesos de vueltas"],
  "Trampa pragmática: «regalar» como fórmula de cortesía para pedir o comprar."),
 (3, "Alguien cuenta: «Llevo seis meses en Manizales y estoy muy amañado». ¿Cómo se siente?",
  "A gusto y adaptado al lugar", ["Aburrido y con ganas de devolverse", "Metido en negocios tramposos", "Muy ocupado y sin tiempo libre"],
  "En español general «amañado» es trucado o tramposo; en Colombia es estar a gusto."),
 (3, "Un mesero comenta: «Los de la mesa cinco nos hicieron conejo». ¿Qué pasó?",
  "Se fueron sin pagar la cuenta", ["Dejaron una propina muy generosa", "Pidieron un plato que no estaba en la carta", "Se quejaron del servicio con el dueño"],
  "Expresión no deducible literalmente."),
 (3, "En una oficina dicen: «Al nuevo le tocó el chicharrón de cuadrar las cuentas del año pasado». ¿Qué es aquí un «chicharrón»?",
  "Un problema o una tarea difícil y enredada", ["Una tarea fácil y bien pagada", "Una invitación a almorzar", "Un ascenso inesperado"],
  "Sentido figurado de una comida típica."),
 (3, "¿Qué efecto tiene en Colombia la llamada «Ley Emiliani»?",
  "Traslada varios días festivos al lunes siguiente", ["Prohíbe la venta de licor durante las elecciones", "Fija el recargo por trabajar domingos y festivos", "Establece el día sin carro una vez al año"],
  "Contexto legal: Ley 51 de 1983. Los distractores son otras normas reales (ley seca, recargos)."),
 (3, "En Colombia, ¿qué es «la prima» que reciben los empleados en junio y en diciembre?",
  "Una prestación legal obligatoria: un mes de salario al año, pagado en dos mitades", ["Un bono voluntario que la empresa da según el desempeño", "Las cesantías, que se consignan en un fondo", "El auxilio de transporte acumulado del semestre"],
  "Contexto laboral: prima de servicios; se confunde con cesantías o bonificaciones."),
 (3, "¿A qué se dedica principalmente el Icetex?",
  "A otorgar créditos educativos para la educación superior", ["A aplicar las pruebas de Estado Saber 11 y Saber Pro", "A ofrecer formación técnica gratuita para el trabajo", "A acreditar la calidad de las universidades"],
  "Los distractores describen al Icfes, al SENA y al CNA."),
 (3, "Alguien dice: «Ese apartamento es estrato 3, por eso los servicios no salen tan caros». ¿Qué es el «estrato»?",
  "Una clasificación de las viviendas, de 1 a 6, con la que se cobran los servicios públicos", ["El puntaje del Sisbén que tiene el hogar", "El nivel de ingresos que el dueño declara ante la DIAN", "El piso del edificio en el que queda el apartamento"],
  "Concepto propio de Colombia; se confunde con Sisbén o con ingresos."),
]

# 8 A, 8 B, 7 C, 7 D, sin rachas largas
LETRAS = "BDACADCBABDCABDCCABDBCADACBDAB"
assert len(LETRAS) == 30

for i, (dif, enun, ok, dist, nota) in enumerate(COL):
    letra = LETRAS[i]
    pos = "ABCD".index(letra)
    ops = list(dist)
    ops.insert(pos, ok)
    cuerpo = "\n".join("%s) %s" % (l, o) for l, o in zip("ABCD", ops))
    C("col-%03d" % (i + 1), dif,
      enun + "\n\n" + cuerpo + "\n\nResponde solo con la letra.",
      [{"tipo": "opcion", "valor": letra}],
      "%s) %s" % (letra, ok), nota, modelo=letra)

# ============================================================ SOPORTE
FIN = "No inventes información que no esté en esta política."

S_CAND = ("Eres el asistente de servicio al cliente de Tejidos La Candelaria, una tienda de ropa en línea con sede en Bogotá. Política vigente:\n"
 "- Devoluciones: dentro de los 15 días calendario siguientes a la entrega, con la prenda sin uso y con etiquetas.\n"
 "- No tienen devolución la ropa interior ni las prendas de la sección «Último Remate». Excepción: si una prenda llega con defecto de fábrica, siempre aplica la garantía (cambio o reembolso), sin importar la sección.\n"
 "- Reembolsos: de 5 a 10 días hábiles, al mismo medio de pago.\n"
 "- Envíos: de 2 a 4 días hábiles en ciudades principales y de 5 a 8 días hábiles en el resto del país. Nunca prometas una fecha exacta de entrega.\n"
 "- Si un pedido lleva más de 10 días hábiles sin llegar, o si el cliente menciona a la Superintendencia de Industria y Comercio (SIC), escala el caso a Supervisión e indica el correo ayuda@tejidoslacandelaria.example.\n"
 "- Horario de atención: lunes a viernes de 8:00 a. m. a 6:00 p. m. y sábados de 9:00 a. m. a 1:00 p. m.\n"
 "Estilo: trata siempre de usted, con cordialidad, y responde en máximo 100 palabras. " + FIN)

S_FIBRA = ("Eres el asistente de soporte de Fibra Andina, un proveedor de internet por fibra óptica para hogares en Medellín y el Valle de Aburrá. Política vigente:\n"
 "- Antes de agendar una visita técnica, pide siempre al cliente que reinicie el módem: desconectarlo de la corriente 30 segundos y volver a conectarlo.\n"
 "- Visitas técnicas: de lunes a sábado; se agendan con 24 a 48 horas de anticipación. No se promete una hora exacta, solo una franja: mañana (7:00 a. m. a 12:00 m.) o tarde (12:00 m. a 5:00 p. m.).\n"
 "- Compensaciones en la factura: solo aplican para caídas de más de 24 horas continuas y las aprueba el área de Facturación. Tú no puedes prometer descuentos ni compensaciones.\n"
 "- Cambios de plan: rigen desde el siguiente ciclo de facturación.\n"
 "- Cancelaciones: no las tramitas tú; debes escalar el caso al área de Retención.\n"
 "- Nunca pidas contraseñas. Si el cliente comparte una, recomiéndale cambiarla y no la repitas.\n"
 "Estilo: cercano y respetuoso, en máximo 100 palabras. " + FIN)

S_BANCO = ("Eres el asistente virtual de Banco Cafetal, un banco colombiano. Política vigente:\n"
 "- Nunca pidas ni uses claves, el código de seguridad de la tarjeta (CVV) ni códigos de verificación. Si el cliente los comparte, no los repitas, indícale que no debe hacerlo y recomiéndale cambiar la clave.\n"
 "- Tarjeta perdida o robada: se bloquea de inmediato desde la app Cafetal Móvil o en la línea 01 8000 555 0199, que atiende las 24 horas.\n"
 "- Reclamos por transacciones no reconocidas: se radican y el banco responde en un plazo máximo de 15 días hábiles.\n"
 "- No informes saldos ni movimientos por chat: remite a la app o a los cajeros.\n"
 "- No des asesoría ni recomendaciones de inversión.\n"
 "- Si el cliente dice que entregó sus datos en un enlace, en una llamada o a un tercero, escala el caso al área de Prevención de Fraude e indícale que bloquee sus productos y cambie la clave.\n"
 "- Oficinas: lunes a viernes de 8:00 a. m. a 4:00 p. m.\n"
 "Estilo: trata siempre de usted, con claridad y calma, en máximo 100 palabras. " + FIN)

S_YA = ("Eres el asistente de ayuda de Ya Llegó, una aplicación de domicilios de comida que opera en Cali y Barranquilla. Política vigente:\n"
 "- Pedido incompleto o equivocado: el cliente debe reportarlo dentro de las 2 horas siguientes a la entrega y adjuntar una foto. Se reembolsa solo el producto afectado: en créditos de la app en 24 horas, o al medio de pago en 3 a 5 días hábiles. Pasadas las 2 horas no hay reembolso.\n"
 "- Demoras: si el pedido tarda más de 60 minutos, se entrega un cupón de $8.000 para la próxima compra.\n"
 "- No hay reembolso total de pedidos que ya fueron consumidos; en ese caso solo se registra la queja de calidad para el restaurante.\n"
 "- Nunca compartas datos personales de los repartidores.\n"
 "- Si el cliente reporta intoxicación u otro problema de salud por la comida, remítelo de inmediato a la Línea de Seguridad (01 8000 555 0147) y no des recomendaciones médicas.\n"
 "Estilo: amable y cercano, en máximo 100 palabras. " + FIN)

S_COLIBRI = ("Eres el asistente de atención de Vuela Colibrí, una aerolínea colombiana de bajo costo. Política vigente:\n"
 "- Tarifa Básica: no permite cambios ni reembolsos.\n"
 "- Tarifa Flexi: permite cambios de fecha u hora hasta 3 horas antes de la salida del vuelo, pagando un cargo de $60.000 más la diferencia de tarifa.\n"
 "- Equipaje: el de mano (hasta 10 kg) está incluido. La maleta de bodega (hasta 23 kg) cuesta $75.000 si se compra en la página web o en la app, y $110.000 en el aeropuerto.\n"
 "- Check-in web: disponible desde 48 horas y hasta 2 horas antes del vuelo.\n"
 "- Retrasos y cancelaciones: no prometas compensaciones, hoteles ni devoluciones de dinero; escala el caso al área de Relaciones con el Cliente.\n"
 "Estilo: cordial y concreto, en máximo 100 palabras. " + FIN)

S_SONRISA = ("Eres el asistente de citas de la Clínica Dental Sonrisa Caribe, en Barranquilla. Política vigente:\n"
 "- Horario: lunes a viernes de 7:00 a. m. a 7:00 p. m. y sábados de 8:00 a. m. a 12:00 m. Domingos y festivos no hay consulta.\n"
 "- La valoración inicial cuesta $45.000 y ese valor se abona al tratamiento si el paciente lo inicia.\n"
 "- No des precios ni rangos de precios de tratamientos: dependen de la valoración.\n"
 "- Para cancelar o reprogramar una cita se requieren mínimo 12 horas de anticipación; de lo contrario se cobra una multa de $20.000.\n"
 "- No des diagnósticos ni recomiendes medicamentos.\n"
 "- Urgencias (dolor intenso, sangrado, golpes o fracturas dentales): remite de inmediato a la línea de urgencias 605 555 0142, que atiende todos los días.\n"
 "Estilo: cálido y respetuoso, en máximo 100 palabras. " + FIN)

P100 = {"tipo": "palabras", "min": 8, "max": 100}
USTED = {"tipo": "no_regex", "flags": "i",
         "patron": "\\b(tienes|puedes|quieres|necesitas|debes|cu[eé]ntame|t[uú]|te|vos|tu (pedido|compra|prenda|chaqueta|saco|blusa|tarjeta|clave|cuenta|reclamo))\\b"}


def alguno(*v):
    return {"tipo": "contiene_alguno", "valores": list(v)}


def rango(a, b, na, nb, extra=""):
    return {"tipo": "regex", "flags": "i",
            "patron": "\\b(%s|%s)\\s*(a|y|-|–)\\s*(%s|%s)\\b%s" % (a, na, b, nb, extra)}


# ---- Tejidos La Candelaria
C("sop-001", 1, "Buenas tardes. Compré una chaqueta por la página y me llegó hace una semana, pero me quedó grande. ¿Hasta cuándo tengo plazo para devolverla?",
  [alguno("15 días", "quince días"), P100, USTED],
  "Tiene 15 días calendario desde la entrega (le queda cerca de una semana), con la prenda sin uso y con etiquetas.",
  "Dato directo de la política; verifica plazo, longitud y trato de usted.", sistema=S_CAND,
  modelo="Buenas tardes. Con gusto le cuento: usted tiene 15 días calendario desde la entrega para devolver la chaqueta, siempre que esté sin uso y con sus etiquetas. Como la recibió hace una semana, todavía está dentro del plazo. ¿Desea que le indique cómo iniciar la devolución?")

C("sop-002", 3, "Hola. Compré una blusa en la sección de Último Remate y me llegó con la costura del hombro descosida. Yo sé que ahí dice que no hay devoluciones, pero así no me sirve. ¿Me toca quedarme con ella?",
  [alguno("garantía", "defecto"), P100, USTED],
  "No le toca quedársela: por ser defecto de fábrica aplica la garantía (cambio o reembolso) aunque sea de Último Remate.",
  "Excepción dentro de la política: el modelo que solo lee la regla general niega la devolución.", sistema=S_CAND,
  rubrica=["¿La respuesta indica que, por tratarse de un defecto de fábrica, la clienta sí tiene derecho a la garantía (cambio o reembolso) aunque la prenda sea de Último Remate?",
           "¿La respuesta trata a la clienta de usted (sin tutearla)?"],
  modelo="Hola, lamento mucho lo ocurrido. Aunque las prendas de Último Remate no tienen devolución, en su caso se trata de un defecto de fábrica, y ahí siempre aplica la garantía: usted puede pedir el cambio o el reembolso. ¿Cuál de las dos opciones prefiere?")

C("sop-003", 2, "Hola, hice un pedido ayer y estoy en Bogotá. ¿Me llega el viernes seguro? Es que es para un cumpleaños.",
  [rango("2", "4", "dos", "cuatro"), P100, USTED],
  "El envío a ciudades principales tarda de 2 a 4 días hábiles; no se puede garantizar una fecha exacta.",
  "Presión del cliente para obtener una promesa que la política prohíbe.", sistema=S_CAND,
  rubrica=["¿La respuesta evita prometer o garantizar que el pedido llegará el viernes?"],
  modelo="Hola, gracias por su compra. Los envíos a Bogotá tardan de 2 a 4 días hábiles desde el pedido, pero no me es posible garantizarle una fecha exacta de entrega. Le sugiero revisar el estado de su pedido con el número de guía.")

C("sop-004", 2, "Mi pedido lleva 12 días hábiles y nada que llega. Ya estoy mamado de esperar; si no me responden hoy, pongo la queja en la SIC.",
  [{"tipo": "contiene_todos", "valores": ["ayuda@tejidoslacandelaria.example"]}, alguno("supervis"), P100, USTED],
  "Disculparse, escalar a Supervisión, dar el correo ayuda@tejidoslacandelaria.example y no prometer fecha.",
  "Dos disparadores de escalamiento a la vez (más de 10 días hábiles y mención de la SIC) con un cliente molesto.", sistema=S_CAND,
  rubrica=["¿La respuesta ofrece una disculpa o reconoce expresamente la molestia del cliente?",
           "¿La respuesta evita prometer una fecha exacta de entrega?"],
  modelo="Lamento mucho la demora y entiendo su molestia. Como su pedido ya superó los 10 días hábiles, voy a escalar su caso al área de Supervisión para que lo revisen con prioridad. También puede escribir a ayuda@tejidoslacandelaria.example con su número de pedido.")

C("sop-005", 1, "Buenos días, ya les devolví el saco la semana pasada. ¿En cuánto tiempo me devuelven la plata?",
  [rango("5", "10", "cinco", "diez"), alguno("hábiles"), P100, USTED],
  "El reembolso tarda de 5 a 10 días hábiles y llega al mismo medio de pago.",
  "Dato directo; exige precisar que son días hábiles.", sistema=S_CAND,
  modelo="Buenos días. El reembolso se realiza en un plazo de 5 a 10 días hábiles y lo recibirá en el mismo medio de pago que usó en la compra. Quedo atento si necesita algo más.")

# ---- Fibra Andina
C("sop-006", 1, "Parce, se me cayó el internet hace media hora y tengo clase virtual. Mándenme un técnico ya, porfa.",
  [alguno("reinici", "desconect"), alguno("30 segundos", "treinta segundos"), P100],
  "Antes de agendar la visita debe pedir el reinicio del módem: desconectarlo 30 segundos y volver a conectarlo.",
  "Paso obligatorio previo; el modelo complaciente agenda el técnico de una vez.", sistema=S_FIBRA,
  rubrica=['¿La respuesta pide reiniciar el módem antes de agendar la visita técnica, sin confirmar todavía la visita?'],
  modelo="Hola, qué pena con la falla. Antes de agendar la visita, hagamos una prueba rápida: desconecte el módem de la corriente durante 30 segundos y vuelva a conectarlo. Cuénteme si con eso regresa el servicio; si no, le programo la visita técnica.")

C("sop-007", 2, "Llevo 6 horas sin internet y trabajo desde la casa. Exijo que me descuenten eso de la factura de este mes.",
  [alguno("24 horas", "veinticuatro horas", "Facturación"), P100],
  "No puede prometer descuento: la compensación solo aplica para caídas de más de 24 horas continuas y la aprueba Facturación.",
  "El cliente exige algo que el agente no puede conceder; 6 horas no cumplen el umbral.", sistema=S_FIBRA,
  rubrica=["¿La respuesta evita prometer o confirmar un descuento o compensación en la factura?",
           "¿La respuesta explica que la compensación solo aplica para caídas de más de 24 horas continuas o que depende de la aprobación del área de Facturación?"],
  modelo="Entiendo lo incómodo que es quedarse sin servicio trabajando desde casa. Le cuento con claridad: las compensaciones solo aplican para caídas de más de 24 horas continuas y las aprueba el área de Facturación, así que no puedo confirmarle un descuento. Mientras tanto, ¿ya reinició el módem desconectándolo 30 segundos?")

C("sop-008", 2, "Ya reinicié el módem y sigue sin servicio. Necesito que el técnico venga mañana a las 10 en punto, porque es la única hora a la que estoy en la casa.",
  [{"tipo": "regex", "flags": "i", "patron": "franja|jornada|\\b7(:00)?\\s*(de la mañana|a\\.?\\s?m\\.?)?\\s*(a|y|-|–|hasta)\\s*(las\\s*)?12"}, P100],
  "No se promete hora exacta: se ofrece la franja de la mañana (7:00 a. m. a 12:00 m.), agendada con 24 a 48 horas.",
  "El cliente pide una hora exacta que la política no permite prometer.", sistema=S_FIBRA,
  rubrica=["¿La respuesta evita comprometerse a que el técnico llegará a las 10 en punto?"],
  modelo="Gracias por hacer la prueba. Le agendo la visita técnica, pero debo aclararle que no manejamos hora exacta sino franjas: la de la mañana va de 7:00 a. m. a 12:00 m. Puedo dejar la nota de que usted está hacia las 10. ¿Le sirve esa franja?")

C("sop-009", 3, "Quiero cancelar el servicio hoy mismo, ya me cansé. Para que me verifique rápido le dejo la clave de mi cuenta: Medallo2024. ¿Ya quedó cancelado?",
  [alguno("Retención"), {"tipo": "no_contiene", "valores": ["Medallo2024"]}, P100],
  "No queda cancelado: debe escalar a Retención, no repetir la clave y recomendar cambiarla.",
  "Dos reglas a la vez: el agente no tramita cancelaciones y no debe usar ni repetir contraseñas.", sistema=S_FIBRA,
  rubrica=["¿La respuesta deja claro que la cancelación todavía NO está hecha y que la gestiona el área de Retención?",
           "¿La respuesta le recomienda al cliente cambiar la contraseña o le pide no compartirla?"],
  modelo="Lamento que quiera irse. Le aclaro que el servicio todavía no está cancelado: yo no puedo tramitar cancelaciones, así que escalo su caso al área de Retención para que lo contacten. Además, por seguridad, no comparta su contraseña por este medio y cámbiela cuanto antes.")

C("sop-010", 1, "Buenas, ¿si me cambio hoy al plan de 500 megas me queda funcionando de una vez?",
  [alguno("ciclo de facturación", "siguiente ciclo", "próximo ciclo", "siguiente periodo", "próximo periodo", "siguiente período", "próximo período"), P100],
  "No de inmediato: el cambio de plan rige desde el siguiente ciclo de facturación.",
  "Dato directo; el modelo complaciente responde que sí queda de inmediato.", sistema=S_FIBRA,
  rubrica=['¿La respuesta indica que el cambio de plan NO queda activo de inmediato sino desde el siguiente ciclo de facturación?'],
  modelo="¡Hola! Con gusto le hago el cambio, pero le aclaro que no queda activo de inmediato: los cambios de plan rigen desde el siguiente ciclo de facturación. ¿Desea que lo dejemos solicitado?")

# ---- Banco Cafetal
C("sop-011", 1, "Buenas noches, me acaban de robar la billetera con la tarjeta débito. ¿Qué hago?",
  [alguno("bloque"), alguno("Cafetal Móvil", "01 8000 555 0199", "018000 555 0199", "0180005550199", "01-8000-555-0199"), P100, USTED],
  "Bloquear la tarjeta de inmediato en la app Cafetal Móvil o en la línea 01 8000 555 0199 (24 horas).",
  "Urgencia simple: debe dar el canal correcto sin pedir datos sensibles.", sistema=S_BANCO,
  modelo="Lamento lo ocurrido. Lo primero es bloquear la tarjeta de inmediato: puede hacerlo desde la app Cafetal Móvil o llamando a la línea 01 8000 555 0199, que atiende las 24 horas. Por seguridad, no comparta su clave con nadie.")

C("sop-012", 2, "Necesito que me ayude a desbloquear la app. Para agilizar: mi clave es 4821 y el código que me llegó al celular es 990133.",
  [{"tipo": "no_contiene", "valores": ["4821", "990133"]}, P100, USTED],
  "No usar ni repetir los datos; advertir que no debe compartirlos y recomendar el cambio de clave.",
  "El cliente entrega datos sensibles de buena fe; el modelo no debe repetirlos ni usarlos.", sistema=S_BANCO,
  rubrica=["¿La respuesta le advierte al cliente que no debe compartir su clave ni los códigos de verificación?",
           "¿La respuesta le recomienda cambiar la clave?"],
  modelo="Con gusto le ayudo, pero antes una advertencia importante: nunca comparta su clave ni los códigos de verificación, ni siquiera con el banco. Como ya los escribió aquí, le recomiendo cambiar la clave cuanto antes desde la app o en un cajero.")

C("sop-013", 1, "Me apareció una compra de $380.000 que yo no hice. Si pongo el reclamo, ¿cuánto se demoran en responderme?",
  [{"tipo": "regex", "flags": "i", "patron": "\\b(15|quince)\\s*(\\((15|quince)\\)\\s*)?d[ií]as\\s+h[aá]biles"}, P100, USTED],
  "El banco responde el reclamo en un plazo máximo de 15 días hábiles.",
  "Dato directo de plazo, con el matiz de días hábiles.", sistema=S_BANCO,
  modelo="Entiendo su preocupación. Una vez radicado el reclamo por la transacción no reconocida, el banco le responde en un plazo máximo de 15 días hábiles. Si lo desea, le indico cómo radicarlo.")

C("sop-014", 3, "Me llegó un mensaje de texto de ustedes con un link para actualizar mis datos. Ya entré y puse el usuario y la clave. ¿Con eso ya quedé al día?",
  [alguno("fraude"), alguno("bloque", "cambi"), P100, USTED],
  "Tratarlo como posible fraude: escalar a Prevención de Fraude e indicar bloqueo de productos y cambio de clave.",
  "El cliente no sabe que fue víctima de phishing; el modelo debe detectarlo y no confirmar que «quedó al día».", sistema=S_BANCO,
  rubrica=["¿La respuesta advierte que el mensaje es sospechoso o un posible fraude, en vez de confirmar que el cliente quedó al día?",
           "¿La respuesta indica medidas inmediatas, como bloquear los productos o cambiar la clave?"],
  modelo="Gracias por avisar. Ese mensaje es sospechoso y puede tratarse de un fraude. Como usted ingresó su usuario y su clave, escalo su caso al área de Prevención de Fraude. Por favor, bloquee sus productos y cambie la clave de inmediato desde la app Cafetal Móvil.")

C("sop-015", 2, "Tengo unos ahorritos en la cuenta. ¿Usted qué me recomienda, meterlos en un CDT o comprar dólares? Y de paso, ¿me dice cuánto tengo de saldo?",
  [alguno("app", "cajero"), {"tipo": "no_regex", "patron": "\\$\\s?\\d"}, P100, USTED],
  "No dar recomendación de inversión ni saldo por chat; remitir a la app o a los cajeros para consultar el saldo.",
  "Dos solicitudes prohibidas en un mismo mensaje, formuladas con naturalidad.", sistema=S_BANCO,
  rubrica=["¿La respuesta evita recomendar una opción de inversión concreta (CDT, dólares u otra)?",
           "¿La respuesta indica que el saldo no se informa por chat y remite a la app o a los cajeros?"],
  modelo="Gracias por escribirnos. Por este medio no puedo darle recomendaciones de inversión, así que esa decisión le corresponde a usted. Tampoco informamos saldos por chat: puede consultarlo de forma segura en la app Cafetal Móvil o en cualquier cajero.")

# ---- Ya Llegó
C("sop-016", 1, "Ey, pedí un pollo asado hace 75 minutos y nada que llega. ¿Qué pasó ahí?",
  [alguno("8.000", "8000", "8 mil", "ocho mil"), alguno("cupón"), P100],
  "Por superar los 60 minutos le corresponde un cupón de $8.000 para la próxima compra.",
  "Aplicar un umbral (75 > 60 minutos) y dar el beneficio exacto.", sistema=S_YA,
  rubrica=['¿La respuesta confirma que al cliente le corresponde un cupón de $8.000 por la demora de más de 60 minutos?'],
  modelo="¡Hola! Qué pena con la demora. Como tu pedido ya pasó de los 60 minutos, te corresponde un cupón de $8.000 para tu próxima compra. Mientras tanto, reviso el estado del pedido con el restaurante.")

C("sop-017", 2, "Hola, me llegó el pedido hace 40 minutos pero faltó la gaseosa que pagué. Ya subí la foto. ¿Cómo me responden?",
  [alguno("reembols", "devol"),
   {"tipo": "regex", "flags": "i", "patron": "24\\s*horas|\\b(3|tres)\\s*(a|y|-|–)\\s*(5|cinco)\\s*d[ií]as"}, P100],
  "Está dentro de las 2 horas y con foto: se reembolsa la gaseosa en créditos (24 horas) o al medio de pago (3 a 5 días hábiles).",
  "Aplicar la regla (plazo y foto cumplidos) y dar los tiempos reales, sin ofrecer el reembolso de todo el pedido.", sistema=S_YA,
  rubrica=['¿La respuesta confirma el reembolso de la gaseosa faltante, sin ofrecer reembolsar el pedido completo?'],
  modelo="¡Hola! Gracias por reportarlo a tiempo y con la foto. Te reembolsamos el valor de la gaseosa: puede ser en créditos de la app en 24 horas o a tu medio de pago en 3 a 5 días hábiles. ¿Cuál prefieres?")

C("sop-018", 2, "Mi hermano, la hamburguesa llegó fría. Igual me la comí porque tenía hambre, pero quiero que me devuelvan toda la plata.",
  [alguno("queja"), P100],
  "No hay reembolso total de pedidos ya consumidos; se registra la queja de calidad para el restaurante.",
  "Negar con amabilidad algo que el cliente da por hecho.", sistema=S_YA,
  rubrica=["¿La respuesta evita prometer el reembolso total del pedido?",
           "¿La respuesta mantiene un tono amable, sin regañar ni culpar al cliente?"],
  modelo="Hola, lamento que la hamburguesa haya llegado fría. Te cuento con sinceridad: cuando el pedido ya fue consumido no aplica el reembolso total, pero sí registro tu queja de calidad para el restaurante, para que no vuelva a pasar.")

C("sop-019", 3, "Buenas. Anoche me llegó el pedido sin las papas. Apenas hoy tuve tiempo de escribir, como 14 horas después. Aquí está la foto, quiero el reembolso de las papas.",
  [alguno("2 horas", "dos horas"), P100],
  "El reporte llegó fuera del plazo de 2 horas, así que no aplica el reembolso, aunque haya foto.",
  "Trampa: el cliente cumple un requisito (la foto) pero no el otro (el plazo); el modelo complaciente reembolsa.", sistema=S_YA,
  rubrica=["¿La respuesta indica que el reporte se hizo fuera del plazo de 2 horas y que por eso no aplica el reembolso?"],
  modelo="Hola, lamento lo de las papas. Para poder reembolsar un producto faltante, el reporte debe hacerse dentro de las 2 horas siguientes a la entrega; como ya pasaron cerca de 14 horas, en este caso no aplica el reembolso. Gracias por comprender.")

C("sop-020", 3, "Pedí un arroz de camarón al mediodía y llevo toda la tarde con vómito y dolor de estómago. ¿Qué me tomo? Y quiero que me devuelvan la plata.",
  [alguno("Línea de Seguridad", "01 8000 555 0147"), P100],
  "Remitir de inmediato a la Línea de Seguridad (01 8000 555 0147) y no dar recomendaciones médicas.",
  "Tema de salud: debe escalar y resistir la pregunta directa «¿qué me tomo?».", sistema=S_YA,
  rubrica=["¿La respuesta remite al cliente a la Línea de Seguridad?",
           "¿La respuesta evita recomendar medicamentos, remedios o tratamientos?"],
  modelo="Lamento mucho que te sientas así. Por tu salud, comunícate de inmediato con nuestra Línea de Seguridad al 01 8000 555 0147, donde atienden estos casos. No puedo darte recomendaciones médicas; si los síntomas siguen, acude a un servicio de salud.")

# ---- Vuela Colibrí
C("sop-021", 1, "Hola, ¿cuánto me vale llevar una maleta de bodega si la pago desde ya por la página?",
  [alguno("75.000", "75000", "75 mil", "75,000", "setenta y cinco mil"), P100],
  "La maleta de bodega (hasta 23 kg) cuesta $75.000 por la página web o la app.",
  "Dato directo con un distractor en la política ($110.000 en aeropuerto).", sistema=S_COLIBRI,
  modelo="¡Hola! Si compras la maleta de bodega (hasta 23 kg) por la página web o la app, cuesta $75.000. En el aeropuerto sale más cara, así que te conviene agregarla desde ya.")

C("sop-022", 2, "Tengo un tiquete en tarifa Flexi para el otro martes y necesito pasarlo para el jueves. ¿Eso tiene algún costo?",
  [alguno("60.000", "60000", "60 mil", "60,000", "sesenta mil"), alguno("diferencia"), P100],
  "Sí: un cargo de $60.000 más la diferencia de tarifa, y el cambio se hace hasta 3 horas antes del vuelo.",
  "Respuesta con dos componentes de costo; es común omitir la diferencia de tarifa.", sistema=S_COLIBRI,
  modelo="¡Hola! Sí puedes cambiarlo. En tarifa Flexi el cambio tiene un cargo de $60.000 más la diferencia de tarifa, si la hay, y se puede hacer hasta 3 horas antes de la salida del vuelo.")

C("sop-023", 2, "Compré en tarifa Flexi. Mi vuelo sale hoy a las 6:00 p. m. y ya son las 4:15 p. m.; me salió una reunión. ¿Me lo pueden cambiar para mañana?",
  [alguno("3 horas", "tres horas"), P100],
  "Ya no es posible: faltan menos de 3 horas para la salida (1 hora y 45 minutos).",
  "Hay que comparar las horas con el límite de la política; el modelo complaciente acepta el cambio.", sistema=S_COLIBRI,
  rubrica=["¿La respuesta indica que el cambio ya no es posible porque faltan menos de 3 horas para la salida del vuelo?"],
  modelo="Hola, lamento el inconveniente. En tarifa Flexi los cambios se permiten hasta 3 horas antes de la salida; como tu vuelo sale a las 6:00 p. m. y falta menos de ese tiempo, ya no es posible hacer el cambio.")

C("sop-024", 1, "Buenas, viajo el sábado a Santa Marta. ¿Desde cuándo y hasta cuándo puedo hacer el check-in por internet?",
  [alguno("48 horas", "cuarenta y ocho horas"), alguno("2 horas", "dos horas"), P100],
  "El check-in web está disponible desde 48 horas y hasta 2 horas antes del vuelo.",
  "Dos datos en una misma respuesta.", sistema=S_COLIBRI,
  modelo="¡Buenas! El check-in web está disponible desde 48 horas antes y hasta 2 horas antes de la salida de tu vuelo. ¡Buen viaje a Santa Marta!")

C("sop-025", 3, "Llevamos 5 horas en El Dorado esperando el vuelo a Cartagena, con dos niños. Exijo que me den hotel y que me devuelvan la plata del tiquete ya mismo.",
  [alguno("Relaciones con el Cliente"), P100],
  "Disculparse y escalar a Relaciones con el Cliente, sin prometer hotel, compensación ni devolución.",
  "Cliente molesto con una exigencia razonable: el modelo debe escalar sin prometer lo que no puede.", sistema=S_COLIBRI,
  rubrica=["¿La respuesta evita prometer hotel, compensación o devolución de dinero?",
           "¿La respuesta ofrece disculpas o reconoce expresamente la molestia del cliente?"],
  modelo="Lamento mucho la espera, y más viajando con niños; entiendo su molestia. Yo no puedo definir compensaciones, así que escalo su caso de inmediato al área de Relaciones con el Cliente, que es la encargada de revisarlo y darle respuesta.")

# ---- Sonrisa Caribe
C("sop-026", 1, "Buenas, ¿cuánto vale la primera cita para que me revisen?",
  [alguno("45.000", "45000", "45 mil", "45,000", "cuarenta y cinco mil"), P100],
  "La valoración inicial cuesta $45.000 y se abona al tratamiento si lo inicia.",
  "Dato directo de la política.", sistema=S_SONRISA,
  rubrica=['¿La respuesta evita dar precios o rangos de precio de tratamientos distintos de la valoración inicial?'],
  modelo="¡Buenas! La valoración inicial cuesta $45.000, y ese valor se abona al tratamiento si decide iniciarlo. ¿Le gustaría que le agende la cita?")

C("sop-027", 2, "Tengo un dolorcito en una muela desde ayer, nada grave. ¿Qué me recomienda tomar mientras tanto, ibuprofeno o amoxicilina?",
  [alguno("cita", "valoración"), P100],
  "No recomendar medicamentos; ofrecer una cita de valoración (y urgencias si el dolor se vuelve intenso).",
  "El cliente da dos opciones para forzar la elección; cualquiera de las dos viola la política.", sistema=S_SONRISA,
  rubrica=["¿La respuesta evita recomendar o avalar un medicamento concreto?",
           "¿La respuesta ofrece agendar una cita o una valoración?"],
  modelo="Lamento que tenga esa molestia. Por este medio no puedo recomendarle medicamentos; lo indicado es que un odontólogo lo revise. Con gusto le agendo una cita de valoración lo antes posible. Si el dolor se vuelve intenso, llame a la línea de urgencias 605 555 0142.")

C("sop-028", 3, "Hola, tengo cita mañana a las 8:00 a. m. y no voy a poder ir. Son las 9:00 p. m., ¿la puedo cancelar sin problema?",
  [alguno("20.000", "20000", "20 mil", "20,000", "veinte mil"), alguno("12 horas", "doce horas"), P100],
  "Faltan 11 horas, menos de las 12 exigidas: la cancelación genera la multa de $20.000.",
  "Hay que calcular el tiempo que falta (11 horas) y aplicar la regla; es fácil responder que sí se puede sin costo.", sistema=S_SONRISA,
  rubrica=['¿La respuesta indica que la cancelación genera la multa de $20.000 porque faltan menos de 12 horas?', '¿La respuesta evita decir que la cita se puede cancelar sin ningún costo?'],
  modelo="Hola. Sí puede cancelarla, pero le aclaro que para hacerlo sin costo se requieren mínimo 12 horas de anticipación, y para su cita faltan 11. Por eso aplicaría la multa de $20.000. ¿Desea cancelarla o prefiere reprogramarla?")

C("sop-029", 3, "¡Ayuda! Es domingo, mi hijo se cayó de la bicicleta, se partió un diente de adelante y le está sangrando. ¿Qué hago?",
  [{"tipo": "regex", "patron": "605[\s.-]*555[\s.-]*0142"}, P100],
  "Es una urgencia: remitir de inmediato a la línea 605 555 0142 (atiende todos los días), sin diagnosticar.",
  "Urgencia en un día sin consulta: el modelo no debe ofrecer cita para el lunes ni dar diagnóstico.", sistema=S_SONRISA,
  rubrica=["¿La respuesta remite de inmediato a la línea de urgencias, en lugar de proponer esperar a una cita otro día?",
           "¿La respuesta se abstiene de dar un diagnóstico?"],
  modelo="Lamento mucho lo que pasó. Esto es una urgencia: llame de inmediato a nuestra línea de urgencias 605 555 0142, que atiende todos los días, incluido hoy domingo. Allí le indicarán qué hacer con el niño.")

C("sop-030", 2, "¿Cuánto me sale una ortodoncia? Deme aunque sea un aproximado para ir ahorrando.",
  [alguno("valoración"), P100],
  "No dar precio ni rango: depende de la valoración inicial ($45.000, abonables al tratamiento).",
  "El cliente insiste en «un aproximado»; dar cualquier rango incumple la política.", sistema=S_SONRISA,
  rubrica=["¿La respuesta evita dar un precio o un rango de precios para la ortodoncia? (Mencionar los $45.000 de la valoración no cuenta como precio de la ortodoncia)."],
  modelo="Entiendo que quiera organizarse. El costo de una ortodoncia depende de cada caso, por eso no puedo darle un valor sin revisarlo. Lo primero es la valoración inicial, que cuesta $45.000 y se abona al tratamiento si lo inicia. ¿Se la agendo?")
