# -*- coding: utf-8 -*-
"""Extrai as figuras do notebook executado para _figs/, que o relatorio usa.

As imagens nao sao versionadas: sao derivadas do notebook. Rode este script
antes de compilar o relatorio_d23bda.tex.

    python extrair_figuras.py && pdflatex relatorio_d23bda.tex
"""
import base64
import json
import re
from pathlib import Path

NOTEBOOK = Path("avaliacao_d23bda.ipynb")
DESTINO = Path("_figs")

nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
DESTINO.mkdir(exist_ok=True)

n, item = 0, "0"
for celula in nb["cells"]:
    if celula["cell_type"] == "markdown":
        titulo = re.search(r"^#+ ([A-J]) [—-]", "".join(celula["source"]), re.M)
        if titulo:
            item = titulo.group(1).lower()
    for saida in celula.get("outputs", []):
        png = saida.get("data", {}).get("image/png")
        if png:
            n += 1
            caminho = DESTINO / f"fig_{item}_{n:02d}.png"
            caminho.write_bytes(base64.b64decode(png))
            print(f"{caminho}  ({caminho.stat().st_size / 1024:.0f} KB)")

print(f"\n{n} figuras extraidas para {DESTINO}/")
