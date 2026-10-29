# Plano de testes: To Do List

## 1. Objetivo

Encontrar o máximo de defeitos na aplicação <https://todolist.james.am/#/> e reportar cada um com evidência suficiente para o time reproduzir, priorizar e corrigir.

## 2. Escopo

**Dentro do escopo**

- Funcionalidades: criar, concluir, reabrir, editar e excluir tarefas; contador; “Mark all as complete”; limpar concluídas; filtros e rotas; persistência.
- Textos e interface.
- Robustez: várias abas, armazenamento cheio e dado inválido.
- Acessibilidade (WCAG 2.1 AA): teclado, foco, nomes acessíveis e contraste.
- Celular: layout em 375 px e toque.
- Segurança básica: injeção de HTML ou de expressão, cabeçalhos HTTP e dependências com vulnerabilidades conhecidas.
- Compatibilidade: Chrome, Firefox e WebKit (motor do Safari).

**Fora do escopo**

- Modo com backend. A aplicação procura `/api`, recebe 404 e usa só o `localStorage`, então esse modo não existe neste ambiente.
- Carga e desempenho. É uma página estática, sem servidor de aplicação. Fiz só uma checagem de volume com 1.000 tarefas.
- Aparelho Android real, Chrome para Android e leitores de tela reais. No celular, usei emulação, um iPhone 13 Pro e o emulador Android com Firefox; na acessibilidade, a árvore de acessibilidade e o axe-core.

## 3. Oráculos

1. **Especificação do TodoMVC** ([app-spec.md](https://github.com/tastejs/todomvc/blob/master/app-spec.md)). A página declara `data-framework="angularjs"` e salva na chave `todos-angularjs`, o padrão desse projeto.
2. **Implementação de referência** (tastejs/todomvc, `examples/angularjs`, commit `2cda67b`). Comparar o código publicado com ela aponta a linha provável de cada bug.
3. **WCAG 2.1 AA** para acessibilidade.
4. **Heurísticas de consistência (HICCUPPS).** O comportamento deve ser consistente com a especificação, com produtos parecidos, com a expectativa do usuário e consigo mesmo. Por exemplo, os nomes dos filtros devem seguir o mesmo padrão.

## 4. Ambiente

| Item | Versão |
|---|---|
| Sistema | macOS 26.2 |
| Navegadores | Google Chrome 156.0.8078.48; Chromium 156.0.8078.4, Firefox 157.0 e WebKit 27.2 via Playwright 1.64.1 |
| Celular | emulação de 375×667 px (`is_mobile`, toque) no Chromium e no WebKit; iPhone 13 Pro, iOS 26.0, Safari em aba privada |
| Android | emulador Pixel 3 com Android 9, Firefox 159 (APK oficial da Mozilla) e teclado Gboard |
| Aplicação | arquivos de 22/12/2019 (cabeçalho `Last-Modified`), AngularJS 1.4.3 |
| Ferramentas | DevTools, axe-core 4.10.2, `npm audit`, Python 3.12, pytest e Playwright |

Cada teste automatizado começa num contexto de navegador novo, então o `localStorage` começa vazio e um teste não interfere no outro.

## 5. Abordagem

### 5.1 Sessões exploratórias

| # | Missão | Foco |
|---|---|---|
| 1 | Criação de tarefas | Enter, aparar espaços, vazio e só espaços, caracteres invisíveis, texto longo, acentos e emoji, HTML e `{{ }}` |
| 2 | Conclusão, contador e “Mark all” | Transições de estado com 0, 1 e 2 ou mais pendentes; estado visual da caixa “Mark all” |
| 3 | Edição | Duplo clique, Enter, sair do campo, Esc, texto vazio, espaços, sequências como Esc seguido de Enter em outra tarefa |
| 4 | Exclusão e limpeza | Botão ×, “Clear” com e sem concluídas |
| 5 | Filtros e rotas | `#/`, `#/active`, `#/completed`, recarregar, voltar e avançar, rota inexistente, maiúsculas |
| 6 | Persistência e robustez | Recarregar, duas abas, armazenamento cheio, bloqueado e com valor inválido, 1.000 tarefas |
| 7 | Textos | Placeholder, rótulos, tooltip, rodapé, código-fonte |
| 8 | Acessibilidade e celular | Navegação só por teclado, foco visível, árvore de acessibilidade, axe-core, 375 px, 320 px, toque e duplo toque |
| 9 | Segurança e console | Injeção, cabeçalhos HTTP, iframe de outra origem, `npm audit`, erros de rede, arquivos expostos, bucket de hospedagem |

### 5.2 Técnicas

- **Partição de equivalência e valor-limite:** 0, 1 e 2 ou mais pendentes; texto vazio, com espaços e longo.
- **Transição de estados:** pendente/concluída; edição aberta, salva e descartada; filtros.
- **Testes negativos e de robustez:** falhas de armazenamento e concorrência entre abas.
- **Revisão do código publicado** contra a referência, para apontar a causa provável e encontrar defeitos sem efeito visível (seção 5 do relatório).
- **Compatibilidade:** a mesma suíte roda em Chromium, Firefox e WebKit.

### 5.3 Automação

A suíte em pytest e Playwright segue o padrão Page Object (`pages/todo_page.py`). Cada caso de teste verifica o comportamento **esperado**. Quando um bug conhecido impede esse comportamento, o teste recebe o marcador do bug (`bugs.py`), que aplica `xfail(strict=True)`:

- enquanto o bug existir, o teste aparece como `XFAIL` e a suíte fica verde;
- quando o bug for corrigido, o teste passa, vira `XPASS`, e o modo estrito faz a suíte falhar. Isso avisa que o marcador deve sair e transforma o teste em regressão.

## 6. Riscos priorizados

| Risco | Impacto | Onde o teste concentrou esforço |
|---|---|---|
| Informação errada sobre o que falta fazer | Alto: o usuário decide com base no contador | Contador e “Mark all” com 0, 1 e 2 ou mais pendentes |
| Perda de tarefas | Alto: perda de confiança no produto | Persistência, duas abas, armazenamento cheio, valor inválido |
| Ação em massa errada | Alto | “Mark all” e “Clear” |
| Exclusão de usuários de teclado, leitor de tela ou celular | Médio | Teclado, foco, nomes acessíveis, viewport |
| Textos errados ou internos expostos | Baixo para a função, alto para a imagem | Placeholder, tooltip, rodapé, código-fonte |

## 7. Severidade e prioridade

| Severidade | Critério |
|---|---|
| Alta | Resultado errado em função principal, perda de dados ou aplicação inutilizável |
| Média | Comportamento errado com contorno, ou que exclui um grupo de usuários |
| Baixa | Texto, visual ou configuração sem impacto funcional |

A prioridade (alta, média ou baixa) é a urgência sugerida. Ela combina a severidade com a frequência e a exposição. Um texto errado no primeiro campo da tela tem severidade baixa, mas prioridade média.

## 8. Critérios de entrada e de saída

- **Entrada:** aplicação acessível em `https://todolist.james.am`, a especificação do TodoMVC como referência e os navegadores instalados.
- **Saída:** todas as missões da seção 5.1 executadas; cada bug com passos, esperado, obtido e evidência; casos de teste com resultado; suíte automatizada verde (passou ou `XFAIL`) em Chromium, Firefox e WebKit.

## 9. Entregáveis

- [Relatório de bugs](relatorio-de-bugs.md), também em PDF em `docs/`.
- [Casos de teste](casos-de-teste.md) com resultados.
- Evidências em [`docs/evidencias/`](evidencias/), geradas por `scripts/evidencias.py`.
- Suíte automatizada (`tests/`) e pipeline no GitHub Actions (`.github/workflows/testes.yml`).
