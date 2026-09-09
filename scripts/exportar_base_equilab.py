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
