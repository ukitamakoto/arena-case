from playwright.sync_api import Locator, Page


class TodoPage:
    CHAVE_STORAGE = "todos-angularjs"

    def __init__(self, page: Page):
        self.page = page
        self.campo_nova = page.locator(".new-todo")
        self.lista = page.locator(".main")
        self.itens = page.locator(".todo-list li")
        self.titulos = self.itens.locator("label")
        self.marcar_todos = page.locator("#toggle-all")
        self.contador = page.locator(".todo-count")
        self.filtros = page.locator(".filters a")
        self.filtro_selecionado = page.locator(".filters a.selected")
        self.limpar_concluidas = page.locator(".clear-completed")
        self.rodape = page.locator(".footer")
        self.instrucao = page.locator(".info")

    def abrir(self, rota: str = "/") -> "TodoPage":
        self.page.goto(f"/#{rota}")
        self.campo_nova.wait_for()
        return self

    def adicionar(self, *titulos: str) -> "TodoPage":
        for titulo in titulos:
            self.campo_nova.fill(titulo)
            self.campo_nova.press("Enter")
        return self

    def item(self, titulo: str) -> Locator:
        return self.itens.filter(has=self.page.get_by_text(titulo, exact=True))

    def alternar(self, *titulos: str) -> "TodoPage":
        for titulo in titulos:
            self.item(titulo).locator(".toggle").click()
        return self

    def clicar_marcar_todos(self) -> "TodoPage":
        # O checkbox real fica invisível (opacity 0); quem recebe o clique é o rótulo com a seta.
        self.page.locator("label[for=toggle-all]").click()
        return self

    def editar(self, titulo: str, novo: str, confirmar: str = "Enter") -> "TodoPage":
        """confirmar: tecla pressionada no campo (Enter, Escape) ou "blur" para clicar fora dele."""
        self.item(titulo).locator("label").dblclick()
        campo = self.page.locator(".todo-list li.editing .edit")
        campo.fill(novo)
        if confirmar == "blur":
            self.page.locator("h1").click()
        else:
            campo.press(confirmar)
        return self

    def excluir(self, titulo: str) -> "TodoPage":
        item = self.item(titulo)
        item.hover()  # o botão só aparece com o mouse sobre a tarefa
        item.locator(".destroy").click()
        return self

    def filtrar(self, rota: str) -> "TodoPage":
        self.page.locator(f'.filters a[href="#{rota}"]').click()
        return self

    def salvos(self) -> list[dict]:
        return self.page.evaluate(f"JSON.parse(localStorage.getItem('{self.CHAVE_STORAGE}') || '[]')")
