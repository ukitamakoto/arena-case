"""Textos que o usuário vê e conteúdo público da página."""
import re

from playwright.sync_api import expect

from bugs import BUG_14, BUG_15, BUG_16, BUG_17, BUG_18


@BUG_16
def test_placeholder_do_campo_de_nova_tarefa(todo):
    expect(todo.campo_nova).to_have_attribute("placeholder", "What needs to be done?")


@BUG_17
def test_instrucao_de_edicao_no_rodape(todo):
    expect(todo.instrucao).to_have_text("Double-click to edit a todo")


@BUG_18
def test_nomes_dos_filtros_seguem_o_mesmo_padrao(todo):
    todo.adicionar("Comprar pão")

    expect(todo.filtros).to_have_text(["All", "Active", "Completed"])


@BUG_14
def test_botao_excluir_nao_mostra_anotacao_interna(todo):
    todo.adicionar("Comprar pão")

    expect(todo.item("Comprar pão").locator(".destroy")).not_to_have_attribute("title", re.compile("TODO"))


@BUG_15
def test_html_publico_sem_comentario_ofensivo(page, base_url):
    html = page.request.get(f"{base_url}/").text()

    assert "stupid" not in html.lower()
