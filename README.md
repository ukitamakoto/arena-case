# Arena · Jr. QA Engineer Tech Case

Testes da aplicação **To Do List** (<https://todolist.james.am/#/>): bugs encontrados, documentação de QA e uma suíte automatizada que reproduz cada bug.

**25 bugs encontrados**: 5 de severidade alta, 7 de média e 13 de baixa. A suíte automatizada cobre 23 deles e roda em Chrome, Firefox e WebKit.

| Documento | Conteúdo |
|---|---|
| [Relatório de bugs](docs/relatorio-de-bugs.md) ([PDF](docs/Relatorio_de_Bugs_Arena_Makoto_Ukita.pdf)) | Resumo, método, lista priorizada e detalhamento de cada bug, com passos, esperado, obtido, evidência e causa provável |
| [Plano de testes](docs/plano-de-testes.md) | Escopo, oráculos, ambiente, sessões exploratórias, técnicas, riscos e critérios |
| [Casos de teste](docs/casos-de-teste.md) | 64 casos com resultado; cada falha aponta o bug e o teste automatizado |
| [Evidências](docs/evidencias/) | Prints anotados e o GIF do BUG-02, gerados por `scripts/evidencias.py` |

## Principais achados

- **Uma linha causa quatro bugs.** `todoCtrl.js:18` subtrai 1 da contagem de pendentes. O contador chega a “-1 items left” (BUG-01). Com 1 pendente, “Mark all as complete” reabre todas as tarefas (BUG-02). Com tudo concluído, a caixa aparece desmarcada (BUG-07). E o botão “Clear” aparece sem nada concluído (BUG-13).
- **Perda de dados.** Duas abas abertas apagam as tarefas uma da outra (BUG-03). Com o armazenamento cheio, a tarefa não é salva e o campo trava (BUG-04). Com o armazenamento bloqueado pela configuração de privacidade do navegador, ou com um valor inválido salvo, a tela fica em branco (BUG-05).
- **Uso diário.** O campo fica com 3 espaços depois de cada tarefa adicionada (BUG-06). Não há `meta viewport`, então no celular a página aparece reduzida (BUG-09). Excluir e editar não funcionam pelo teclado (BUG-08).

![BUG-02: com uma tarefa pendente, “Mark all as complete” reabre todas](docs/evidencias/BUG-02.gif)

## Automação

Python 3.12, pytest, Playwright e uv, no padrão Page Object (`pages/todo_page.py`).

Cada teste verifica o comportamento **esperado**, segundo a especificação do TodoMVC. Se um bug conhecido impede esse comportamento, o teste leva o marcador do bug, definido em `bugs.py`. O marcador aplica `xfail(strict=True)` com o código do bug:

- enquanto o bug existir, o teste aparece como `XFAIL` e a suíte fica verde;
- quando o bug for corrigido, o teste vira `XPASS` e a suíte falha, avisando para remover o marcador. A partir daí, o teste vale como regressão.

```bash
uv sync
uv run playwright install chromium firefox webkit
uv run pytest                                                  # Chromium
uv run pytest --browser firefox --browser webkit               # outros motores
uv run pytest --browser-channel chrome                         # Google Chrome instalado
uv run pytest --runxfail                                       # mostra a falha real de cada bug
```

Resultado em 28/10/2026, por navegador: **24 passed e 30 xfailed** no Chromium e no Chrome. O teste de armazenamento cheio só roda no Chromium, então é pulado no Firefox e no WebKit. O teste de celular também é pulado no Firefox, que não emula `is_mobile`. Os relatórios ficam em `reports/relatorio.html` (pytest-html) e `reports/junit.xml`. Se um teste falhar, o trace e o print ficam em `test-results/`.

O GitHub Actions (`.github/workflows/testes.yml`) roda a suíte nos três navegadores a cada push e pull request, e publica os relatórios como artefato.

## Estrutura

```
├── bugs.py                  # marcadores xfail de cada bug conhecido
├── conftest.py              # contexto do navegador, checagem de ambiente, fixture `todo`
├── pages/todo_page.py       # Page Object
├── tests/                   # 54 testes (por área)
├── scripts/
│   ├── evidencias.py        # gera docs/evidencias (prints anotados + GIF; GIF exige ffmpeg)
│   └── gerar_pdf.py         # gera o PDF do relatório a partir do Markdown
└── docs/                    # relatório, plano, casos de teste e evidências
```

Para regerar as evidências e o PDF:

```bash
uv run python scripts/evidencias.py
uv run --with markdown python scripts/gerar_pdf.py
```

Autor: Makoto Ukita
