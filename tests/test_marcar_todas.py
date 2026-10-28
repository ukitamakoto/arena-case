"""Caixa "Mark all as complete" (app-spec: Mark all as complete)."""
import re

from playwright.sync_api import expect

from bugs import BUG_02, BUG_07

CONCLUIDA = re.compile(r"\bcompleted\b")


def test_marcar_todas_conclui_todas_as_pendentes(todo):
    todo.adicionar("A", "B", "C").clicar_marcar_todos()

    for titulo in ("A", "B", "C"):
        expect(todo.item(titulo)).to_have_class(CONCLUIDA)
    assert all(t["completed"] for t in todo.salvos())


@BUG_02
def test_marcar_todas_com_uma_pendente_conclui_todas(todo):
    todo.adicionar("A", "B", "C").alternar("A", "B")

    todo.clicar_marcar_todos()

    for titulo in ("A", "B", "C"):
        expect(todo.item(titulo)).to_have_class(CONCLUIDA)


@BUG_02
def test_caixa_fica_desmarcada_enquanto_houver_pendente(todo):
    todo.adicionar("A", "B").alternar("A")

    expect(todo.marcar_todos).not_to_be_checked()


@BUG_07
def test_caixa_fica_marcada_quando_todas_estao_concluidas(todo):
    todo.adicionar("A", "B").alternar("A", "B")

    expect(todo.marcar_todos).to_be_checked()


@BUG_07
def test_um_clique_reabre_todas_quando_todas_estao_concluidas(todo):
    todo.adicionar("A", "B").clicar_marcar_todos()

    todo.clicar_marcar_todos()

    for titulo in ("A", "B"):
        expect(todo.item(titulo)).not_to_have_class(CONCLUIDA)
