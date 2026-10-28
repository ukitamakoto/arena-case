"""Persistência no localStorage (app-spec: Persistence) e comportamento quando o armazenamento falha."""
import re

import pytest
from playwright.sync_api import expect

from bugs import BUG_03, BUG_04, BUG_05
from pages.todo_page import TodoPage

# Ocupa a cota do localStorage com blocos cada vez menores, até nem 1 caractere caber.
ENCHER_COTA = """() => {
    let n = 0;
    for (const tamanho of [1 << 20, 1 << 16, 1 << 12, 1 << 8, 16, 1]) {
        const bloco = 'x'.repeat(tamanho);
        try { while (true) localStorage.setItem('ocupado-' + n++, bloco); } catch (e) {}
    }
}"""


def test_tarefas_e_estado_sobrevivem_ao_recarregar(todo):
    todo.adicionar("Comprar pão", "Pagar contas").alternar("Comprar pão")

    todo.page.reload()

    expect(todo.titulos).to_have_text(["Comprar pão", "Pagar contas"])
    expect(todo.item("Comprar pão")).to_have_class(re.compile(r"\bcompleted\b"))
    expect(todo.item("Pagar contas")).not_to_have_class(re.compile(r"\bcompleted\b"))


@BUG_03
def test_duas_abas_nao_apagam_as_tarefas_uma_da_outra(context):
    aba1 = TodoPage(context.new_page()).abrir()
    aba2 = TodoPage(context.new_page()).abrir()

    aba1.adicionar("Criada na aba 1")
    aba2.adicionar("Criada na aba 2")
    aba1.page.reload()

    expect(aba1.titulos).to_have_text(["Criada na aba 1", "Criada na aba 2"])


@BUG_04
@pytest.mark.only_browser("chromium")  # a cota e o erro de cota variam entre navegadores
def test_armazenamento_cheio_nao_trava_o_campo(todo):
    todo.adicionar("Já salva")
    todo.page.evaluate(ENCHER_COTA)

    todo.adicionar("Não cabe")

    expect(todo.campo_nova).to_be_enabled()


@BUG_05
def test_dado_invalido_no_armazenamento_nao_deixa_a_tela_em_branco(context):
    context.add_init_script(f"localStorage.setItem('{TodoPage.CHAVE_STORAGE}', '{{corrompido')")
    page = context.new_page()

    page.goto("/#/")

    expect(page.locator(".new-todo")).to_be_visible()
