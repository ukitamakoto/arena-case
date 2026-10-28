"""Filtros por rota: #/, #/active e #/completed (app-spec: Routing)."""
import re

import pytest
from playwright.sync_api import expect

from bugs import BUG_20


@pytest.mark.parametrize(("rota", "visiveis"), [
    ("/active", ["Pagar contas"]),
    ("/completed", ["Comprar pão"]),
    ("/", ["Comprar pão", "Pagar contas"]),
])
def test_filtro_mostra_as_tarefas_certas_e_fica_destacado(todo, rota, visiveis):
    todo.adicionar("Comprar pão", "Pagar contas").alternar("Comprar pão")

    todo.filtrar(rota)

    expect(todo.titulos).to_have_text(visiveis)
    expect(todo.filtro_selecionado).to_have_attribute("href", f"#{rota}")


def test_filtro_continua_aplicado_depois_de_recarregar(todo):
    todo.adicionar("Comprar pão", "Pagar contas").alternar("Comprar pão").filtrar("/completed")

    todo.page.reload()

    expect(todo.titulos).to_have_text(["Comprar pão"])
    expect(todo.filtro_selecionado).to_have_attribute("href", "#/completed")


def test_tarefa_concluida_sai_da_visao_de_pendentes(todo):
    todo.adicionar("Comprar pão", "Pagar contas").filtrar("/active")

    todo.alternar("Comprar pão")

    expect(todo.titulos).to_have_text(["Pagar contas"])


@BUG_20
@pytest.mark.parametrize("rota", ["/xyz", "/Active"])
def test_rota_inexistente_volta_para_todas(todo, rota):
    todo.adicionar("Comprar pão")

    todo.abrir(rota)

    expect(todo.page).to_have_url(re.compile(r"#/$"))
