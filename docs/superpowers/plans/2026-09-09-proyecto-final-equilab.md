# Radar EAN de brechas laborales — Plan de implementacion

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dejar listo el proyecto final de DataXperience: la base de Equilab publicada, el cuaderno 07 plantilla ejecutado y verificado, y cinco tareas creadas en Canvas en borrador, una por equipo.

**Architecture:** La tabla `personas` de `geih_docencia.duckdb` (repo Equilab) se exporta a parquet y se publica en el repo del curso, donde DuckDB la lee por URL cruda desde Colab. El cuaderno 07 se genera con `nbformat` desde un script reproducible, se ejecuta con `nbconvert` y sus cifras se verifican contra las salidas reales. El montaje en Canvas lo hace el agente `activity_creator` de Aula Studio con los cinco casos dictados en `--notas`.

**Tech Stack:** DuckDB 1.x · Python 3.12 · nbformat + nbconvert · pandas · matplotlib · LangGraph (Aula Studio) · Canvas LMS

**Spec:** `docs/superpowers/specs/2026-09-09-proyecto-final-equilab-design.md`

## Global Constraints

- **Texto del cuaderno en espanol SIN tildes.** Es la convencion de los cuadernos 01–06.
- **Paleta obligatoria:** `#0B4F6C` (fondo oscuro), `#D6EEF6` (fondo claro), `#8FD3E8` (acento), `#C9E7F2` (texto sobre oscuro), `#FFFFFF`.
- **Badge de Colab** como primera celda, apuntando a `https://colab.research.google.com/github/YourFavouriteDataSuperstar/Data-Xperience/blob/main/notebooks/07_proyecto_final_equilab.ipynb`.
- **Kernelspec:** `{"display_name": "Python 3", "name": "python3"}`.
- **El cuaderno se guarda EJECUTADO**, con outputs.
- **Toda cifra ponderada con `fex`:** `sum(fex * x) / sum(fex)`. Nunca un promedio crudo.
- **Chequeo de muestra:** todo agregado lleva `count(*)` al lado; se advierte por debajo de 100 registros.
- **URL cruda de datos:** `https://raw.githubusercontent.com/YourFavouriteDataSuperstar/Data-Xperience/main/notebooks/data/<archivo>` (misma convencion de los cuadernos 05 y 06).
- **Git SIEMPRE desde la raiz del repo del curso.** `notebooks/` contiene un `.git` huerfano sin commits que apunta al mismo remoto; un `git add` ejecutado dentro de `notebooks/` escribe en ese repo vacio y el archivo nunca llega a GitHub.
- **Commits acotados:** usar siempre `git commit -- <ruta>`. El repo tiene cambios ajenos en staging que NO deben entrar en estos commits.
- **Nada se publica en Canvas.** El agente crea borradores y se detiene en su compuerta; el OK y la publicacion los da la docente.

---

### Task 1: Publicar la base de Equilab en el repo del curso

**Files:**
- Create: `scripts/exportar_base_equilab.py`
- Create: `notebooks/data/geih_equilab_2021_2026.parquet` (45 MB, generado)
- Modify: `notebooks/data/README.md` (agregar seccion de la base nueva)

**Interfaces:**
- Produces: el archivo parquet servido en
  `https://raw.githubusercontent.com/YourFavouriteDataSuperstar/Data-Xperience/main/notebooks/data/geih_equilab_2021_2026.parquet`
  con la tabla `personas`: 4.772.421 filas, 37 columnas, anios 2021–2026.
  Las tareas 2 y 3 leen ese URL.

- [ ] **Step 1: Escribir el script de exportacion**

```python
# scripts/exportar_base_equilab.py
"""Exporta la tabla personas de Equilab a parquet para el repo del curso."""
from pathlib import Path
import duckdb

ORIGEN = Path("/Users/aor/Documents/GitHub/Equilab---Radar/data/db/geih_docencia.duckdb")
DESTINO = Path(__file__).resolve().parents[1] / "notebooks/data/geih_equilab_2021_2026.parquet"

con = duckdb.connect(str(ORIGEN), read_only=True)
con.execute(
    f"COPY (SELECT * FROM personas) TO '{DESTINO}' (FORMAT PARQUET, COMPRESSION ZSTD)"
)
filas = con.execute("SELECT count(*) FROM personas").fetchone()[0]
print(f"{filas:,} filas -> {DESTINO} ({DESTINO.stat().st_size/1e6:.1f} MB)")
```

- [ ] **Step 2: Correr la exportacion**

Run: `python3 scripts/exportar_base_equilab.py`
Expected: `4,772,421 filas -> .../geih_equilab_2021_2026.parquet (45.1 MB)`

Si el tamano supera 95 MB, parar: GitHub rechaza a los 100 MB. En ese caso
reexportar solo `WHERE en_edad_de_trabajar = 1` (25,5 MB medidos) y ajustar el
README y el cuaderno para decir que la base trae solo poblacion en edad de trabajar.

- [ ] **Step 3: Verificar que el parquet se lee y las cifras cuadran**

Run:
```bash
python3 -c "
import duckdb
d='notebooks/data/geih_equilab_2021_2026.parquet'
c=duckdb.connect()
print(c.execute(f\"SELECT count(*) FROM '{d}'\").fetchone())
print(c.execute(f\"SELECT round(100*sum(fex*informal)/sum(fex),1) FROM '{d}' WHERE anio=2025 AND ocupado=1 AND migrante=1\").fetchone())
"
```
Expected: `(4772421,)` y `(87.8,)`. Si la segunda cifra no es 87.8, la exportacion perdio filas o columnas: parar y revisar.

- [ ] **Step 4: Documentar las variables en el README**

Agregar a `notebooks/data/README.md` una seccion `## geih_equilab_2021_2026.parquet`
con: origen (repo Equilab, tabla `personas` de `geih_docencia.duckdb`), cobertura
(2021–2026, 2026 con 6 meses publicados), numero de filas, y la tabla de las 37
variables agrupadas en cinco bloques — identificacion (`anio`, `mes`,
`departamento`, `zona`), persona (`edad`, `sexo`, `nivel_educativo`,
`educacion_superior`), dimensiones de diversidad (`mujer`, `joven`,
`racializada`, `lgbtiq`, `migrante`, `discapacidad`), situacion laboral
(`ocupado`, `desocupado`, `inactivo`, `posicion`, `asalariado`, `independiente`,
`rama`, `informal`, `tiene_contrato`, `contrato_escrito`, `cotiza_pension`,
`afiliado_salud`, `subempleo_horas`, `horas_semana`, `ingreso_laboral`,
`salario_hora`) y ponderacion (`fex`, `fex_mes`).

Incluir la advertencia sobre `migrante`: la variable no existe en 2021 y cae de
29.756 registros en 2022 a 8.419 en 2025; no usarla para series de tiempo.

- [ ] **Step 5: Commit y push**

```bash
git add notebooks/data/geih_equilab_2021_2026.parquet notebooks/data/README.md scripts/exportar_base_equilab.py
git commit -m "Publica la base de Equilab (GEIH 2021-2026) para el proyecto final" -- notebooks/data/geih_equilab_2021_2026.parquet notebooks/data/README.md scripts/exportar_base_equilab.py
git push origin main
```

- [ ] **Step 6: Verificar el URL crudo ya publicado**

Run:
```bash
python3 -c "
import duckdb
c=duckdb.connect(); c.execute('INSTALL httpfs; LOAD httpfs;')
u='https://raw.githubusercontent.com/YourFavouriteDataSuperstar/Data-Xperience/main/notebooks/data/geih_equilab_2021_2026.parquet'
print(c.execute(f\"SELECT count(*) FROM '{u}'\").fetchone())
"
```
Expected: `(4772421,)`.

Si falla, el cuaderno usa el plan B: `!wget -q <url> -O geih.parquet` y luego se
consulta el archivo local. Anotarlo y seguir — no bloquea las tareas siguientes.

---

### Task 2: Cuaderno 07 — secciones 0 a 4 (conexion, regla de oro, caso resuelto)

**Files:**
- Create: `scripts/construir_cuaderno_07.py`
- Create: `notebooks/07_proyecto_final_equilab.ipynb` (generado y ejecutado)

**Interfaces:**
- Consumes: el URL del parquet de la Task 1.
- Produces: `construir_cuaderno_07.py` con `bloque_oscuro(titulo, bajada)`,
  `bloque_claro(html)` y `md(texto)` / `code(fuente)`, que la Task 3 reutiliza
  para agregar las secciones 5 a 7.

- [ ] **Step 1: Escribir el generador con los helpers de estilo**

```python
# scripts/construir_cuaderno_07.py
"""Genera notebooks/07_proyecto_final_equilab.ipynb con nbformat."""
from pathlib import Path
import nbformat as nbf

NB = Path(__file__).resolve().parents[1] / "notebooks/07_proyecto_final_equilab.ipynb"
URL = ("https://raw.githubusercontent.com/YourFavouriteDataSuperstar/"
       "Data-Xperience/main/notebooks/data/geih_equilab_2021_2026.parquet")

def md(texto): return nbf.v4.new_markdown_cell(texto)
def code(fuente): return nbf.v4.new_code_cell(fuente)

def bloque_oscuro(titulo, bajada):
    return md(
        '<div style="background:#0B4F6C;border-radius:12px;padding:32px 28px;margin:14px 0;">\n'
        '  <div style="color:#8FD3E8;font-size:13px;letter-spacing:5px;font-weight:700;">DATAXPERIENCE</div>\n'
        f'  <div style="color:#FFFFFF;font-size:38px;font-weight:800;line-height:1.15;margin-top:8px;">{titulo}</div>\n'
        f'  <div style="color:#C9E7F2;font-size:16px;margin-top:12px;">{bajada}</div>\n'
        '</div>')

def bloque_claro(html):
    return md(f'<div style="background:#D6EEF6;border-left:6px solid #0B4F6C;'
              f'border-radius:8px;padding:18px 20px;margin:14px 0;font-size:15px;">{html}</div>')

celdas = []
# ... (secciones, ver pasos siguientes)

nb = nbf.v4.new_notebook(cells=celdas)
nb.metadata["kernelspec"] = {"display_name": "Python 3", "name": "python3"}
nbf.write(nb, NB)
print(f"escrito: {NB} ({len(celdas)} celdas)")
```

- [ ] **Step 2: Agregar la seccion 0 (badge + portada + el reto)**

Primera celda: el badge de Colab apuntando al 07 (ver Global Constraints).
Luego `bloque_oscuro("Proyecto final: Radar EAN de brechas laborales", "...")`,
y markdown con: la situacion del comite, la poblacion de cada equipo, las seis
preguntas obligatorias y la rubrica resumida — todo copiado del spec §3 y §5,
sin tildes.

- [ ] **Step 3: Agregar la seccion 1 (conexion) y correrla suelta antes de meterla**

```python
code("""!pip install -q duckdb""")
code(f"""import duckdb

BASE = "{URL}"
con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs;")

con.execute(f"SELECT * FROM '{{BASE}}' LIMIT 5").df()""")
```

Antes de seguir, correr esas dos celdas a mano en una sesion de Python para
confirmar que el URL responde. Si no responde, cambiar a la variante `wget`
que quedo anotada en la Task 1 Step 6.

- [ ] **Step 4: Agregar la seccion 2 (la regla de oro) con la comparacion sin ponderar vs ponderada**

```python
code(f"""con.execute(f\"\"\"
SELECT round(100 * avg(informal), 1)                  AS sin_ponderar,
       round(100 * sum(fex * informal) / sum(fex), 1) AS ponderado,
       count(*)                                       AS registros
FROM '{{BASE}}'
WHERE anio = 2025 AND ocupado = 1
\"\"\").df()""")
```

El markdown que la acompana explica que la diferencia entre las dos columnas es
la razon por la que el factor de expansion no es opcional, y que `registros` es
el chequeo de muestra: por debajo de 100, la cifra no se reporta sin advertencia.

- [ ] **Step 5: Agregar la seccion 3 (caso resuelto: migrantes) con las seis preguntas**

Las consultas ya estan verificadas contra la base. Van una por celda, cada una
precedida de un markdown que dice que pregunta responde:

```sql
-- P1 cuantas personas son
SELECT round(sum(fex)) AS personas, count(*) AS registros,
       round(sum(CASE WHEN ocupado=1 THEN fex END)) AS ocupados
FROM '{BASE}' WHERE anio = 2025 AND migrante = 1;
-- esperado: 633.137 personas | 8.419 registros | 291.818 ocupados

-- P2 como les va
SELECT CASE WHEN migrante=1 THEN 'Migrante' ELSE 'Resto' END AS grupo, count(*) AS registros,
       round(100*sum(fex*informal)/sum(fex),1)         AS informal_pct,
       round(100*sum(fex*cotiza_pension)/sum(fex),1)   AS pension_pct,
       round(100*sum(fex*contrato_escrito)/sum(fex),1) AS contrato_pct
FROM '{BASE}' WHERE anio = 2025 AND ocupado = 1 GROUP BY 1;
-- esperado: Migrante 87,8 / 12,2 / 14,5 (n=3.611) — Resto 54,9 / 43,6 / 40,2 (n=354.418)

-- P4 como cambio
SELECT anio, count(*) AS registros, round(100*sum(fex*informal)/sum(fex),1) AS informal_pct
FROM '{BASE}' WHERE ocupado = 1 AND migrante = 1 GROUP BY 1 ORDER BY 1;
-- esperado: 2022 88,8 | 2023 85,0 | 2024 85,8 | 2025 87,8 | 2026 88,4 (2021 no existe)

-- P5 donde es peor
SELECT departamento, count(*) AS registros, round(100*sum(fex*informal)/sum(fex),1) AS informal_pct
FROM '{BASE}' WHERE anio = 2025 AND ocupado = 1 AND migrante = 1
GROUP BY 1 HAVING count(*) >= 100 ORDER BY 3 DESC LIMIT 6;
-- esperado: La Guajira 98,4 (n=187) | Vichada 98,2 (n=115) | Magdalena 97,0 (n=100)
--           Boyaca 94,1 (n=133) | Meta 93,1 (n=200) | Norte de Santander 91,9 (n=370)
```

El markdown de P4 senala que la serie arranca en 2022 y que los registros caen
de 13.241 a 3.611: por eso migrantes no esta en el reparto, y por eso una serie
de tiempo se lee con cuidado. El de P5 senala el `HAVING count(*) >= 100`: es el
chequeo de muestra escrito en SQL.

- [ ] **Step 6: Agregar la seccion 4 (la trampa de composicion)**

```sql
-- donde vive y que estudio cada grupo
SELECT CASE WHEN migrante=1 THEN 'Migrante' ELSE 'Resto' END AS grupo,
       round(100*sum(CASE WHEN zona='Urbano' THEN fex END)/sum(fex),1) AS pct_urbano,
       round(100*sum(CASE WHEN educacion_superior=1 THEN fex END)/sum(fex),1) AS pct_superior,
       round(sum(fex*edad)/sum(fex),1) AS edad_promedio
FROM '{BASE}' WHERE anio = 2025 AND ocupado = 1 GROUP BY 1;
-- esperado: Migrante 90,2 / 19,3 / 31,8 — Resto 79,5 / 33,6 / 41,1

-- la misma comparacion, ahora dentro de cada zona
SELECT zona, CASE WHEN migrante=1 THEN 'Migrante' ELSE 'Resto' END AS grupo,
       count(*) AS registros, round(100*sum(fex*informal)/sum(fex),1) AS informal_pct
FROM '{BASE}' WHERE anio = 2025 AND ocupado = 1 GROUP BY 1,2 ORDER BY 1,2;
-- esperado: Rural Migrante 94,5 (n=261) / Resto 83,4 — Urbano Migrante 87,1 (n=3.350) / Resto 47,5
```

El markdown cierra con la leccion, que es la que sostiene el criterio de
Destacado: los dos grupos no son comparables de entrada (los migrantes son mas
urbanos, mas jovenes y con menos educacion superior), asi que hay que comparar
dentro de grupos parecidos. **En este caso la brecha sobrevive el control y hasta
crece en lo urbano (87,1 vs 47,5): la brecha es real.** Y la advertencia: no
siempre pasa esto — hay poblaciones donde la brecha cruda se desarma al
controlar, y detectarlo es parte del trabajo de cada equipo.

- [ ] **Step 7: Generar y ejecutar el cuaderno**

```bash
python3 scripts/construir_cuaderno_07.py
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 notebooks/07_proyecto_final_equilab.ipynb
```
Expected: termina sin error y el `.ipynb` queda con outputs.

- [ ] **Step 8: Verificar que ninguna celda fallo y que las cifras del texto cuadran**

Run:
```bash
python3 -c "
import json
nb=json.load(open('notebooks/07_proyecto_final_equilab.ipynb'))
errores=[c for c in nb['cells'] if any(o.get('output_type')=='error' for o in c.get('outputs',[]))]
vacias=[c for c in nb['cells'] if c['cell_type']=='code' and c['source'] and not c.get('outputs')]
print('celdas con error:',len(errores),'| celdas de codigo sin salida:',len(vacias))
texto=json.dumps(nb)
for cifra in ['87,8','633.137','98,4','47,5','90,2']:
    print(cifra, 'OK' if cifra in texto else 'FALTA')
"
```
Expected: `celdas con error: 0`, y las cinco cifras en OK. Cualquier `FALTA`
significa que el texto y las salidas se separaron: corregir el texto, no la salida.

- [ ] **Step 9: Commit**

```bash
git add scripts/construir_cuaderno_07.py notebooks/07_proyecto_final_equilab.ipynb
git commit -m "Cuaderno 07: conexion, regla de oro y caso resuelto de migrantes" -- scripts/construir_cuaderno_07.py notebooks/07_proyecto_final_equilab.ipynb
```

---

### Task 3: Cuaderno 07 — secciones 5 a 7 (esqueleto, graficas, plus Quarto)

**Files:**
- Modify: `scripts/construir_cuaderno_07.py`
- Modify: `notebooks/07_proyecto_final_equilab.ipynb` (regenerado y reejecutado)

**Interfaces:**
- Consumes: `bloque_oscuro`, `bloque_claro`, `md`, `code` y `URL` de la Task 2.

- [ ] **Step 1: Agregar la seccion 5 — el esqueleto de las seis preguntas**

Una celda de markdown por pregunta (el enunciado tal como esta en el spec §3) y
debajo una celda de codigo con la consulta a medio armar y el hueco marcado:

```python
code("""# P1. Cuantas personas son
# Cambia MI_DIMENSION por la columna de tu equipo:
# mujer | joven | racializada | lgbtiq | discapacidad
MI_DIMENSION = "___"

con.execute(f\"\"\"
SELECT round(sum(fex)) AS personas, count(*) AS registros
FROM '{BASE}'
WHERE anio = 2025 AND {MI_DIMENSION} = 1
\"\"\").df()""")
```

Las seis celdas usan la misma variable `MI_DIMENSION`, declarada una sola vez al
inicio de la seccion: cambiando un valor, el equipo corre su analisis completo.
La P3 (composicion) lleva el recordatorio de que la respuesta correcta puede ser
"la brecha se desarma", y que eso tambien es un hallazgo.

- [ ] **Step 2: Agregar la seccion 6 — de SQL a grafica**

```python
code("""import matplotlib.pyplot as plt

datos = con.execute(f\"\"\"
SELECT departamento, count(*) AS registros,
       round(100*sum(fex*informal)/sum(fex),1) AS informal_pct
FROM '{BASE}'
WHERE anio = 2025 AND ocupado = 1 AND migrante = 1
GROUP BY 1 HAVING count(*) >= 100
ORDER BY 3 DESC LIMIT 10
\"\"\").df()

fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(datos["departamento"], datos["informal_pct"], color="#0B4F6C")
ax.invert_yaxis()
ax.set_xlabel("Informalidad (%)")
ax.set_title("Informalidad de la poblacion migrante ocupada, 2025")
for y, (v, n) in enumerate(zip(datos["informal_pct"], datos["registros"])):
    ax.text(v + 0.5, y, f"{v} % (n={n})", va="center", fontsize=9)
plt.tight_layout()
plt.show()""")
```

El markdown senala que el `n=` en cada barra no es decoracion: es el chequeo de
muestra visible en la grafica, y es parte de lo que se califica.

- [ ] **Step 3: Agregar la seccion 7 — el plus de Quarto**

Markdown con los cuatro comandos y la advertencia de que son puntos extra:

```bash
pip install jupyter
quarto convert 07_proyecto_final_equilab.ipynb   # -> .qmd
quarto render 07_proyecto_final_equilab.qmd --to html
# publicar: subir el .html a GitHub y activar GitHub Pages en Settings > Pages
```

Mas el bloque de front matter que deben poner al inicio del `.qmd`:

```yaml
---
title: "Radar EAN de brechas laborales — Equipo N"
author: "Nombres"
format: html
execute:
  echo: true
---
```

- [ ] **Step 4: Regenerar, reejecutar y verificar**

```bash
python3 scripts/construir_cuaderno_07.py
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 notebooks/07_proyecto_final_equilab.ipynb
```

Y volver a correr el verificador del Step 8 de la Task 2.
Expected: `celdas con error: 0`.

Ojo: las celdas del esqueleto (seccion 5) tienen `MI_DIMENSION = "___"` y **van a
fallar al ejecutarse**. Antes de ejecutar el cuaderno, cambiar esa linea a
`MI_DIMENSION = "migrante"` para que corran, y dejarla asi en el entregado: el
equipo la cambia por la suya. Si se prefiere dejarlas sin ejecutar, marcarlas con
`"tags": ["raises-exception"]` en los metadatos de la celda para que nbconvert no
aborte.

- [ ] **Step 5: Commit**

```bash
git add scripts/construir_cuaderno_07.py notebooks/07_proyecto_final_equilab.ipynb
git commit -m "Cuaderno 07: esqueleto de las seis preguntas, graficas y plus de Quarto" -- scripts/construir_cuaderno_07.py notebooks/07_proyecto_final_equilab.ipynb
git push origin main
```

---

### Task 4: Las notas dictadas para el agente

**Files:**
- Create: `docs/reto_final_equilab_notas.md`

**Interfaces:**
- Produces: el texto que la Task 5 pasa como `--notas`. El nodo `planear` lo
  inyecta al prompt bajo "Indicaciones de la docente (respetalas)", asi que lo
  que quede aqui es lo que el modelo obedece.

- [ ] **Step 1: Escribir el documento**

Contenido, en este orden:

1. **Los cinco casos, uno por equipo, literales** — Equipo 1 mujeres, 2 jovenes,
   3 personas racializadas, 4 personas LGBTIQ+, 5 personas con discapacidad.
   Advertir explicitamente: "No cambies el reparto ni agregues poblaciones. La
   poblacion migrante NO se asigna a ningun equipo: es el ejemplo resuelto."
2. **La situacion** (el comite que financia un solo programa, spec §3).
3. **Las seis preguntas obligatorias**, literales del spec §3.
4. **Las reglas de rigor**: `fex` siempre, `count(*)` al lado de cada cifra,
   advertencia por debajo de 100 registros.
5. **Los entregables**: cuaderno + sustentacion de 8–10 minutos. Sin dashboard.
   Puntos extra por el sitio en Quarto.
6. **La rubrica pedida**: cuatro criterios con estos pesos exactos — Rigor con
   datos de encuesta y SQL 30, Analisis y hallazgos 25, Visualizacion 20,
   Comunicacion y sustentacion 25. Cuatro niveles: Destacado, Competente, Basico,
   No competente. Y la regla dura: "en Analisis y hallazgos, un equipo que
   reporte la cifra cruda sin controlar por composicion no puede llegar a Destacado".
7. **El enlace al cuaderno** en Colab y al parquet.

- [ ] **Step 2: Revisar que no contradiga al spec**

Leer `docs/superpowers/specs/2026-09-09-proyecto-final-equilab-design.md` §3 y §5
al lado del documento nuevo. Pesos, criterios, entregables y reparto tienen que
coincidir exactamente. Cualquier diferencia se corrige aqui, no en el spec.

- [ ] **Step 3: Commit**

```bash
git add docs/reto_final_equilab_notas.md
git commit -m "Notas dictadas del reto final para el agente activity_creator" -- docs/reto_final_equilab_notas.md
```

---

### Task 5: Crear las cinco tareas en Canvas (borrador)

**Files:**
- Ninguno en el repo. La salida vive en Canvas.

**Interfaces:**
- Consumes: `docs/reto_final_equilab_notas.md` de la Task 4.

- [ ] **Step 1: Pedirle a la docente los tres datos que faltan**

No arrancar sin ellos:

1. **`--curso`**: el `course_id` de DataXperience en Canvas.
2. **`--modo`**: `manual` con `--composicion "id,id,id,id;..."` si ya tiene los
   equipos armados, o `mezclado` para que el agente los arme heterogeneos por
   desempeno.
3. **`--fecha-entrega`** y **`--disponible-desde`** en ISO8601 con zona
   (`2026-XX-XXTHH:MM:00-05:00`). Referencia del plan clase a clase: abrir en la
   clase 22 (semana 8), cerrar antes de la 25 (semana 9).

- [ ] **Step 2: Confirmar que la ranura de Canvas responde**

Run (desde `/Users/aor/aula_studio`):
```bash
uv run python scripts/verificar_cursos.py
```
Expected: lista los cursos visibles con el token del `.env`. Si el curso de
DataXperience no aparece, parar: el token no alcanza y hay que conectarlo antes.

- [ ] **Step 3: Correr el agente hasta la compuerta**

```bash
cd /Users/aor/aula_studio
uv run python scripts/probar_actividad.py \
  --curso <COURSE_ID> \
  --materia "DataXperience" \
  --objetivo "Analizar con SQL sobre la GEIH la brecha laboral de una poblacion y defender ante un comite por que financiar su programa de empleabilidad" \
  --notas "$(cat '/Users/aor/Library/CloudStorage/OneDrive-Personal/Documentos/EAN/2026 C3/Data experience/docs/reto_final_equilab_notas.md')" \
  --tema-por-grupo --n-equipos 5 --tamano 4 \
  --modo <MODO> \
  --puntos 100 \
  --grupo-tareas "Proyecto final" \
  --fecha-entrega <ISO8601> --disponible-desde <ISO8601>
```

**NO pasar `--auto`.** El script se detiene en la compuerta e imprime los cinco
casos, la rubrica y los equipos.

- [ ] **Step 4: Revisar el plan en la compuerta antes de responder nada**

Verificar contra el spec, en la salida impresa:
- Cinco casos, y que sean mujeres / jovenes / racializadas / LGBTIQ+ / discapacidad.
  Si aparece migrantes o el modelo invento otra poblacion, responder con ajustes
  en vez de `ok` y decirle que respete el reparto de las notas.
- Rubrica de cuatro criterios con pesos 30 / 25 / 20 / 25 y cuatro niveles.
- Cinco equipos de cuatro integrantes.

- [ ] **Step 5: Entregarle la compuerta a la docente**

Mostrarle la salida y dejar que sea ella quien escriba `ok`, `ajustes` o
`cancelar`. **El asistente no aprueba esta compuerta.** Al aprobar, el agente
crea las cinco tareas en Canvas **en borrador**, cada una con override para su
equipo.

- [ ] **Step 6: Verificar el resultado en Canvas**

De la salida del script: cinco lineas `Tarea (borrador): <url> [<equipo>: <caso>]`,
el `group_category_id` y la rubrica con su id. Abrir una de las cinco y confirmar
que las instrucciones se ven bien (si el sanitizador de Canvas rompio el HTML, el
agente ya cae solo al iframe; revisar los avisos de la corrida).

**La publicacion de las tareas la hace la docente desde Canvas.** El plan termina
con las cinco en borrador.

---

## Verificacion final

- [ ] El parquet responde por URL cruda y devuelve 4.772.421 filas.
- [ ] El cuaderno 07 abre en Colab desde el badge y llega a su primera cifra ponderada sin intervencion.
- [ ] Ninguna celda del cuaderno tiene salida de error.
- [ ] Las cifras del texto coinciden con las salidas ejecutadas.
- [ ] Las cinco tareas estan en Canvas, en borrador, cada una visible solo para su equipo, con la rubrica asociada.
