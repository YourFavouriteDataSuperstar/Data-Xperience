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
