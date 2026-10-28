"""Acessibilidade (WCAG 2.1 AA): teclado, foco visível, nomes acessíveis e tela de celular."""
import pytest
from playwright.sync_api import expect

from bugs import BUG_08, BUG_09, BUG_11, BUG_12


def percorrer_com_tab(page, vezes: int = 12) -> list[str]:
    """Classes de cada elemento que recebe foco ao apertar Tab, a partir do topo da página."""
    page.locator("h1").click()
    focados = []
    for _ in range(vezes):
        page.keyboard.press("Tab")
        focados.append(page.evaluate("document.activeElement.className"))
    return focados


@BUG_08
def test_botao_excluir_e_alcancavel_pelo_teclado(todo):
    todo.adicionar("Comprar pão")

    focados = percorrer_com_tab(todo.page)

    assert any("destroy" in classe for classe in focados), f"Tab nunca chega ao botão de excluir: {focados}"


@BUG_11
def test_checkbox_focado_pelo_teclado_tem_indicador_visivel(todo):
    todo.adicionar("Comprar pão")
    item = todo.item("Comprar pão")
    todo.page.mouse.move(0, 0)  # sem hover: o botão de excluir não aparece na comparação
    todo.page.wait_for_timeout(500)  # fim da transição de cor do item
    sem_foco = item.screenshot()

    todo.page.keyboard.press("Tab")  # campo de nova tarefa -> "Mark all"
    todo.page.keyboard.press("Tab")  # -> checkbox da tarefa
    expect(item.locator(".toggle")).to_be_focused()

    assert item.screenshot() != sem_foco, "nada muda na tela quando o checkbox recebe foco"


@BUG_12
def test_checkbox_da_tarefa_tem_nome_acessivel(todo):
    todo.adicionar("Comprar pão")

    expect(todo.page.get_by_role("checkbox", name="Comprar pão")).to_have_count(1)


@BUG_09
@pytest.mark.skip_browser("firefox")  # o Firefox do Playwright não emula is_mobile
@pytest.mark.browser_context_args(viewport={"width": 375, "height": 667}, is_mobile=True, has_touch=True)
def test_pagina_usa_a_largura_da_tela_do_celular(todo):
    assert todo.page.evaluate("window.innerWidth") == 375
