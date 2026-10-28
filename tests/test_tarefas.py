"""Criar, concluir, editar e excluir tarefas (app-spec do TodoMVC: New todo, Item e Editing)."""
import re

import pytest
from playwright.sync_api import expect

from bugs import BUG_06, BUG_24

CONCLUIDA = re.compile(r"\bcompleted\b")


def test_sem_tarefas_lista_e_rodape_ficam_ocultos(todo):
    expect(todo.lista).to_be_hidden()
    expect(todo.rodape).to_be_hidden()


def test_campo_de_nova_tarefa_recebe_foco_ao_abrir(todo):
    expect(todo.campo_nova).to_be_focused()


def test_enter_adiciona_tarefa_no_fim_da_lista_e_salva(todo):
    todo.adicionar("Comprar pão", "Pagar contas")

    expect(todo.titulos).to_have_text(["Comprar pão", "Pagar contas"])
    assert todo.salvos() == [{"title": "Comprar pão", "completed": False},
                             {"title": "Pagar contas", "completed": False}]


def test_espacos_nas_pontas_sao_removidos_ao_adicionar(todo):
    todo.adicionar("   Comprar pão   ")

    expect(todo.titulos).to_have_text(["Comprar pão"])
    assert todo.salvos()[0]["title"] == "Comprar pão"  # to_have_text normaliza espaços; o salvo não


@pytest.mark.parametrize("entrada", ["", "     "], ids=["vazia", "so-espacos"])
def test_tarefa_vazia_nao_e_criada(todo, entrada):
    todo.adicionar(entrada)

    expect(todo.itens).to_have_count(0)
    assert todo.salvos() == []


@BUG_24
def test_caractere_invisivel_nao_cria_tarefa(todo):
    todo.adicionar("\u200b")  # espaço de largura zero, comum em texto copiado da web

    expect(todo.itens).to_have_count(0)


@BUG_06
def test_campo_fica_vazio_depois_de_adicionar(todo):
    todo.adicionar("Comprar pão")

    expect(todo.campo_nova).to_have_value("")


def test_html_e_expressao_angular_aparecem_como_texto(todo):
    dialogos = []
    todo.page.on("dialog", lambda d: (dialogos.append(d.message), d.dismiss()))
    entradas = ["<img src=x onerror=alert(1)>", "{{7*7}}", "{{constructor.constructor('alert(2)')()}}"]

    todo.adicionar(*entradas)

    expect(todo.titulos).to_have_text(entradas)
    expect(todo.itens.locator("img")).to_have_count(0)
    assert dialogos == []


def test_concluir_e_reabrir_tarefa(todo):
    todo.adicionar("Comprar pão").alternar("Comprar pão")
    expect(todo.item("Comprar pão")).to_have_class(CONCLUIDA)
    assert todo.salvos()[0]["completed"] is True

    todo.alternar("Comprar pão")
    expect(todo.item("Comprar pão")).not_to_have_class(CONCLUIDA)
    assert todo.salvos()[0]["completed"] is False


def test_duplo_clique_abre_edicao_com_foco_e_esconde_os_controles(todo):
    todo.adicionar("Comprar pão")

    todo.item("Comprar pão").locator("label").dblclick()

    item = todo.item("Comprar pão")
    expect(item).to_have_class(re.compile(r"\bediting\b"))
    expect(item.locator(".edit")).to_be_focused()
    expect(item.locator(".edit")).to_have_value("Comprar pão")
    expect(item.locator(".toggle")).to_be_hidden()


@pytest.mark.parametrize("confirmar", ["Enter", "blur"])
def test_edicao_e_salva_com_enter_ou_ao_sair_do_campo(todo, confirmar):
    todo.adicionar("Comprar pão", "Pagar contas").editar("Comprar pão", "Comprar pão integral", confirmar)

    expect(todo.titulos).to_have_text(["Comprar pão integral", "Pagar contas"])
    expect(todo.page.locator(".todo-list li.editing")).to_have_count(0)
    assert todo.salvos()[0]["title"] == "Comprar pão integral"


def test_escape_descarta_a_edicao(todo):
    todo.adicionar("Comprar pão").editar("Comprar pão", "Texto descartado", "Escape")

    expect(todo.titulos).to_have_text(["Comprar pão"])
    assert todo.salvos()[0]["title"] == "Comprar pão"


def test_espacos_nas_pontas_sao_removidos_ao_editar(todo):
    todo.adicionar("Comprar pão").editar("Comprar pão", "   Comprar leite   ")

    assert todo.salvos()[0]["title"] == "Comprar leite"


def test_edicao_vazia_exclui_a_tarefa(todo):
    todo.adicionar("Comprar pão", "Pagar contas").editar("Comprar pão", "   ")

    expect(todo.titulos).to_have_text(["Pagar contas"])
    assert [t["title"] for t in todo.salvos()] == ["Pagar contas"]


def test_botao_excluir_aparece_no_hover_e_remove_a_tarefa(todo):
    todo.adicionar("Comprar pão", "Pagar contas")
    expect(todo.item("Comprar pão").locator(".destroy")).to_be_hidden()

    todo.excluir("Comprar pão")

    expect(todo.titulos).to_have_text(["Pagar contas"])
    assert [t["title"] for t in todo.salvos()] == ["Pagar contas"]
