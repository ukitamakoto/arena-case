"""Contador de pendentes e botão de limpar concluídas (app-spec: Counter e Clear completed button)."""
import pytest
from playwright.sync_api import expect

from bugs import BUG_01, BUG_13, BUG_19


@BUG_01
@pytest.mark.parametrize(("pendentes", "concluidas", "texto"), [
    (1, 0, "1 item left"),
    (2, 0, "2 items left"),
    (1, 2, "1 item left"),
    (0, 2, "0 items left"),
])
def test_contador_mostra_quantas_tarefas_estao_pendentes(todo, pendentes, concluidas, texto):
    feitas = [f"Feita {i}" for i in range(concluidas)]
    todo.adicionar(*[f"Pendente {i}" for i in range(pendentes)], *feitas).alternar(*feitas)

    expect(todo.contador).to_have_text(texto)


def test_limpar_remove_apenas_as_concluidas(todo):
    todo.adicionar("Comprar pão", "Pagar contas", "Lavar o carro").alternar("Pagar contas")

    todo.limpar_concluidas.click()

    expect(todo.titulos).to_have_text(["Comprar pão", "Lavar o carro"])
    assert [t["title"] for t in todo.salvos()] == ["Comprar pão", "Lavar o carro"]


@BUG_13
def test_limpar_fica_oculto_sem_tarefas_concluidas(todo):
    todo.adicionar("Comprar pão")

    expect(todo.limpar_concluidas).to_be_hidden()


@BUG_19
def test_botao_de_limpar_diz_clear_completed(todo):
    todo.adicionar("Comprar pão").alternar("Comprar pão")

    expect(todo.limpar_concluidas).to_have_text("Clear completed")
