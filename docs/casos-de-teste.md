# Casos de teste: To Do List

Executados em 28/10/2026 em Chrome 156, Firefox 157 e WebKit 27.2. Os casos de toque e layout também foram feitos em 29/10/2026 num iPhone 13 Pro com iOS 26.0 (Safari). Ambiente e critérios estão no [plano de testes](plano-de-testes.md), e os bugs, no [relatório](relatorio-de-bugs.md).

A coluna **Automação** traz o teste em `tests/` que cobre o caso. “Manual” indica um caso verificado só na exploração.

**Resultado:** 61 casos; 32 passaram e 29 falharam. As falhas cobrem os 25 bugs.

## Criação de tarefas

| ID | Cenário | Esperado | Status | Bug | Automação |
|---|---|---|---|---|---|
| CT-01 | Abrir a aplicação sem tarefas | Lista e rodapé ocultos | Passou | | `test_sem_tarefas_lista_e_rodape_ficam_ocultos` |
| CT-02 | Abrir a aplicação | Foco no campo de nova tarefa | Passou | | `test_campo_de_nova_tarefa_recebe_foco_ao_abrir` |
| CT-03 | Digitar e pressionar Enter (2 tarefas) | Tarefas no fim da lista, na ordem, salvas no `localStorage` | Passou | | `test_enter_adiciona_tarefa_no_fim_da_lista_e_salva` |
| CT-04 | Adicionar `"   Comprar pão   "` | Título salvo sem os espaços das pontas | Passou | | `test_espacos_nas_pontas_sao_removidos_ao_adicionar` |
| CT-05 | Enter com o campo vazio ou só com espaços | Nada é criado | Passou | | `test_tarefa_vazia_nao_e_criada` (2 variações) |
| CT-06 | Enter com caractere invisível: U+200B, U+00A0, tabulação, U+3000 | Nada é criado | **Falhou** (só U+200B) | BUG-24 | `test_caractere_invisivel_nao_cria_tarefa` |
| CT-07 | Adicionar uma tarefa | Campo volta vazio, com o placeholder | **Falhou** | BUG-06 | `test_campo_fica_vazio_depois_de_adicionar` |
| CT-08 | Adicionar `<img src=x onerror=alert(1)>`, `{{7*7}}` e `{{constructor.constructor('alert(2)')()}}` | Texto exibido literalmente, sem imagem nem alerta | Passou | | `test_html_e_expressao_angular_aparecem_como_texto` |
| CT-09 | Adicionar 300 caracteres sem espaço | Quebra de linha, sem rolagem horizontal | Passou | | Manual |
| CT-10 | Adicionar texto com acentos e emoji | Texto exibido corretamente | Passou | | Manual |
| CT-11 | Ler o placeholder | “What needs to be done?” | **Falhou** | BUG-16 | `test_placeholder_do_campo_de_nova_tarefa` |

## Concluir e excluir

| ID | Cenário | Esperado | Status | Bug | Automação |
|---|---|---|---|---|---|
| CT-12 | Marcar e desmarcar o checkbox de uma tarefa | Classe `completed` alterna e o estado é salvo | Passou | | `test_concluir_e_reabrir_tarefa` |
| CT-13 | Passar o mouse sobre a tarefa e clicar no × | Botão aparece só no hover e remove a tarefa | Passou | | `test_botao_excluir_aparece_no_hover_e_remove_a_tarefa` |
| CT-14 | Deixar o mouse sobre o × | Nenhum tooltip, ou um tooltip útil | **Falhou** | BUG-14 | `test_botao_excluir_nao_mostra_anotacao_interna` |

## Edição

| ID | Cenário | Esperado | Status | Bug | Automação |
|---|---|---|---|---|---|
| CT-15 | Duplo clique no título | Modo de edição, campo com o título e foco, controles ocultos | Passou | | `test_duplo_clique_abre_edicao_com_foco_e_esconde_os_controles` |
| CT-16 | Editar e pressionar Enter | Título salvo e edição encerrada | Passou | | `test_edicao_e_salva_com_enter_ou_ao_sair_do_campo[Enter]` |
| CT-17 | Editar e clicar fora do campo | Título salvo e edição encerrada | Passou | | `test_edicao_e_salva_com_enter_ou_ao_sair_do_campo[blur]` |
| CT-18 | Editar e pressionar Esc | Alteração descartada | Passou | | `test_escape_descarta_a_edicao` |
| CT-19 | Editar para `"   Comprar leite   "` | Título salvo sem os espaços das pontas | Passou | | `test_espacos_nas_pontas_sao_removidos_ao_editar` |
| CT-20 | Editar para vazio ou só espaços | Tarefa excluída | Passou | | `test_edicao_vazia_exclui_a_tarefa` |
| CT-21 | Esc numa tarefa e Enter em outra; Enter numa e clique fora em outra | A segunda edição é salva normalmente | Passou | | Manual, nos 3 navegadores |
| CT-22 | Editar digitando tecla a tecla, com espaço no meio e no fim | Espaços aparecem durante a digitação; título salvo aparado | Passou | | Manual |
| CT-23 | Ler a instrução do rodapé | “Double-click to edit a todo” | **Falhou** | BUG-17 | `test_instrucao_de_edicao_no_rodape` |

## Contador e limpar concluídas

| ID | Cenário | Esperado | Status | Bug | Automação |
|---|---|---|---|---|---|
| CT-24 | Contador com 1 pendente; 2 pendentes; 1 pendente e 2 concluídas; 0 pendentes e 2 concluídas | “1 item left”, “2 items left”, “1 item left”, “0 items left” | **Falhou** | BUG-01 | `test_contador_mostra_quantas_tarefas_estao_pendentes` (4 variações) |
| CT-25 | “Clear” com 1 de 3 tarefas concluída | Remove só a concluída, inclusive do armazenamento | Passou | | `test_limpar_remove_apenas_as_concluidas` |
| CT-26 | Lista sem tarefas concluídas | Botão de limpar oculto | **Falhou** | BUG-13 | `test_limpar_fica_oculto_sem_tarefas_concluidas` |
| CT-27 | Ler o rótulo do botão de limpar | “Clear completed” | **Falhou** | BUG-19 | `test_botao_de_limpar_diz_clear_completed` |

## Mark all as complete

| ID | Cenário | Esperado | Status | Bug | Automação |
|---|---|---|---|---|---|
| CT-28 | Clicar com todas as tarefas pendentes | Todas concluídas | Passou | | `test_marcar_todas_conclui_todas_as_pendentes` |
| CT-29 | Clicar com só 1 pendente | Todas concluídas | **Falhou** | BUG-02 | `test_marcar_todas_com_uma_pendente_conclui_todas`; no iPhone 13 Pro, com 1 tarefa, o 1º toque não conclui |
| CT-30 | Observar a caixa com 1 pendente | Caixa desmarcada | **Falhou** | BUG-02 | `test_caixa_fica_desmarcada_enquanto_houver_pendente` |
| CT-31 | Observar a caixa com todas concluídas | Caixa marcada | **Falhou** | BUG-07 | `test_caixa_fica_marcada_quando_todas_estao_concluidas` |
| CT-32 | Clicar uma vez com todas concluídas | Todas reabertas | **Falhou** | BUG-07 | `test_um_clique_reabre_todas_quando_todas_estao_concluidas`; confirmado no iPhone 13 Pro |

## Filtros e rotas

| ID | Cenário | Esperado | Status | Bug | Automação |
|---|---|---|---|---|---|
| CT-33 | Clicar em active, Completed e All | Só as tarefas do filtro; link destacado | Passou | | `test_filtro_mostra_as_tarefas_certas_e_fica_destacado` (3 variações) |
| CT-34 | Recarregar em `#/completed` | Filtro mantido | Passou | | `test_filtro_continua_aplicado_depois_de_recarregar` |
| CT-35 | Concluir uma tarefa na visão `#/active` | A tarefa sai da lista filtrada | Passou | | `test_tarefa_concluida_sai_da_visao_de_pendentes` |
| CT-36 | Usar voltar e avançar do navegador entre filtros | Lista e destaque acompanham a URL | Passou | | `test_voltar_e_avancar_do_navegador_respeitam_o_filtro` |
| CT-37 | Ler os nomes dos filtros | “All”, “Active”, “Completed” | **Falhou** | BUG-18 | `test_nomes_dos_filtros_seguem_o_mesmo_padrao` |
| CT-38 | Abrir `#/xyz` e `#/Active` | Volta para `#/` | **Falhou** | BUG-20 | `test_rota_inexistente_volta_para_todas` (2 variações) |

## Persistência e robustez

| ID | Cenário | Esperado | Status | Bug | Automação |
|---|---|---|---|---|---|
| CT-39 | Recarregar a página | Tarefas e estados mantidos | Passou | | `test_tarefas_e_estado_sobrevivem_ao_recarregar` |
| CT-40 | Criar uma tarefa em cada aba e recarregar a primeira | As duas tarefas aparecem | **Falhou** | BUG-03 | `test_duas_abas_nao_apagam_as_tarefas_uma_da_outra` |
| CT-41 | Adicionar tarefa com o `localStorage` cheio | Aviso de erro; campo continua utilizável | **Falhou** | BUG-04 | `test_armazenamento_cheio_nao_trava_o_campo` (Chromium) |
| CT-42 | Abrir com o armazenamento bloqueado (Chrome sem permissão para salvar dados de sites; Safari com “Bloquear Todos os Cookies”) | Aplicação abre e avisa que não vai salvar | **Falhou** | BUG-05 | `test_armazenamento_bloqueado_nao_deixa_a_tela_em_branco`; confirmado no Chrome 156 e no iPhone 13 Pro |
| CT-43 | Abrir com um valor inválido em `todos-angularjs` | Aplicação abre normalmente | **Falhou** | BUG-05 | `test_dado_invalido_no_armazenamento_nao_deixa_a_tela_em_branco` |
| CT-44 | Carregar 1.000 tarefas e concluir, adicionar e marcar todas | Cada ação responde em menos de 1 s | Passou | | Manual (até 0,3 s no Chromium) |

## Acessibilidade e celular

| ID | Cenário | Esperado | Status | Bug | Automação |
|---|---|---|---|---|---|
| CT-45 | Chegar ao botão excluir usando só o Tab | O botão recebe foco | **Falhou** | BUG-08 | `test_botao_excluir_e_alcancavel_pelo_teclado` |
| CT-46 | Editar uma tarefa usando só o teclado (Enter e F2 no checkbox) | Existe um atalho de teclado | **Falhou** | BUG-08 | Manual |
| CT-47 | Focar o checkbox da tarefa com Tab | Indicador de foco visível | **Falhou** | BUG-11 | `test_checkbox_focado_pelo_teclado_tem_indicador_visivel` |
| CT-48 | Ler a árvore de acessibilidade | Checkbox com o nome da tarefa | **Falhou** | BUG-12 | `test_checkbox_da_tarefa_tem_nome_acessivel` |
| CT-49 | Rodar o axe-core (WCAG 2.1 AA) | Sem violação de contraste | **Falhou** | BUG-21 | Manual |
| CT-50 | Abrir em tela de 375 px (celular) | Layout com 375 px de largura | **Falhou** | BUG-09 | `test_pagina_usa_a_largura_da_tela_do_celular` (Chromium e WebKit); confirmado no iPhone 13 Pro |
| CT-51 | Abrir em janela de 320 px no desktop (reflow, WCAG 1.4.10) | Sem rolagem horizontal | Passou | | Manual |
| CT-52 | Tocar na tarefa no celular e depois no × | O × aparece e remove a tarefa | Passou | | Manual: Chromium emulado e iPhone 13 Pro |
| CT-53 | Duplo toque no título no celular | Abre a edição | Passou | | Manual: Chromium emulado e iPhone 13 Pro |

## Segurança e itens não funcionais

| ID | Cenário | Esperado | Status | Bug | Automação |
|---|---|---|---|---|---|
| CT-54 | Ler os cabeçalhos de `GET /` e embutir a página em iframe de outra origem | Cabeçalhos de proteção presentes; iframe bloqueado | **Falhou** | BUG-22 | `test_pagina_nao_pode_ser_embutida_em_iframe_de_outro_site` |
| CT-55 | Carregar a página com a aba Network aberta | Nenhuma resposta 4xx ou 5xx | **Falhou** | BUG-23 | `test_carregamento_sem_erros_de_rede` |
| CT-56 | `npm audit` das dependências | Nenhuma vulnerabilidade conhecida | **Falhou** | BUG-10 | Manual |
| CT-57 | Ler o código-fonte da página | Sem comentários internos ou ofensivos | **Falhou** | BUG-15 | `test_html_publico_sem_comentario_ofensivo` |
| CT-58 | Abrir `https://storage.googleapis.com/todolist.james.am/` sem login | Listagem negada | **Falhou** | BUG-25 | `test_bucket_de_hospedagem_nao_lista_os_arquivos` |
| CT-59 | Procurar arquivos sensíveis no domínio (`.git/HEAD`, `.git/config`, `package.json`) | 404 | Passou | | Manual |
| CT-60 | Acessar por `http://` | Redireciona para HTTPS | Passou | | Manual (`curl`: 301) |
| CT-61 | Rodar a suíte em Chrome, Firefox e WebKit | Mesmos resultados | Passou | | Suíte completa nos 3 navegadores |
