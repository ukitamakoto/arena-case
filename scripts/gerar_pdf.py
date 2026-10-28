"""Gera docs/Relatorio_de_Bugs_Arena_Makoto_Ukita.pdf a partir de docs/relatorio-de-bugs.md.

Uso: uv run --with markdown python scripts/gerar_pdf.py
Links para outros arquivos do repositório viram links do GitHub, porque o PDF circula fora do repositório.
"""
import re
import tempfile
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[1]
DOCS = RAIZ / "docs"
REPO = "https://github.com/ukitamakoto/arena-case/blob/main/"
PDF = DOCS / "Relatorio_de_Bugs_Arena_Makoto_Ukita.pdf"

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm; }
body { font: 10pt/1.45 -apple-system, "Helvetica Neue", Arial, sans-serif; color: #1d2329; }
h1 { font-size: 21pt; margin: 0 0 6pt; color: #263238; }
h2 { font-size: 14pt; margin: 18pt 0 6pt; padding-bottom: 3pt; border-bottom: 2px solid #263238; break-after: avoid; }
h3 { font-size: 11.5pt; margin: 16pt 0 4pt; color: #263238; break-after: avoid; }
p, li { margin: 3pt 0; }
a { color: #1565c0; text-decoration: none; }
code { font: 8.6pt Menlo, Consolas, monospace; background: #f1f3f4; padding: 0 2pt; border-radius: 2pt; }
pre { background: #f1f3f4; padding: 6pt 8pt; white-space: pre-wrap; word-break: break-all; border-radius: 3pt; }
pre code { padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 8.8pt; break-inside: auto; }
th, td { border: 1px solid #cfd8dc; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #eceff1; }
td:first-child { white-space: nowrap; }
tr { break-inside: avoid; }
img { max-width: 49%; border: 1px solid #cfd8dc; margin: 4pt 0; break-inside: avoid; }
"""

RODAPE = ('<div style="font:7.5pt -apple-system,Helvetica,Arial,sans-serif;width:100%;padding:0 15mm;color:#78909c;display:flex;'
          'justify-content:space-between"><span>Relatório de bugs · To Do List · Makoto Ukita</span>'
          '<span><span class="pageNumber"></span>/<span class="totalPages"></span></span></div>')


def para_github(alvo: str) -> str:
    caminho, _, ancora = alvo.partition("#")
    relativo = (DOCS / caminho).resolve().relative_to(RAIZ).as_posix()
    return REPO + relativo + (f"#{ancora}" if ancora else "")


def main() -> None:
    texto = (DOCS / "relatorio-de-bugs.md").read_text(encoding="utf-8")
    texto = re.sub(r"\]\((?!https?:|#)([^)]+)\)", lambda m: f"]({para_github(m.group(1))})", texto)
    corpo = markdown.markdown(texto, extensions=["tables", "fenced_code", "sane_lists"])
    html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><base href="{DOCS.as_uri()}/">'
            f"<title>Relatório de bugs: To Do List</title><style>{CSS}</style></head><body>{corpo}</body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8", delete=False) as arquivo:
        arquivo.write(html)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(Path(arquivo.name).as_uri(), wait_until="load")
            page.pdf(path=PDF, prefer_css_page_size=True, print_background=True, display_header_footer=True,
                     header_template="<span></span>", footer_template=RODAPE)
            browser.close()
    finally:
        Path(arquivo.name).unlink()
    print(PDF)


if __name__ == "__main__":
    main()
