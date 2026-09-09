# Datos del curso

## `geih_2025_06_personas.csv`

Microdato de la **Gran Encuesta Integrada de Hogares (GEIH) – junio de 2025**, publicado por el DANE
(catalogo [DANE-DIMPE-GEIH-2025](https://microdatos.dane.gov.co/index.php/catalog/853)).

- Contiene el modulo **"Caracteristicas generales, seguridad social en salud y educacion" (Personas)** completo
  (67.856 personas, 19 variables seleccionadas) mas 6 variables del modulo **Ocupados**
  (`INGLABO`, `P6800`, `P6430`, `P6426`, `RAMA2D_R4`, `P6920`) unidas por `DIRECTORIO`, `SECUENCIA_P`, `ORDEN`.
- Los datos **no fueron modificados**: solo se seleccionaron columnas, se unieron los dos modulos y se convirtio
  el archivo de `latin-1` con separador `;` a UTF-8 con separador `,`. El factor de expansion `FEX_C18` se redondeo a 4 decimales.
- Los codigos de cada variable estan documentados en el notebook `05_limpieza_de_datos_geih.ipynb` (Seccion 1)
  y en los diccionarios oficiales del catalogo del DANE.
- Uso academico. Los microdatos de la GEIH son de acceso publico bajo los terminos de uso del DANE.

Usado por los notebooks **05** (tutorial) y **06** (taller).

## `geih_equilab_2021_2026.parquet`

Extracto de la tabla `personas` de la base de docencia del proyecto **Equilab**
(`geih_docencia.duckdb`, repo [Equilab---Radar](https://github.com/YourFavouriteDataSuperstar/Equilab---Radar)),
construida a partir de la GEIH del DANE.

- Cobertura: **2021-2026**, con **2026 con solo 6 meses publicados** (enero-junio).
- **4.772.421 filas, 37 columnas**. Exportado sin filtrar con `COPY (SELECT * FROM personas) TO ... (FORMAT PARQUET, COMPRESSION ZSTD)`
  (ver `scripts/exportar_base_equilab.py`). Peso en disco: 45,1 MB.
- Las 37 variables, agrupadas en cinco bloques tematicos (mas cinco columnas
  identificadoras/administrativas de la tabla origen que no encajan en ningun
  bloque tematico: `departamento_cod`, `en_edad_de_trabajar`, `directorio`,
  `secuencia`, `orden`):

| Bloque | Variables |
|---|---|
| Identificacion | `anio`, `mes`, `departamento`, `zona` |
| Persona | `edad`, `sexo`, `nivel_educativo`, `educacion_superior` |
| Dimensiones de diversidad | `mujer`, `joven`, `racializada`, `lgbtiq`, `migrante`, `discapacidad` |
| Situacion laboral | `ocupado`, `desocupado`, `inactivo`, `posicion`, `asalariado`, `independiente`, `rama`, `informal`, `tiene_contrato`, `contrato_escrito`, `cotiza_pension`, `afiliado_salud`, `subempleo_horas`, `horas_semana`, `ingreso_laboral`, `salario_hora` |
| Ponderacion | `fex`, `fex_mes` |

**Advertencia sobre `migrante`:** la variable no existe en 2021 (0 registros)
y cae de 29.756 registros en 2022 a 8.419 en 2025 (verificado sobre este
parquet). No usarla para series de tiempo: la caida refleja un cambio en la
cobertura de la pregunta en la encuesta, no una tendencia real.

Servido por URL cruda en:
`https://raw.githubusercontent.com/YourFavouriteDataSuperstar/Data-Xperience/main/notebooks/data/geih_equilab_2021_2026.parquet`

Usado por el proyecto final del curso (analisis de brechas laborales con SQL
sobre DuckDB desde Google Colab).
