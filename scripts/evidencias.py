"""Gera as evidências do relatório (docs/evidencias): prints anotados, o GIF do BUG-02 e as evidências em texto.

Uso: uv run python scripts/evidencias.py
As anotações (faixa com a legenda e contorno vermelho) são injetadas na página só para a captura.
"""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

URL = "https://todolist.james.am/#/"
SAIDA = Path(__file__).resolve().parents[1] / "docs" / "evidencias"
AXE = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js"
JANELA = {"width": 900, "height": 620}
RECORTE = {"x": 150, "y": 0, "width": 600, "height": 560}

ANOTAR = """([legenda, seletores]) => {
    let faixa = document.getElementById('evidencia-legenda');
    if (!faixa) {
        faixa = document.createElement('div');
        faixa.id = 'evidencia-legenda';
        faixa.style.cssText = 'position:absolute;top:0;left:0;right:0;padding:10px 160px;background:#263238;color:#fff;'
            + 'font:15px/1.35 Helvetica,Arial,sans-serif;text-align:center;z-index:9999';
        document.body.prepend(faixa);
        document.body.style.paddingTop = '64px';
    }
    faixa.textContent = legenda;
    document.querySelectorAll('[data-evidencia]').forEach(e => { e.style.outline = ''; e.removeAttribute('data-evidencia'); });
    for (const s of seletores) document.querySelectorAll(s).forEach(e => {
        e.setAttribute('data-evidencia', '');
        e.style.outline = '3px solid #e53935';
        e.style.outlineOffset = '2px';
    });
}"""


def abrir(browser, **opcoes) -> Page:
    contexto = browser.new_context(viewport=JANELA, locale="en-US", **opcoes)
    page = contexto.new_page()
    page.goto(URL)
    page.locator(".new-todo").wait_for()
    return page


def adicionar(page: Page, *titulos: str) -> None:
    for titulo in titulos:
        page.locator(".new-todo").fill(titulo)
        page.locator(".new-todo").press("Enter")


def alternar(page: Page, *titulos: str) -> None:
    for titulo in titulos:
        page.locator(".todo-list li", has=page.get_by_text(titulo, exact=True)).locator(".toggle").click()


def print_anotado(page: Page, nome: str, legenda: str, *seletores: str, recorte=RECORTE) -> None:
    page.mouse.move(0, 0)
    page.evaluate(ANOTAR, [legenda, list(seletores)])
    page.wait_for_timeout(500)  # fim das transições de cor do CSS
    page.screenshot(path=SAIDA / f"{nome}.png", clip=recorte)
    print(f"  {nome}.png")


def gif_bug_02(browser) -> None:
    if not shutil.which("ffmpeg"):
        print("  ffmpeg ausente: GIF do BUG-02 não gerado")
        return
    with tempfile.TemporaryDirectory() as pasta:
        contexto = browser.new_context(viewport=JANELA, locale="en-US", record_video_dir=pasta,
                                       record_video_size=JANELA)
        page = contexto.new_page()
        page.goto(URL)
        page.locator(".new-todo").wait_for()
        adicionar(page, "Comprar pão", "Pagar contas", "Lavar o carro")
        alternar(page, "Comprar pão", "Pagar contas")
        page.evaluate(ANOTAR, ["1/3 · Duas tarefas concluídas e uma pendente", [".todo-list"]])
        page.wait_for_timeout(2200)
        page.evaluate(ANOTAR, ["2/3 · Clique em “Mark all as complete” (seta) para concluir a última",
                               ["label[for=toggle-all]"]])
        page.wait_for_timeout(1800)
        page.locator("label[for=toggle-all]").click()
        page.evaluate(ANOTAR, ["3/3 · Resultado: as três tarefas voltaram a ficar pendentes", [".todo-list"]])
        page.wait_for_timeout(2500)
        video = page.video.path()
        contexto.close()
        filtro = ("fps=8,crop=600:560:150:0,scale=600:-1:flags=lanczos,split[a][b];"
                  "[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-vf", filtro, str(SAIDA / "BUG-02.gif")],
                       check=True)
        print("  BUG-02.gif")


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    textos = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = abrir(browser)
        print_anotado(page, "BUG-16", "Placeholder: “What need's to be done?” (correto: “What needs to be done?”)",
                      ".new-todo")
        print_anotado(page, "BUG-17", "Rodapé: “Double-click to edit a toodo” (correto: “todo”)", ".info p")

        adicionar(page, "Comprar pão", "Pagar contas", "Lavar o carro")
        alternar(page, "Comprar pão", "Pagar contas")
        print_anotado(page, "BUG-01-um-pendente", "1 tarefa pendente, mas o contador mostra “0 items left”",
                      ".todo-count")
        print_anotado(page, "BUG-02-antes", "Antes do clique: 1 pendente e a seta de “Mark all” já aparece marcada",
                      "label[for=toggle-all]", ".todo-list li:not(.completed)")
        page.locator("label[for=toggle-all]").click()
        print_anotado(page, "BUG-02-depois", "Depois de 1 clique em “Mark all as complete”: todas voltaram a pendentes",
                      ".todo-list")
        print_anotado(page, "BUG-18", "Filtro “active” em minúsculas, diferente de “All” e “Completed”",
                      '.filters a[href="#/active"]')
        print_anotado(page, "BUG-13", "Nenhuma tarefa concluída, mas o botão “Clear” aparece", ".clear-completed")
        page.locator("label[for=toggle-all]").click()
        print_anotado(page, "BUG-01-todas-concluidas", "Todas as 3 tarefas concluídas: contador mostra “-1 items left”",
                      ".todo-count")
        print_anotado(page, "BUG-07", "Todas concluídas, mas a seta de “Mark all” aparece desmarcada (cinza-claro)",
                      "label[for=toggle-all]")
        print_anotado(page, "BUG-19", "O botão diz só “Clear”: não deixa claro que remove apenas as concluídas",
                      ".clear-completed")
        page.goto("https://todolist.james.am/#/xyz")
        page.locator(".new-todo").wait_for()
        print_anotado(page, "BUG-20", "Rota inexistente #/xyz: lista tudo e nenhum filtro fica destacado", ".filters")
        page.context.close()

        page = abrir(browser)
        adicionar(page, "Comprar pão")
        page.locator(".new-todo").press("ControlOrMeta+a")
        print_anotado(page, "BUG-06", "Depois de adicionar, o campo ficou com 3 espaços (trecho selecionado) e o placeholder sumiu",
                      ".new-todo")
        page.context.close()

        page = abrir(browser)
        adicionar(page, "\u200b")
        print_anotado(page, "BUG-24", "Só um caractere de largura zero (U+200B) no campo: a tarefa foi criada sem texto",
                      ".todo-list li")
        page.context.close()

        page = abrir(browser)
        adicionar(page, "Comprar pão")
        page.keyboard.press("Tab")  # campo -> "Mark all"
        page.keyboard.press("Tab")  # -> checkbox da tarefa
        print_anotado(page, "BUG-11", "O foco do teclado está no checkbox de “Comprar pão”, mas nada na tela mostra isso")
        print_anotado(page, "BUG-08", "Com o foco na tarefa, o botão excluir (×) não aparece e o Tab nunca chega a ele",
                      ".todo-list li")
        textos["aria_snapshot"] = page.locator(".todoapp").aria_snapshot()
        page.add_script_tag(url=AXE)
        resultado = page.evaluate("axe.run(document, {runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']})")
        textos["axe"] = [{"regra": v["id"], "impacto": v["impact"], "nos": [
            {"alvo": n["target"][0], "dados": (n["any"][0].get("data") if n["any"] else None)} for n in v["nodes"]]}
            for v in resultado["violations"]]
        page.context.close()

        aba1 = abrir(browser)
        aba2 = aba1.context.new_page()
        aba2.goto(URL)
        aba2.locator(".new-todo").wait_for()
        adicionar(aba1, "Criada na aba 1")
        adicionar(aba2, "Criada na aba 2")
        aba1.reload()
        aba1.locator(".new-todo").wait_for()
        print_anotado(aba1, "BUG-03", "Aba 1 recarregada: “Criada na aba 1” sumiu, apagada pela gravação da aba 2",
                      ".todo-list")
        aba1.context.close()

        page = abrir(browser)
        adicionar(page, "Já salva")
        page.evaluate("""() => {
            let n = 0;
            for (const tamanho of [1 << 20, 1 << 16, 1 << 12, 1 << 8, 16, 1]) {
                const bloco = 'x'.repeat(tamanho);
                try { while (true) localStorage.setItem('ocupado-' + n++, bloco); } catch (e) {}
            }
        }""")
        adicionar(page, "Não cabe")
        print_anotado(page, "BUG-04", "localStorage cheio: “Não cabe” aparece, mas não foi salva e o campo travou desabilitado",
                      ".new-todo", ".todo-list li:last-child")
        page.context.close()

        contexto = browser.new_context(viewport=JANELA, locale="en-US")
        contexto.add_init_script("localStorage.setItem('todos-angularjs', '{corrompido')")
        page = contexto.new_page()
        page.goto(URL)
        page.wait_for_timeout(1500)
        print_anotado(page, "BUG-05", "Valor inválido em todos-angularjs: a aplicação não aparece (SyntaxError no console)")
        contexto.close()

        celular = browser.new_context(viewport={"width": 375, "height": 667}, is_mobile=True, has_touch=True,
                                      device_scale_factor=2, locale="en-US")
        page = celular.new_page()
        page.goto(URL)
        page.locator(".new-todo").wait_for()
        adicionar(page, "Comprar pão", "Pagar contas")
        page.wait_for_timeout(500)
        page.screenshot(path=SAIDA / "BUG-09.png")
        print("  BUG-09.png")
        celular.close()

        falhas = []
        page = browser.new_context().new_page()
        page.on("response", lambda r: falhas.append(f"HTTP {r.status} GET {r.url}") if r.status >= 400 else None)
        page.goto(URL)
        page.wait_for_load_state("networkidle")
        textos["erros_de_rede"] = falhas
        textos["cabecalhos"] = page.request.get("https://todolist.james.am/").headers
        textos["angular"] = page.evaluate("angular.version.full")
        page.context.close()

        gif_bug_02(browser)
        browser.close()
    print(json.dumps(textos, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
