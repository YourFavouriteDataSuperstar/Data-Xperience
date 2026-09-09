# scripts/construir_cuaderno_07.py
"""Genera notebooks/07_proyecto_final_equilab.ipynb con nbformat.

El .ipynb se regenera desde aqui; no se edita a mano. Despues de correr este
script hay que ejecutar el cuaderno para que quede guardado con salidas:

    python3 scripts/construir_cuaderno_07.py
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    jupyter nbconvert --to notebook --execute --inplace \
      --ExecutePreprocessor.timeout=900 notebooks/07_proyecto_final_equilab.ipynb
"""
from pathlib import Path
import nbformat as nbf

NB = Path(__file__).resolve().parents[1] / "notebooks/07_proyecto_final_equilab.ipynb"
URL = ("https://raw.githubusercontent.com/YourFavouriteDataSuperstar/"
       "Data-Xperience/main/notebooks/data/geih_equilab_2021_2026.parquet")

AZUL, CLARO, ACENTO, TEXTO_CLARO = "#0B4F6C", "#D6EEF6", "#8FD3E8", "#C9E7F2"


def md(texto):
    return nbf.v4.new_markdown_cell(texto)


def code(fuente):
    return nbf.v4.new_code_cell(fuente.replace("__BASE__", URL))


def bloque_oscuro(titulo, bajada, pastillas=()):
    chips = ""
    for i, (texto, blanca) in enumerate(pastillas):
        fondo = "#FFFFFF" if blanca else ACENTO
        margen = "" if i == 0 else "margin-left:6px;"
        chips += (f'<span style="background:{fondo};color:{AZUL};padding:5px 14px;'
                  f'border-radius:14px;font-size:12px;font-weight:700;{margen}">{texto}</span>')
    return (f'<div style="background:{AZUL};border-radius:12px;padding:32px 28px;margin:14px 0;">\n'
            f'  <div style="color:{ACENTO};font-size:13px;letter-spacing:5px;font-weight:700;">DATAXPERIENCE</div>\n'
            f'  <div style="color:#FFFFFF;font-size:38px;font-weight:800;line-height:1.15;margin-top:8px;">{titulo}</div>\n'
            f'  <div style="color:{TEXTO_CLARO};font-size:16px;margin-top:12px;">{bajada}</div>\n'
            f'  <div style="margin-top:18px;">{chips}</div>\n'
            '</div>')


def encabezado(numero, titulo, bajada):
    return md(
        f'<div style="background:{CLARO};border-left:10px solid {AZUL};border-radius:8px;'
        'padding:18px 22px;margin:26px 0 8px 0;">\n'
        f'  <div style="font-size:12px;letter-spacing:3px;font-weight:700;color:{AZUL};">SECCION {numero}</div>\n'
        f'  <div style="font-size:26px;font-weight:800;color:#083A50;margin-top:2px;">{titulo}</div>\n'
        f'  <div style="font-size:14px;color:#083A50;margin-top:6px;">{bajada}</div>\n'
        '</div>')


def bloque_claro(html):
    return md(f'<div style="background:{CLARO};border-left:6px solid {AZUL};'
              f'border-radius:8px;padding:18px 20px;margin:14px 0;font-size:15px;'
              f'color:#1A1A1A;line-height:1.6;">{html}</div>')


def tabla(encabezados, filas):
    """Tabla HTML en la paleta del curso, con filas alternadas."""
    out = ['<div style="overflow-x:auto;">',
           '<table style="width:100%;border-collapse:collapse;font-size:14px;">',
           f'  <tr style="background:{AZUL};color:#FFFFFF;">' +
           "".join(f'<th style="padding:10px;text-align:left;">{h}</th>' for h in encabezados) +
           '</tr>']
    for i, fila in enumerate(filas):
        fondo = ' style="background:#F4F6F8;color:#242B33;"' if i % 2 == 0 else ' style="color:#242B33;"'
        out.append(f'  <tr{fondo}>' +
                   "".join(f'<td style="padding:9px;vertical-align:top;">{c}</td>' for c in fila) +
                   '</tr>')
    out += ['</table>', '</div>']
    return "\n".join(out)


BADGE = (
    '<a href="https://colab.research.google.com/github/YourFavouriteDataSuperstar/'
    'Data-Xperience/blob/main/notebooks/07_proyecto_final_equilab.ipynb" target="_parent">\n'
    '  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>\n'
    '</a>')

celdas = []

# ---------------------------------------------------------------- portada ---
celdas.append(md(
    BADGE + "\n\n" +
    bloque_oscuro(
        "Proyecto final: Radar EAN de brechas laborales",
        "Cinco equipos, cinco poblaciones, un solo programa que financiar. "
        "Analisis de brechas laborales de la GEIH del DANE (2021-2026) con SQL sobre DuckDB.",
        pastillas=[("NIVEL: AVANZADO", True),
                   ("PESO: 60 % DEL CORTE 2", False),
                   ("SQL + DATOS REALES", False)])))

celdas.append(md(
    "## Como usar este cuaderno\n"
    "\n"
    "Este cuaderno **es tu plantilla de trabajo, no un tutorial mas**. Trae tres cosas:\n"
    "un caso ya resuelto de punta a punta (secciones 3 y 4), el esqueleto vacio de tu\n"
    "propio analisis (seccion 5) y las herramientas para graficar y publicar (secciones 6 y 7).\n"
    "\n"
    "La regla de siempre se mantiene: **lee la explicacion, ejecuta la celda, cambia un\n"
    "valor y vuelve a ejecutar**. Pero aqui se le suma una segunda regla, la del proyecto:\n"
    "**cada cifra que escribas en tu sustentacion tiene que salir de una celda de este\n"
    "cuaderno que se pueda volver a ejecutar delante del comite**. Si no la puedes\n"
    "reproducir, no la reportes.\n"
    "\n" +
    tabla(["Aspecto", "Detalle"], [
        ("<b>Requisitos previos</b>",
         "Cuadernos 05 y 06 (limpieza de datos con la GEIH) y la clase de bases de datos "
         "relacionales y SQL. Debes manejar <code>SELECT</code>, <code>WHERE</code>, "
         "<code>GROUP BY</code>, <code>HAVING</code> y <code>CASE WHEN</code>."),
        ("<b>Librerias</b>",
         "<code>duckdb</code> (se instala en la seccion 1), <code>pandas</code> y "
         "<code>matplotlib</code> (ya vienen en Colab)."),
        ("<b>Datos</b>",
         "Un solo archivo parquet publicado en el repo del curso: 4.772.421 filas de la "
         "GEIH, 2021 a 2026, con el factor de expansion ya calculado. No hay que limpiar nada."),
        ("<b>Entrega</b>",
         "Una sola: este cuaderno completado por el equipo, mas una sustentacion de 8 a 10 "
         "minutos. No hay avances ni fases."),
    ])))

# --------------------------------------------------------------- seccion 0 ---
celdas.append(encabezado(
    0, "El reto",
    "Que se les pide, a quien defienden, que preguntas tienen que responder y como se califica."))

celdas.append(md(
    "### La situacion\n"
    "\n"
    "**Equilab** es un observatorio de datos sobre desigualdad en el mercado laboral\n"
    "colombiano. Para 2027 tiene presupuesto para financiar **un solo** programa de\n"
    "empleabilidad, y no le alcanza para mas. Convoco un comite para decidir a que\n"
    "poblacion dirigirlo.\n"
    "\n"
    "Cada equipo del curso llega a ese comite a **defender a una poblacion distinta**, con\n"
    "evidencia de la GEIH. No se trata de opinar sobre quien la tiene mas dificil: se trata\n"
    "de mostrar, con cifras que aguanten preguntas incomodas, por que esa poblacion deberia\n"
    "quedarse con el programa. **La clase decide en la sustentacion.**\n"
    "\n"
    "La pregunta madre es la misma para los cinco equipos. Lo unico que cambia es la\n"
    "poblacion.\n"
    "\n" +
    tabla(["Equipo", "Poblacion", "Columna en la base", "Lo que les va a costar"], [
        ("1", "Mujeres", "<code>mujer</code>",
         "Paradoja: su informalidad es <b>menor</b> que la de los hombres. Si no desarman "
         "esa cifra, van a concluir que no hay brecha."),
        ("2", "Jovenes (14 a 28 anos)", "<code>joven</code>",
         "Brecha limpia. Es el caso mas accesible de los cinco, asi que el liston de "
         "profundidad les queda mas alto."),
        ("3", "Personas racializadas", "<code>racializada</code>",
         "La brecha mas grande, con muestra amplia. El reto es explicar de donde sale, "
         "no encontrarla."),
        ("4", "Personas LGBTIQ+", "<code>lgbtiq</code>",
         "Segunda paradoja <b>y</b> muestra chica: van a chocar de verdad con el chequeo "
         "de tamano de muestra."),
        ("5", "Personas con discapacidad", "<code>discapacidad</code>",
         "Brecha grande sobre una poblacion que casi no se trabaja en clase. Poca "
         "referencia previa, mucho por decir."),
    ]) +
    "\n\n"
    "La **poblacion migrante** no esta en el reparto: es el caso que este cuaderno resuelve\n"
    "de ejemplo en las secciones 3 y 4. Asi ven el flujo completo, con la trampa incluida,\n"
    "sin que ningun equipo reciba servida su propia respuesta."))

celdas.append(md(
    "### Las seis preguntas obligatorias\n"
    "\n"
    "Son las mismas para los cinco equipos, y el cuaderno que entreguen tiene que\n"
    "responderlas todas, en este orden.\n"
    "\n" +
    tabla(["#", "Pregunta", "Que tiene que traer la respuesta"], [
        ("1", "<b>Cuantas personas son?</b>",
         "La magnitud expandida con <code>fex</code> y los registros que la sustentan."),
        ("2", "<b>Como les va?</b>",
         "Informalidad (obligatoria) mas <b>dos</b> indicadores a eleccion entre salario "
         "por hora, contrato escrito, cotizacion a pension y subempleo, siempre comparados "
         "contra el resto de la poblacion ocupada."),
        ("3", "<b>La brecha es real o es composicion?</b>",
         "Rehacer la comparacion controlando por al menos una variable: edad, nivel "
         "educativo o zona. <b>Es el criterio que separa Destacado de Competente.</b>"),
        ("4", "<b>Como cambio entre 2021 y 2025?</b>",
         "La serie ano a ano, con los registros de cada ano al lado."),
        ("5", "<b>Donde es peor?</b>",
         "Corte territorial con el chequeo de muestra activo."),
        ("6", "<b>La recomendacion</b>",
         "Por que su poblacion, y <b>que no pueden afirmar</b> con estos datos."),
    ])))

celdas.append(bloque_claro(
    "<b>Las dos reglas de rigor. No son negociables.</b>"
    "<ol>"
    "<li><b>Ponderar siempre con <code>fex</code>.</b> La GEIH es una muestra: cada persona "
    "encuestada representa a muchas otras, y ese peso es <code>fex</code>. Toda cifra se "
    "calcula como <code>sum(fex * x) / sum(fex)</code>. Un promedio crudo "
    "(<code>avg(x)</code>) sobre datos de encuesta esta mal, aunque el numero se vea "
    "razonable. En la seccion 2 lo vas a ver con tus propios ojos.</li>"
    "<li><b>Chequeo de muestra.</b> Toda cifra va acompanada de su <code>count(*)</code>: "
    "cuantos encuestados reales hay detras. <b>Por debajo de 100 registros la cifra no se "
    "reporta sin advertencia explicita.</b> En SQL eso se escribe "
    "<code>HAVING count(*) &gt;= 100</code>, y en una grafica se escribe poniendo el "
    "<code>n=</code> en cada barra.</li>"
    "</ol>"
    "Un numero sin ponderar o sin registros al lado no es un hallazgo: es un error que "
    "todavia no se noto."))

celdas.append(md(
    "### Como se califica\n"
    "\n"
    "Cuatro criterios sobre 100 puntos, con los cuatro niveles del syllabus\n"
    "(Destacado / Competente / Basico / No competente).\n"
    "\n" +
    tabla(["Criterio", "Peso", "Que se evalua"], [
        ("Rigor con datos de encuesta y SQL", "<b>30</b>",
         "Ponderacion con <code>fex</code> - registros reportados - advertencia de muestra "
         "chica - consultas que responden lo que dicen responder."),
        ("Analisis y hallazgos", "<b>25</b>",
         "Las seis preguntas con evidencia. <b>Un equipo que reporte la cifra cruda como si "
         "fuera la brecha no llega a Destacado.</b>"),
        ("Visualizacion", "<b>20</b>",
         "Graficos correctos, etiquetados y honestos (clase 19)."),
        ("Comunicacion y sustentacion", "<b>25</b>",
         "Narrativa (clase 15), recomendacion al comite y limites de lo que se puede afirmar."),
    ]) +
    "\n\n"
    "**Entregables:** el cuaderno completado y una sustentacion de **8 a 10 minutos**. Sin\n"
    "dashboard, sin informe aparte, sin entregas parciales: una sola entrega que se califica\n"
    "completa con los cuatro criterios.\n"
    "\n"
    "**Puntos extra (opcionales, por fuera de los 100):** publicar el analisis como sitio web\n"
    "con Quarto. La receta esta en la seccion 7."))

celdas.append(md(
    "### Mapa del cuaderno\n"
    "\n" +
    tabla(["Seccion", "Que hay ahi", "Que haces tu"], [
        ("0", "El reto, el reparto, las seis preguntas y la rubrica", "Leer"),
        ("1", "Conexion a la base ya resuelta", "Ejecutar"),
        ("2", "La regla de oro: sin ponderar contra ponderado", "Ejecutar y entender"),
        ("3", "Caso resuelto (poblacion migrante): las seis preguntas", "Leer el codigo, imitarlo"),
        ("4", "La trampa de composicion, demostrada con datos", "Leer con cuidado: aqui se gana el Destacado"),
        ("5", "<b>El esqueleto de tu analisis</b>", "<b>Aqui trabajas</b>"),
        ("6", "De SQL a grafica, y exportar resultados", "Adaptar a tu poblacion"),
        ("7", "El plus: publicar con Quarto", "Opcional, puntos extra"),
    ])))

# --------------------------------------------------------------- seccion 1 ---
celdas.append(encabezado(
    1, "Conexion a la base",
    "Instalar DuckDB, traer el parquet una sola vez y darle el primer vistazo."))

celdas.append(md(
    "En los cuadernos 05 y 06 leimos un CSV con pandas. Aqui no: la base del proyecto tiene\n"
    "**4.772.421 filas** y seis anos de encuesta, y la vamos a consultar con **SQL**, que es\n"
    "donde termina el arco de herramientas del curso.\n"
    "\n"
    "**DuckDB** es una base de datos que no hay que instalar en ningun servidor: vive dentro\n"
    "de tu sesion de Python, entiende SQL estandar y lee archivos **parquet** directamente,\n"
    "incluso por URL. El parquet es un formato columnar y comprimido: estos mismos datos\n"
    "guardados en CSV ocupan 800 MB, y en parquet ocupan 45.\n"
    "\n"
    "Cada consulta devuelve un `DataFrame` de pandas con `.df()`, asi que todo lo que ya\n"
    "sabes hacer con pandas y matplotlib sigue sirviendo."))

celdas.append(code(
    "# Colab no trae DuckDB preinstalado. Esta celda lo instala (tarda unos segundos).\n"
    "# %pip es la forma correcta dentro de un cuaderno: instala en el mismo\n"
    "# entorno donde corre este kernel, no en otro Python del sistema.\n"
    "%pip install -q duckdb\n"
    "\n"
    "import duckdb\n"
    "print(\"duckdb\", duckdb.__version__)"))

celdas.append(md(
    "Ahora abrimos una conexion en memoria y le damos el primer vistazo al archivo. La\n"
    "extension `httpfs` es la que le permite a DuckDB leer por HTTP."))

celdas.append(code(
    'BASE = "__BASE__"\n'
    "\n"
    "con = duckdb.connect()\n"
    'con.execute("INSTALL httpfs; LOAD httpfs;")\n'
    "\n"
    "# Apagamos la barra de progreso: se ve bien mientras corres, pero al guardar\n"
    "# el cuaderno deja basura en la salida. Quita esta linea si la prefieres.\n"
    'con.execute("SET enable_progress_bar = false")\n'
    "\n"
    "# Primer vistazo: cinco filas cualesquiera, leidas directo del URL.\n"
    "con.execute(f\"SELECT * FROM '{BASE}' LIMIT 5\").df()"))

celdas.append(bloque_claro(
    "<b>Un paso que te ahorra media clase.</b> Leer <code>FROM '{BASE}'</code> vuelve a "
    "descargar el archivo completo <b>en cada consulta</b>. Con una docena de consultas serian "
    "cientos de megas y una espera larguisima cada vez. La celda de abajo trae el archivo "
    "<b>una sola vez</b> y lo guarda como una tabla llamada <code>personas</code> dentro de la "
    "sesion.<br><br>"
    "A partir de ahi, todas las consultas del cuaderno dicen <code>FROM personas</code>: "
    "consultas una tabla, exactamente como en la clase de SQL. Si reinicias el entorno de "
    "Colab, vuelve a ejecutar esta celda."))

celdas.append(code(
    "# Materializamos la base UNA sola vez. Tarda entre 10 y 40 segundos segun la conexion.\n"
    "con.execute(f\"CREATE TABLE personas AS SELECT * FROM '{BASE}'\")\n"
    "\n"
    "con.execute(\"\"\"\n"
    "SELECT count(*) AS filas, min(anio) AS primer_anio, max(anio) AS ultimo_anio\n"
    "FROM personas\n"
    "\"\"\").df()"))

celdas.append(md(
    "Antes de consultar cualquier cosa conviene saber que columnas hay. `DESCRIBE` es la\n"
    "forma de preguntarselo a la base sin traer ni una fila de datos."))

celdas.append(code(
    'con.execute("DESCRIBE personas").df()'))

celdas.append(md(
    "Las que vas a usar todo el tiempo:\n"
    "\n" +
    tabla(["Columna", "Que es"], [
        ("<code>fex</code>", "Factor de expansion: cuantas personas representa cada encuestado. <b>Sin esto ninguna cifra es correcta.</b>"),
        ("<code>anio</code>, <code>mes</code>", "Periodo. 2026 solo tiene enero a junio."),
        ("<code>ocupado</code>", "1 si la persona tiene trabajo. Casi todos los indicadores laborales se calculan solo sobre ocupados."),
        ("<code>informal</code>", "1 si el empleo es informal. Es el indicador obligatorio de la pregunta 2."),
        ("<code>cotiza_pension</code>, <code>contrato_escrito</code>, <code>subempleo_horas</code>, <code>salario_hora</code>",
         "Los cuatro indicadores entre los que eliges dos."),
        ("<code>mujer</code>, <code>joven</code>, <code>racializada</code>, <code>lgbtiq</code>, <code>migrante</code>, <code>discapacidad</code>",
         "Las banderas de dimension. La de tu equipo esta aqui."),
        ("<code>zona</code>, <code>departamento</code>, <code>edad</code>, <code>educacion_superior</code>",
         "Las variables con las que se controla la composicion (pregunta 3) y se hace el corte territorial (pregunta 5)."),
    ])))

# --------------------------------------------------------------- seccion 2 ---
celdas.append(encabezado(
    2, "La regla de oro: ponderar con fex",
    "La misma cifra, calculada de las dos maneras, lado a lado."))

celdas.append(md(
    "La GEIH no le pregunta a los 52 millones de colombianos: le pregunta a una muestra. Para\n"
    "que esa muestra represente al pais, el DANE le asigna a cada encuestado un **factor de\n"
    "expansion** (`fex`): el numero de personas que esa respuesta representa.\n"
    "\n"
    "Y no todos pesan igual, ni de lejos. En esta base el encuestado tipico representa a unas\n"
    "26 personas, pero el 5 % de menor peso representa a menos de 5 cada uno, y el 5 % de\n"
    "mayor peso, a mas de 260. Un solo registro puede valer por mas de tres mil personas.\n"
    "\n"
    "Por eso un promedio crudo esta mal: le da el mismo peso a una respuesta que vale por 5\n"
    "personas y a una que vale por 260. La formula correcta es siempre la misma:\n"
    "\n"
    "```sql\n"
    "sum(fex * indicador) / sum(fex)\n"
    "```\n"
    "\n"
    "La celda de abajo calcula la informalidad nacional de 2025 de las dos maneras."))

celdas.append(code(
    'con.execute("""\n'
    "SELECT round(100 * avg(informal), 1)                  AS sin_ponderar,\n"
    "       round(100 * sum(fex * informal) / sum(fex), 1) AS ponderado,\n"
    "       count(*)                                       AS registros\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND ocupado = 1\n"
    '""").df()'))

celdas.append(md(
    "**Casi un punto porcentual de diferencia** entre las dos columnas, sobre una poblacion de\n"
    "cientos de miles de registros. Ese punto no es ruido: es el efecto de que la muestra no\n"
    "esta repartida igual que la poblacion, y aparece porque la informalidad no se distribuye\n"
    "igual en las zonas sobremuestreadas que en las submuestreadas.\n"
    "\n"
    "Y esa brecha crece cuando el grupo que analizas esta concentrado en pocas regiones, que\n"
    "es justo el caso de varias de las poblaciones del reparto. **Reportar la columna\n"
    "`sin_ponderar` es reportar una cifra que no corresponde a ninguna poblacion real.**\n"
    "\n"
    "La tercera columna, `registros`, es la otra mitad de la regla: son los encuestados que\n"
    "hay detras de la cifra. Con 358.029 registros, la informalidad nacional es solidisima.\n"
    "Cuando bajes a una poblacion especifica en un departamento especifico, ese numero se va\n"
    "a caer rapido. **Por debajo de 100 registros la cifra no se reporta sin advertencia.**"))

# --------------------------------------------------------------- seccion 3 ---
celdas.append(encabezado(
    3, "Caso resuelto: la poblacion migrante",
    "Las seis preguntas respondidas de punta a punta, para que copies el flujo, no la respuesta."))

celdas.append(md(
    "Vamos a hacer completo el analisis de una poblacion que **no le toco a nadie**: las\n"
    "personas migrantes. Asi ves el camino entero -- incluida la trampa de la seccion 4 --\n"
    "sin que ningun equipo se lleve resuelto su propio caso.\n"
    "\n"
    "Lee cada consulta pensando en la tuya: lo unico que vas a cambiar es la columna de la\n"
    "dimension y, si quieres, los dos indicadores de la pregunta 2."))

celdas.append(md(
    "#### Pregunta 1. Cuantas personas son?\n"
    "\n"
    "Dos numeros distintos que nunca hay que confundir: `sum(fex)` da **personas** (la\n"
    "poblacion que representan), `count(*)` da **registros** (los encuestados reales). El\n"
    "primero es el que va en la sustentacion; el segundo es el que dice si el primero se\n"
    "puede creer."))

celdas.append(code(
    'con.execute("""\n'
    "SELECT round(sum(fex))                                 AS personas,\n"
    "       count(*)                                        AS registros,\n"
    "       round(sum(CASE WHEN ocupado = 1 THEN fex END))  AS ocupados\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND migrante = 1\n"
    '""").df()'))

celdas.append(md(
    "**633.137 personas migrantes en 2025**, de las cuales **291.818 estan ocupadas**, y todo\n"
    "eso sale de **8.419 encuestados**. Fijate en la proporcion: cada registro esta\n"
    "representando a unas 75 personas. Por eso `count(*)` importa tanto -- si esos 8.419\n"
    "fueran 84, la misma consulta devolveria un numero parecido y seria basura."))

celdas.append(md(
    "#### Pregunta 2. Como les va?\n"
    "\n"
    "La informalidad es obligatoria; aqui la acompanamos con cotizacion a pension y contrato\n"
    "escrito. Lo importante del diseno de esta consulta es el `CASE WHEN` del `GROUP BY`:\n"
    "**parte la poblacion ocupada en dos y calcula todo para los dos grupos a la vez**, para\n"
    "que la comparacion sea contra el resto de la poblacion y no contra una cifra suelta que\n"
    "alguien recuerda de una noticia."))

celdas.append(code(
    'con.execute("""\n'
    "SELECT CASE WHEN migrante = 1 THEN 'Migrante' ELSE 'Resto' END AS grupo,\n"
    "       count(*)                                         AS registros,\n"
    "       round(100 * sum(fex * informal) / sum(fex), 1)    AS informal_pct,\n"
    "       round(100 * sum(fex * cotiza_pension) / sum(fex), 1)   AS pension_pct,\n"
    "       round(100 * sum(fex * contrato_escrito) / sum(fex), 1) AS contrato_pct\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND ocupado = 1\n"
    "GROUP BY 1\n"
    '""").df()'))

celdas.append(md(
    "La brecha es enorme y va en la misma direccion en los tres indicadores:\n"
    "\n"
    "- **Informalidad: 87,8 % contra 54,9 %.** Casi nueve de cada diez personas migrantes\n"
    "  ocupadas trabajan en la informalidad.\n"
    "- **Cotizacion a pension: 12,2 % contra 43,6 %.** Menos de una de cada ocho esta\n"
    "  construyendo una pension.\n"
    "- **Contrato escrito: 14,5 % contra 40,2 %.**\n"
    "\n"
    "Los registros aguantan: 3.611 encuestados migrantes ocupados y 354.418 en el resto.\n"
    "\n"
    "Ojo con la redaccion: esto dice **que** la brecha existe, no **por que**. La respuesta a\n"
    "esa segunda pregunta es la seccion 4, y es la que decide la nota."))

celdas.append(md(
    "#### Pregunta 3. La brecha es real o es composicion?\n"
    "\n"
    "Esta pregunta tiene seccion propia, la **seccion 4**, porque es la que separa un trabajo\n"
    "Destacado de uno Competente. La respondemos alla, con las dos consultas que hacen falta."))

celdas.append(md(
    "#### Pregunta 4. Como cambio entre 2021 y 2025?\n"
    "\n"
    "Una serie de tiempo se pide agrupando por `anio`. Y como en toda cifra de este cuaderno,\n"
    "el `count(*)` viaja al lado -- en una serie es incluso mas importante, porque lo que\n"
    "cambia entre anos puede ser la realidad **o puede ser la muestra**."))

celdas.append(code(
    'con.execute("""\n'
    "SELECT anio,\n"
    "       count(*)                                      AS registros,\n"
    "       round(100 * sum(fex * informal) / sum(fex), 1) AS informal_pct\n"
    "FROM personas\n"
    "WHERE ocupado = 1 AND migrante = 1\n"
    "GROUP BY 1\n"
    "ORDER BY 1\n"
    '""").df()'))

celdas.append(bloque_claro(
    "<b>Leer esta tabla al derecho es el ejercicio.</b> La informalidad se mueve poco: 88,8 en "
    "2022, baja a 85,0 en 2023, vuelve a 87,8 en 2025. Pero mira la columna de registros: "
    "<b>13.241 en 2022 y 3.611 en 2025</b>. La muestra se redujo a la cuarta parte, y la serie "
    "<b>no empieza en 2021</b>: ese ano la pregunta de migracion no existia en la encuesta.<br><br>"
    "Esa caida no es que haya menos personas migrantes trabajando en Colombia; es un cambio en "
    "la cobertura de la pregunta. Por eso esta poblacion <b>no esta en el reparto de equipos</b>: "
    "cualquier historia sobre 'la tendencia' aqui seria enganosa. Con tu poblacion revisa lo "
    "mismo antes de narrar una tendencia: si los registros se mueven mucho entre anos, el "
    "hallazgo puede estar en la encuesta y no en el mercado laboral."))

celdas.append(md(
    "#### Pregunta 5. Donde es peor?\n"
    "\n"
    "El corte territorial es donde el chequeo de muestra deja de ser teoria. Los 3.611\n"
    "registros de personas migrantes ocupadas se reparten en 31 departamentos, y **16 de\n"
    "esos 31 quedan por debajo de 100 encuestados**: cifras que se mueven enteras si una\n"
    "sola persona hubiera respondido distinto.\n"
    "\n"
    "`HAVING count(*) >= 100` es el chequeo de muestra escrito en SQL. `WHERE` filtra filas\n"
    "**antes** de agrupar; `HAVING` filtra grupos **despues** de agrupar, que es justo lo que\n"
    "necesitamos: descartar los departamentos cuya cifra no se sostiene."))

celdas.append(code(
    'con.execute("""\n'
    "SELECT departamento,\n"
    "       count(*)                                      AS registros,\n"
    "       round(100 * sum(fex * informal) / sum(fex), 1) AS informal_pct\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND ocupado = 1 AND migrante = 1\n"
    "GROUP BY 1\n"
    "HAVING count(*) >= 100\n"
    "ORDER BY 3 DESC\n"
    "LIMIT 6\n"
    '""").df()'))

celdas.append(md(
    "**La Guajira, 98,4 % de informalidad** entre personas migrantes ocupadas, con 187\n"
    "registros detras. Le siguen Vichada (98,2 %, n=115) y Magdalena (97,0 %, n=100). Es\n"
    "practicamente la totalidad de la poblacion migrante ocupada de esos departamentos\n"
    "trabajando sin proteccion.\n"
    "\n"
    "Prueba a quitar la linea del `HAVING` y volver a ejecutar. Van a aparecer de primeros\n"
    "**cinco departamentos con 100,0 % de informalidad** -- Arauca, Vaupes, Guainia, Putumayo\n"
    "y Choco -- desplazando a La Guajira. Miralos con calma: **Vaupes tiene un solo\n"
    "encuestado detras**, y Putumayo once. Ese 100 % no significa que alli la informalidad\n"
    "sea total; significa que la unica persona migrante ocupada que la encuesta alcanzo a\n"
    "entrevistar era informal.\n"
    "\n"
    "Esas cifras no son mas alarmantes: son menos confiables. Llevar una de ellas al comite\n"
    "es la forma mas rapida de perder el punto de rigor, porque es la primera que alguien va\n"
    "a querer verificar."))

celdas.append(md(
    "#### Pregunta 6. La recomendacion\n"
    "\n"
    "La escribimos al final de la seccion 4, cuando ya tengamos hecho el control de\n"
    "composicion. Antes de eso todavia no sabemos si la brecha que encontramos es real."))

# --------------------------------------------------------------- seccion 4 ---
celdas.append(encabezado(
    4, "La trampa de composicion",
    "Por que la cifra cruda puede mentir, y como se comprueba si esta mintiendo."))

celdas.append(md(
    "En la pregunta 2 encontramos que las personas migrantes ocupadas tienen 87,8 % de\n"
    "informalidad contra 54,9 % del resto. Antes de llevar eso a un comite hay que hacerse\n"
    "una pregunta incomoda:\n"
    "\n"
    "> **Estamos comparando dos grupos comparables?**\n"
    "\n"
    "Si un grupo es sistematicamente mas joven, o vive mas en ciudades, o tiene menos\n"
    "educacion superior, entonces parte de la diferencia que vemos no se debe a **ser** de ese\n"
    "grupo, sino a esas otras caracteristicas. A eso se le llama **efecto de composicion**.\n"
    "\n"
    "Empecemos por mirar en que se diferencian los dos grupos, mas alla de la informalidad."))

celdas.append(code(
    'con.execute("""\n'
    "SELECT CASE WHEN migrante = 1 THEN 'Migrante' ELSE 'Resto' END AS grupo,\n"
    "       round(100 * sum(CASE WHEN zona = 'Urbano' THEN fex END) / sum(fex), 1)          AS pct_urbano,\n"
    "       round(100 * sum(CASE WHEN educacion_superior = 1 THEN fex END) / sum(fex), 1)   AS pct_superior,\n"
    "       round(sum(fex * edad) / sum(fex), 1)                                            AS edad_promedio\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND ocupado = 1\n"
    "GROUP BY 1\n"
    '""").df()'))

celdas.append(md(
    "Los dos grupos **no son comparables de entrada**:\n"
    "\n"
    "- La poblacion migrante ocupada es **mas urbana**: 90,2 % contra 79,5 %.\n"
    "- Tiene **menos educacion superior**: 19,3 % contra 33,6 %.\n"
    "- Es **casi diez anos mas joven**: 31,8 anos contra 41,1.\n"
    "\n"
    "Cada una de esas tres cosas empuja la informalidad por su cuenta. Entonces la pregunta\n"
    "correcta ya no es *cuanta informalidad tienen las personas migrantes*, sino: **entre\n"
    "personas parecidas, sigue habiendo brecha?**\n"
    "\n"
    "La forma mas simple de responderlo es rehacer la misma comparacion **dentro de cada\n"
    "grupo parecido**: agregar la variable de control al `GROUP BY`. Aqui controlamos por\n"
    "zona."))

celdas.append(code(
    'con.execute("""\n'
    "SELECT zona,\n"
    "       CASE WHEN migrante = 1 THEN 'Migrante' ELSE 'Resto' END AS grupo,\n"
    "       count(*)                                      AS registros,\n"
    "       round(100 * sum(fex * informal) / sum(fex), 1) AS informal_pct\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND ocupado = 1\n"
    "GROUP BY 1, 2\n"
    "ORDER BY 1, 2\n"
    '""").df()'))

celdas.append(bloque_claro(
    "<b>Aqui esta la leccion completa, y es la que sostiene el criterio de Destacado.</b><br><br>"
    "La brecha cruda era de 87,8 contra 54,9: <b>33 puntos</b>. Al comparar solo dentro de lo "
    "urbano, queda en <b>87,1 contra 47,5: casi 40 puntos</b>. Y dentro de lo rural, 94,5 contra "
    "83,4.<br><br>"
    "O sea que la brecha <b>no solo sobrevive el control: se agranda</b>. Estaba parcialmente "
    "<i>escondida</i> por la composicion, porque la poblacion migrante se concentra en zonas "
    "urbanas, que son justamente las de menor informalidad. <b>Esta brecha es real.</b><br><br>"
    "<b>Y ahora la advertencia que te toca a ti:</b> no siempre pasa esto. Hay poblaciones donde "
    "la brecha cruda <b>se desarma</b> al controlar, y otras donde cambia de signo. Descubrir "
    "cual de los tres casos es el tuyo -- y decirlo -- es exactamente lo que se califica. Un "
    "equipo que reporte la cifra cruda como si fuera la brecha no llega a Destacado, aunque la "
    "cifra este bien calculada."))

celdas.append(md(
    "#### Pregunta 6. La recomendacion (el cierre del caso resuelto)\n"
    "\n"
    "Asi se veria el parrafo final de este caso ante el comite. Fijate en la estructura:\n"
    "magnitud, brecha, control, y **el limite**.\n"
    "\n"
    "> Recomendamos dirigir el programa a la poblacion migrante ocupada. Son 291.818 personas\n"
    "> ocupadas en 2025, respaldadas por 3.611 registros. Su informalidad es de 87,8 % frente\n"
    "> a 54,9 % del resto de la poblacion ocupada, y solo 12,2 % cotiza a pension. Esa brecha\n"
    "> **no se explica por donde viven**: al comparar unicamente dentro de la zona urbana, la\n"
    "> distancia crece de 33 a casi 40 puntos. El corte territorial concentra el problema en\n"
    "> La Guajira (98,4 %, n=187), Vichada (98,2 %, n=115) y Magdalena (97,0 %, n=100).\n"
    ">\n"
    "> **Lo que no podemos afirmar con estos datos:** (1) no podemos hablar de tendencia entre\n"
    "> 2021 y 2025, porque la variable no existe en 2021 y la muestra cae de 13.241 a 3.611\n"
    "> registros por un cambio de cobertura de la encuesta; (2) no podemos afirmar\n"
    "> causalidad -- controlamos por zona, no por sector economico, tiempo de residencia ni\n"
    "> estatus migratorio, que no estan en esta base; (3) no podemos decir nada de los\n"
    "> departamentos que quedaron por debajo de 100 registros.\n"
    "\n"
    "Esos tres limites no restan puntos: **son** puntos. Un equipo que dice con precision que\n"
    "no puede afirmar demuestra que entendio sus datos."))

# --------------------------------------------------------------- seccion 5 ---
celdas.append(encabezado(
    5, "El esqueleto de tu analisis",
    "Las seis preguntas, con las consultas a medio armar. Aqui trabaja tu equipo."))

celdas.append(bloque_claro(
    '<div style="font-size:19px;font-weight:800;color:#0B4F6C;margin-bottom:8px;">'
    'LO PRIMERO: CAMBIA <code>MI_DIMENSION</code> POR LA COLUMNA DE TU EQUIPO</div>'
    "Las seis celdas de esta seccion usan la misma variable <code>MI_DIMENSION</code>, declarada "
    "<b>una sola vez</b> en la celda de abajo. Cambias ese valor y todo tu analisis corre con tu "
    "poblacion.<br><br>"
    "Viene con <code>\"migrante\"</code> puesto <b>solo para que veas las celdas funcionando</b>: "
    "esa es la poblacion del caso resuelto y <b>no le toca a ningun equipo</b>. Si entregas el "
    "cuaderno con <code>\"migrante\"</code>, entregaste el ejemplo, no tu trabajo.<br><br>"
    '<table style="width:100%;border-collapse:collapse;font-size:14px;margin-top:6px;">'
    f'<tr style="background:{AZUL};color:#FFFFFF;">'
    '<th style="padding:8px;text-align:left;">Equipo</th>'
    '<th style="padding:8px;text-align:left;">Tu poblacion</th>'
    '<th style="padding:8px;text-align:left;">Escribe exactamente</th></tr>'
    '<tr style="background:#FFFFFF;"><td style="padding:8px;">1</td><td style="padding:8px;">Mujeres</td><td style="padding:8px;"><code>"mujer"</code></td></tr>'
    '<tr><td style="padding:8px;">2</td><td style="padding:8px;">Jovenes (14 a 28)</td><td style="padding:8px;"><code>"joven"</code></td></tr>'
    '<tr style="background:#FFFFFF;"><td style="padding:8px;">3</td><td style="padding:8px;">Personas racializadas</td><td style="padding:8px;"><code>"racializada"</code></td></tr>'
    '<tr><td style="padding:8px;">4</td><td style="padding:8px;">Personas LGBTIQ+</td><td style="padding:8px;"><code>"lgbtiq"</code></td></tr>'
    '<tr style="background:#FFFFFF;"><td style="padding:8px;">5</td><td style="padding:8px;">Personas con discapacidad</td><td style="padding:8px;"><code>"discapacidad"</code></td></tr>'
    '</table><br>'
    "Debajo de cada celda de codigo hay una celda de texto para tu conclusion. "
    "<b>Un numero sin interpretacion no es una respuesta.</b>"))

celdas.append(code(
    "# ============================================================\n"
    "#  LA UNICA LINEA QUE CAMBIAS PARA CORRER TODO TU ANALISIS\n"
    "#  Opciones: mujer | joven | racializada | lgbtiq | discapacidad\n"
    "#  Viene con \"migrante\" (el caso resuelto). CAMBIALO.\n"
    "# ============================================================\n"
    'MI_DIMENSION = "migrante"\n'
    "\n"
    "print(\"Tu equipo analiza la columna:\", MI_DIMENSION)"))

celdas.append(md(
    "#### P1. Cuantas personas son?\n"
    "\n"
    "Magnitud expandida con `fex` y los registros que la sustentan. Modelo: seccion 3, P1."))

celdas.append(code(
    "con.execute(f\"\"\"\n"
    "SELECT round(sum(fex))                                AS personas,\n"
    "       count(*)                                       AS registros,\n"
    "       round(sum(CASE WHEN ocupado = 1 THEN fex END)) AS ocupados\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND {MI_DIMENSION} = 1\n"
    "\"\"\").df()"))

celdas.append(md("*Tu conclusion (una o dos frases):*"))

celdas.append(md(
    "#### P2. Como les va?\n"
    "\n"
    "Informalidad **obligatoria**, mas **dos** indicadores a eleccion:\n"
    "`salario_hora`, `contrato_escrito`, `cotiza_pension` o `subempleo_horas`. La consulta\n"
    "viene con dos puestos de ejemplo; cambialos si tu poblacion se explica mejor con otros.\n"
    "\n"
    "Ojo con `salario_hora`: no es una bandera 0/1 sino un valor en pesos, asi que su\n"
    "promedio ponderado se escribe `sum(fex * salario_hora) / sum(fex)`, **sin** el `100 *`."))

celdas.append(code(
    "con.execute(f\"\"\"\n"
    "SELECT CASE WHEN {MI_DIMENSION} = 1 THEN 'Mi poblacion' ELSE 'Resto' END AS grupo,\n"
    "       count(*)                                              AS registros,\n"
    "       round(100 * sum(fex * informal) / sum(fex), 1)         AS informal_pct,\n"
    "       round(100 * sum(fex * cotiza_pension) / sum(fex), 1)   AS pension_pct,\n"
    "       round(100 * sum(fex * contrato_escrito) / sum(fex), 1) AS contrato_pct\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND ocupado = 1\n"
    "GROUP BY 1\n"
    "\"\"\").df()"))

celdas.append(md("*Tu conclusion (una o dos frases):*"))

celdas.append(md(
    "#### P3. La brecha es real o es composicion?\n"
    "\n"
    "**Esta es la pregunta que decide tu nota de analisis.** Se responde en dos pasos:\n"
    "primero mirar en que se diferencian los dos grupos, y despues rehacer la comparacion\n"
    "**dentro** de grupos parecidos. La celda controla por `zona`; cambia esa variable por\n"
    "`educacion_superior`, o por tramos de edad, y compara los tres resultados.\n"
    "\n"
    "Modelo: seccion 4 completa."))

celdas.append(code(
    "# Paso 1: en que se diferencian los dos grupos, ademas de la informalidad\n"
    "con.execute(f\"\"\"\n"
    "SELECT CASE WHEN {MI_DIMENSION} = 1 THEN 'Mi poblacion' ELSE 'Resto' END AS grupo,\n"
    "       round(100 * sum(CASE WHEN zona = 'Urbano' THEN fex END) / sum(fex), 1)        AS pct_urbano,\n"
    "       round(100 * sum(CASE WHEN educacion_superior = 1 THEN fex END) / sum(fex), 1) AS pct_superior,\n"
    "       round(sum(fex * edad) / sum(fex), 1)                                          AS edad_promedio\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND ocupado = 1\n"
    "GROUP BY 1\n"
    "\"\"\").df()"))

celdas.append(code(
    "# Paso 2: la misma comparacion, pero dentro de cada grupo parecido\n"
    "# Cambia 'zona' por 'educacion_superior' y vuelve a ejecutar.\n"
    "CONTROL = \"zona\"\n"
    "\n"
    "con.execute(f\"\"\"\n"
    "SELECT {CONTROL},\n"
    "       CASE WHEN {MI_DIMENSION} = 1 THEN 'Mi poblacion' ELSE 'Resto' END AS grupo,\n"
    "       count(*)                                      AS registros,\n"
    "       round(100 * sum(fex * informal) / sum(fex), 1) AS informal_pct\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND ocupado = 1\n"
    "GROUP BY 1, 2\n"
    "ORDER BY 1, 2\n"
    "\"\"\").df()"))

celdas.append(bloque_claro(
    "<b>La respuesta correcta puede ser que no hay brecha.</b> Si al controlar la diferencia se "
    "encoge, desaparece o cambia de signo, <b>eso tambien es un hallazgo</b>, y bien contado vale "
    "tanto como una brecha grande. Lo que no vale es esconderlo: reportar la cifra cruda "
    "sabiendo que el control la desarma es justo lo que la rubrica castiga.<br><br>"
    "Si te pasa, tu recomendacion al comite cambia de forma -- ya no es 'esta poblacion esta "
    "peor', sino algo mas fino: donde si esta peor, o que subgrupo carga la brecha. Eso es "
    "trabajo de Destacado."))

celdas.append(md("*Tu conclusion (compara la cifra cruda con la controlada, y di cual de los tres casos es el tuyo):*"))

celdas.append(md(
    "#### P4. Como cambio entre 2021 y 2025?\n"
    "\n"
    "Y revisa la columna de registros antes de narrar cualquier tendencia: si la muestra se\n"
    "mueve mucho entre anos, el cambio puede estar en la encuesta y no en el mercado laboral."))

celdas.append(code(
    "con.execute(f\"\"\"\n"
    "SELECT anio,\n"
    "       count(*)                                      AS registros,\n"
    "       round(100 * sum(fex * informal) / sum(fex), 1) AS informal_pct\n"
    "FROM personas\n"
    "WHERE ocupado = 1 AND {MI_DIMENSION} = 1\n"
    "GROUP BY 1\n"
    "ORDER BY 1\n"
    "\"\"\").df()"))

celdas.append(md("*Tu conclusion (una o dos frases):*"))

celdas.append(md(
    "#### P5. Donde es peor?\n"
    "\n"
    "Corte territorial **con el chequeo de muestra activo**. El `HAVING count(*) >= 100` no se\n"
    "quita: se deja y, si tu poblacion es chica, se reporta cuantos departamentos quedaron\n"
    "fuera por ese filtro. Eso ultimo tambien es un hallazgo."))

celdas.append(code(
    "con.execute(f\"\"\"\n"
    "SELECT departamento,\n"
    "       count(*)                                      AS registros,\n"
    "       round(100 * sum(fex * informal) / sum(fex), 1) AS informal_pct\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND ocupado = 1 AND {MI_DIMENSION} = 1\n"
    "GROUP BY 1\n"
    "HAVING count(*) >= 100\n"
    "ORDER BY 3 DESC\n"
    "LIMIT 10\n"
    "\"\"\").df()"))

celdas.append(md("*Tu conclusion (una o dos frases):*"))

celdas.append(md(
    "#### P6. La recomendacion\n"
    "\n"
    "No lleva SQL: lleva criterio. Escribe abajo el parrafo que van a decir ante el comite.\n"
    "Modelo: el cierre de la seccion 4.\n"
    "\n"
    "Tiene que traer, en este orden:\n"
    "\n"
    "1. **La magnitud**, expandida y con sus registros.\n"
    "2. **La brecha**, contra el resto de la poblacion ocupada.\n"
    "3. **Que paso al controlar** por composicion (P3). Si la brecha se desarmo, dilo.\n"
    "4. **Donde**, con el chequeo de muestra visible.\n"
    "5. **Que NO pueden afirmar con estos datos.** Minimo tres limites concretos."))

celdas.append(md(
    "> **Recomendacion del equipo N**\n"
    ">\n"
    "> *Escribe aqui.*\n"
    ">\n"
    "> **Lo que no podemos afirmar con estos datos:**\n"
    "> 1. *...*\n"
    "> 2. *...*\n"
    "> 3. *...*"))

# --------------------------------------------------------------- seccion 6 ---
celdas.append(encabezado(
    6, "De SQL a grafica",
    "Llevar el resultado de una consulta a una figura y a un archivo."))

celdas.append(md(
    "Cada consulta devuelve un `DataFrame` con `.df()`, asi que graficar es exactamente lo\n"
    "mismo que hicieron en el cuaderno 03: guardas el resultado en una variable y se lo pasas\n"
    "a matplotlib.\n"
    "\n"
    "El unico detalle propio de este proyecto es que **la consulta trae el `count(*)` y la\n"
    "grafica lo muestra**."))

celdas.append(code(
    "import matplotlib.pyplot as plt\n"
    "\n"
    "datos = con.execute(\"\"\"\n"
    "SELECT departamento,\n"
    "       count(*)                                      AS registros,\n"
    "       round(100 * sum(fex * informal) / sum(fex), 1) AS informal_pct\n"
    "FROM personas\n"
    "WHERE anio = 2025 AND ocupado = 1 AND migrante = 1\n"
    "GROUP BY 1\n"
    "HAVING count(*) >= 100\n"
    "ORDER BY 3 DESC\n"
    "LIMIT 10\n"
    "\"\"\").df()\n"
    "\n"
    "fig, ax = plt.subplots(figsize=(9, 5))\n"
    'ax.barh(datos["departamento"], datos["informal_pct"], color="#0B4F6C")\n'
    "ax.invert_yaxis()\n"
    'ax.set_xlabel("Informalidad (%)")\n'
    'ax.set_title("Informalidad de la poblacion migrante ocupada, 2025")\n'
    "ax.set_xlim(0, 118)\n"
    'for lado in ("top", "right"):\n'
    "    ax.spines[lado].set_visible(False)\n"
    '\n'
    '# El n= de cada barra es el chequeo de muestra, visible en la figura.\n'
    'for y, (v, n) in enumerate(zip(datos["informal_pct"], datos["registros"])):\n'
    '    ax.text(v + 0.8, y, f"{v} % (n={n})", va="center", fontsize=9, color="#0B4F6C")\n'
    "\n"
    "# La fuente y el filtro van al pie de la figura, no encima del titulo.\n"
    'fig.text(0.01, 0.01, "Fuente: GEIH (DANE), 2025. Cifras ponderadas con fex. '
    'Solo departamentos con 100 o mas registros.",\n'
    '         fontsize=8, color="#5A6672")\n'
    "plt.tight_layout(rect=(0, 0.04, 1, 1))\n"
    "plt.show()"))

celdas.append(bloque_claro(
    "<b>El <code>n=</code> de cada barra no es decoracion: es parte de lo que se califica.</b> "
    "Una barra de 98 % construida sobre 187 encuestados y una construida sobre 12 se ven "
    "identicas en la figura, y no dicen lo mismo. Poner el numero de registros al lado es la "
    "manera de que el comite -- y la rubrica -- vean la diferencia.<br><br>"
    "Lo mismo aplica al pie de la figura: <b>de donde salen los datos, de que ano, ponderados "
    "con que, y que se dejo por fuera</b>. Una grafica sin fuente ni filtro declarado no es "
    "honesta, aunque los numeros esten bien."))

celdas.append(md(
    "Para llevar una tabla a la presentacion o al informe, exportala. `to_csv` guarda el\n"
    "archivo en la sesion de Colab; para bajarlo al computador, panel izquierdo > icono de\n"
    "carpeta > los tres puntos del archivo > Descargar."))

celdas.append(code(
    'datos.to_csv("informalidad_migrantes_2025.csv", index=False)\n'
    'print("Guardado: informalidad_migrantes_2025.csv |", len(datos), "filas")\n'
    "datos"))

# --------------------------------------------------------------- seccion 7 ---
celdas.append(encabezado(
    7, "El plus: publicar el analisis con Quarto",
    "Opcional. Puntos extra, por fuera de los 100."))

celdas.append(md(
    "**Quarto** convierte un cuaderno en un documento publicable: una pagina web con el texto,\n"
    "el codigo y las graficas, con tabla de contenidos y aspecto de informe profesional. Es la\n"
    "diferencia entre entregar un archivo `.ipynb` y entregar **un enlace** que el comite puede\n"
    "abrir en el celular.\n"
    "\n"
    "Los comandos, corridos en la carpeta donde esta el cuaderno:\n"
    "\n"
    "```bash\n"
    "pip install jupyter\n"
    "quarto convert 07_proyecto_final_equilab.ipynb   # -> .qmd\n"
    "quarto render 07_proyecto_final_equilab.qmd --to html\n"
    "# publicar: subir el .html a GitHub y activar GitHub Pages en Settings > Pages\n"
    "```\n"
    "\n"
    "Y el bloque de *front matter* que va **al inicio del `.qmd`**, antes de cualquier otra\n"
    "cosa (los tres guiones de apertura y de cierre son obligatorios):\n"
    "\n"
    "```yaml\n"
    "---\n"
    'title: "Radar EAN de brechas laborales - Equipo N"\n'
    'author: "Nombres"\n'
    "format: html\n"
    "execute:\n"
    "  echo: true\n"
    "---\n"
    "```\n"
    "\n"
    "`execute: echo: true` deja el codigo visible en la pagina publicada, que es lo que\n"
    "queremos: la gracia del sitio es que cualquiera pueda ver de donde salio cada cifra."))

celdas.append(bloque_claro(
    "<b>Esto es un plus, no un requisito.</b> Los 100 puntos del proyecto se ganan completos con "
    "el cuaderno y la sustentacion. Quarto suma decimas adicionales por encima de esos 100, y "
    "solo si el sitio publicado funciona: un enlace roto no suma. Antes de meterse aqui, "
    "asegurense de que las seis preguntas estan respondidas."))

# ----------------------------------------------------------------- cierre ---
celdas.append(md(
    "---\n"
    "\n"
    "## Antes de entregar\n"
    "\n" +
    tabla(["Revisa", "Como se ve si esta bien"], [
        ("<code>MI_DIMENSION</code> es la de tu equipo",
         "Dice <code>mujer</code>, <code>joven</code>, <code>racializada</code>, "
         "<code>lgbtiq</code> o <code>discapacidad</code>. <b>Nunca <code>migrante</code>.</b>"),
        ("Todas las cifras estan ponderadas",
         "Cada porcentaje sale de <code>sum(fex * x) / sum(fex)</code>. No queda ningun "
         "<code>avg()</code> suelto."),
        ("Cada cifra trae sus registros",
         "Toda tabla tiene su columna <code>registros</code>, y toda barra su <code>n=</code>."),
        ("La P3 esta respondida de verdad",
         "Hay una comparacion cruda y una controlada, y una frase que dice explicitamente si "
         "la brecha sobrevivio, se encogio o desaparecio."),
        ("La P6 dice que NO se puede afirmar",
         "Minimo tres limites concretos, no una formula generica."),
        ("El cuaderno corre de arriba a abajo",
         "Entorno de ejecucion &gt; Reiniciar y ejecutar todo, sin una sola celda en rojo."),
        ("Las graficas tienen titulo, eje y fuente",
         "Se entienden solas, sin que nadie explique al lado."),
    ]) +
    "\n\n"
    "Y una ultima: **el comite tiene ocho minutos y no ha visto sus datos**. La cifra que\n"
    "elijan para abrir la sustentacion decide si los escuchan el resto del tiempo."))

nb = nbf.v4.new_notebook(cells=celdas)
nb.metadata["kernelspec"] = {"display_name": "Python 3", "name": "python3"}
nb.metadata["language_info"] = {"name": "python"}
nb.metadata["colab"] = {"name": "07_proyecto_final_equilab.ipynb",
                        "provenance": [], "toc_visible": True}
nbf.write(nb, NB)
print(f"escrito: {NB} ({len(celdas)} celdas)")
