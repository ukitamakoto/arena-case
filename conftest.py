"""Configuração da suíte: contexto do navegador, disponibilidade da aplicação e Page Object pronto."""
import pytest
from playwright.sync_api import expect

from pages.todo_page import TodoPage

# A tela do AngularJS reage na hora; 3 s sobram e encurtam a espera dos testes que esperam um bug.
expect.set_options(timeout=3_000)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 800}, "locale": "en-US"}


@pytest.fixture(scope="session", autouse=True)
def aplicacao_disponivel(base_url, playwright):
    """Falha cedo, com mensagem clara, se a aplicação estiver fora do ar (não é regressão do produto)."""
    api = playwright.request.new_context(base_url=base_url)
    try:
        resposta = api.get("/", timeout=30_000)
        ok, detalhe = resposta.ok, f"HTTP {resposta.status}"
    except Exception as erro:  # rede, DNS, timeout
        ok, detalhe = False, str(erro)
    finally:
        api.dispose()
    if not ok:
        pytest.exit(f"Aplicação indisponível em {base_url}: {detalhe}", returncode=3)


@pytest.fixture
def todo(page) -> TodoPage:
    """Aplicação aberta em #/ num contexto novo: o localStorage começa vazio em cada teste."""
    return TodoPage(page).abrir()
