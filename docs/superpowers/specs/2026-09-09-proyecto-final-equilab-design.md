# Proyecto final DataXperience — Radar EAN de brechas laborales

**Fecha:** 2026-09-09
**Curso:** DataXperience (IFP00553), ciclo de 9 semanas, 2026 C3
**Reemplaza:** el "dataset propio" del proyecto final (clases 22–25, corte 2, 60 %)
**Estado:** diseño aprobado, pendiente de construcción

---

## 1. Qué es y por qué

Los estudiantes cierran el ciclo analizando brechas laborales reales de la GEIH
con la base de Equilab, en equipos, con SQL sobre DuckDB. Cada equipo defiende a
una población distinta ante un comité ficticio que solo puede financiar **un**
programa de empleabilidad.

El diseño resuelve tres problemas del proyecto final tal como estaba planteado:

- **Datasets dispares.** Con "dataset propio" cada equipo llegaba con datos de
  calidad distinta y las sustentaciones no eran comparables. Aquí la pregunta
  madre es la misma para los cinco y solo cambia la población.
- **Análisis sin consecuencia.** El marco del comité obliga al "y entonces qué"
  que la rúbrica de comunicación pide y que los talleres no exigían.
- **Cierre del arco de herramientas.** El curso terminó en bases de datos
  relacionales y SQL; el proyecto final se hace en SQL, no en pandas.

**Equipos:** 5 de 4 estudiantes.

---

## 2. La base de datos

`geih_docencia.duckdb` del repo Equilab (`data/db/`), tabla `personas`:
4.772.421 filas, 2021 a 2026 (2026 con 6 meses publicados), 37 columnas, sin
códigos que decodificar, con el factor de expansión `fex` ya calculado y
banderas por dimensión de diversidad.

Se publica como **parquet ZSTD de 45,1 MB** en el repo del curso. Cabe en GitHub
(límite de 100 MB) y DuckDB lo lee por URL con `httpfs` trayéndose solo las
columnas que la consulta pide. Los estudiantes no descargan ni instalan nada más
que `duckdb` en Colab.

### Viabilidad verificada (2025, informalidad ponderada con `fex`)

| Dimensión | Ocupados en muestra | Grupo | Resto |
|---|---|---|---|
| Mujeres | 158.997 | 52,7 % | 57,1 % |
| Jóvenes | 37.115 | 62,8 % | 54,3 % |
| Racializadas | 45.535 | 72,4 % | 52,9 % |
| LGBTIQ+ | 4.499 | 37,3 % | 55,1 % |
| Migrantes | 3.611 | 87,8 % | 54,9 % |
| Discapacidad | 6.207 | 73,7 % | 55,0 % |

Las seis dimensiones aguantan el análisis a nivel nacional. **Migrantes queda
fuera del reparto obligatorio**: la variable no existe en 2021 y cae de 29.756
registros en 2022 a 8.419 en 2025, así que cualquier serie de tiempo ahí es
engañosa. Se usa como caso resuelto de la plantilla (ver §4).

---

## 3. El reto

**Situación.** Equilab financia un solo programa de empleabilidad en 2027. Cada
equipo defiende a una población con evidencia de la GEIH. La clase decide en la
sustentación (clase 25).

**Reparto:**

| Equipo | Población | Dificultad de diseño |
|---|---|---|
| 1 | Mujeres | Paradoja: informalidad menor que la de los hombres. Si no la desarman, concluyen que no hay brecha |
| 2 | Jóvenes (14–28) | Brecha limpia; la más accesible de las cinco |
| 3 | Personas racializadas | La brecha más grande, con muestra amplia |
| 4 | Personas LGBTIQ+ | Segunda paradoja **y** muestra chica: chocan de verdad con el chequeo de tamaño |
| 5 | Personas con discapacidad | Brecha grande, población poco trabajada en clase |

**Las seis preguntas obligatorias** (iguales para los cinco equipos):

1. **¿Cuántas personas son?** Magnitud expandida con `fex` y registros que la sustentan.
2. **¿Cómo les va?** Informalidad (obligatoria) + dos indicadores a elección entre
   salario por hora, contrato escrito, cotización a pensión y subempleo, siempre
   contra el resto de la población ocupada.
3. **¿La brecha es real o es composición?** Rehacer la comparación controlando por
   al menos una variable: edad, nivel educativo o zona. **Es el criterio que
   separa Destacado de Competente.**
4. **¿Cómo cambió entre 2021 y 2025?**
5. **¿Dónde es peor?** Corte territorial con el chequeo de muestra activo.
6. **La recomendación:** por qué su población, y qué **no** pueden afirmar con estos datos.

### Reglas de rigor

- **`fex` siempre.** Toda cifra ponderada: `sum(fex * x) / sum(fex)`. Sin
  ponderar, la cifra está mal. Innegociable.
- **Chequeo de muestra simplificado.** Reportar `count(*)` junto a cada cifra y
  advertir cuando haya menos de 100 registros detrás.
- **Sin gate de CV con linealización de Taylor.** Es estadística de muestreo
  complejo que no está en el syllabus del ciclo. El chequeo de muestra enseña el
  mismo reflejo profesional sin pedir matemática que no vieron.

---

## 4. Artefactos a construir

### 4.1 `notebooks/data/geih_equilab_2021_2026.parquet`

Export de la tabla `personas` completa, ZSTD, 45,1 MB, más un README con el
diccionario de las 37 variables en el formato del README que ya existe para la
GEIH de junio.

**Resuelto:** los archivos de `notebooks/` los versiona el repo raíz
(`YourFavouriteDataSuperstar/Data-Xperience`), que es el que sirve la URL cruda de los
cuadernos 05 y 06. El `.git` que hay dentro de `notebooks/` apunta al mismo remoto pero
no tiene ningún commit: es un residuo inerte. **Todo `git add` se hace desde la raíz del
repo**; ejecutado dentro de `notebooks/` escribiría en el repo vacío y el archivo nunca
llegaría a GitHub.

### 4.2 `notebooks/07_proyecto_final_equilab.ipynb`

Plantilla en el estilo de los seis anteriores: badge de Colab, bloques HTML con
la paleta azul (`#0B4F6C` / `#D6EEF6` / `#8FD3E8`), español sin tildes, secciones
numeradas, regla "lee, ejecuta, cambia un valor".

| Sección | Contenido |
|---|---|
| 0 | El reto, la población del equipo, las seis preguntas, cómo se evalúa |
| 1 | Conexión resuelta: `pip install duckdb`, cargar el parquet por URL, primer vistazo |
| 2 | La regla de oro: la misma cifra sin ponderar y ponderada, lado a lado · el chequeo de muestra |
| 3 | Un caso resuelto de punta a punta: las seis preguntas respondidas |
| 4 | La trampa de composición demostrada: cifra cruda vs. controlada por zona y educación |
| 5 | Esqueleto vacío de las seis preguntas, con celdas marcadas |
| 6 | Exportar resultados y graficar lo que salió de SQL |
| 7 | El plus: pasar el cuaderno a `.qmd` y publicarlo como sitio |

**Decisión de diseño clave:** el caso resuelto de las secciones 3 y 4 usa a la
**población migrante** — la que quedó fuera del reparto. Los equipos ven el flujo
completo, con la trampa de composición incluida, sin que ninguno reciba servida
su propia respuesta. Y les queda demostrado con datos que la cifra cruda puede
mentir, antes de que les pase a ellos.

El cuaderno se guarda **ejecutado**, con outputs, y las cifras del texto se
verifican contra las salidas reales.

### 4.3 Guía del plus de Quarto

`quarto convert` del `.ipynb` a `.qmd`, render a HTML y publicación en GitHub
Pages. Puntos extra opcionales, por fuera de los 100.

---

## 5. Evaluación

Cuatro criterios sobre 100 puntos, con los cuatro niveles del syllabus
(Destacado / Competente / Básico / No competente):

| Criterio | Peso | Qué evalúa |
|---|---|---|
| Rigor con datos de encuesta y SQL | 30 | Ponderación con `fex` · registros reportados · advertencia de muestra chica · consultas que responden lo que dicen responder |
| Análisis y hallazgos | 25 | Las seis preguntas con evidencia. **Un equipo que reporte la cifra cruda como si fuera la brecha no llega a Destacado** |
| Visualización | 20 | Gráficos correctos, etiquetados y honestos (clase 19) |
| Comunicación y sustentación | 25 | Narrativa (clase 15), recomendación al comité, límites de lo afirmable |

Entregables por equipo: **cuaderno + sustentación de 8–10 min**. Sin dashboard.
Décimos adicionales por el sitio en Quarto.

---

## 6. Montaje en Canvas

Con el agente **`activity_creator` de Aula Studio** (no el plugin canvas-mcp).
Una sola corrida con `tema_por_grupo=True`: forma los cinco equipos, genera los
cinco casos y crea **cinco tareas, una por equipo**, cada una visible solo para
su grupo mediante override, todas con la misma rúbrica.

Parámetros de la corrida:

| Campo | Valor |
|---|---|
| `materia` | DataXperience |
| `tema_por_grupo` | `True` |
| `n_equipos` / `tamano_grupo` | 5 / 4 |
| `con_rubrica` | `True` |
| `puntos` | 100 |
| `notas` | Los cinco casos dictados literalmente + las reglas de rigor + entregables + el plus |
| `publicar_en_canvas` | `True` (crea en borrador; el clic de publicar es manual) |
| `course_id`, `modo_grupos`, fechas, `modulo` | **pendientes** (ver §7) |

Los cinco casos van dictados en `notas`, que el nodo `planear` inyecta al prompt
como "Indicaciones de la docente (respétalas)". El modelo no inventa el reparto.

**Compuertas.** El agente se detiene y muestra los cinco casos y la rúbrica antes
de escribir en Canvas, y las tareas nacen sin publicar. El OK de esa compuerta y
la publicación los da la docente, no el asistente.

---

## 7. Decisiones pendientes

1. **Curso de Canvas**: nombre o id de DataXperience.
2. **Formación de equipos**: ¿lista ya armada (modo manual) o los arma el agente?
   Si los arma, se recomienda modo mezclado por desempeño, para que ningún equipo
   quede con los cuatro más flojos en un trabajo que pesa el 60 % del corte.
3. **Fechas**: apertura y cierre. Por el plan clase a clase, abrir en la clase 22
   (semana 8) y cerrar antes de la 25 (semana 9).
(El remoto del parquet ya quedó resuelto: ver §4.1.)

---

## 8. Criterios de éxito

- Todas las consultas de la plantilla corren contra el parquet publicado y las
  cifras del texto coinciden con las salidas ejecutadas.
- Un estudiante abre el cuaderno en Colab y llega a su primera cifra ponderada
  sin ayuda del docente.
- Cada uno de los cinco equipos tiene datos suficientes para responder las seis
  preguntas a nivel nacional.
- Las cinco tareas quedan en Canvas en borrador, cada una visible solo para su
  equipo, con la rúbrica asociada.
