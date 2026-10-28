"""Bugs conhecidos, descritos em docs/relatorio-de-bugs.md.

Cada teste afetado recebe o marcador do bug e passa a esperar a falha (xfail estrito). Quando o bug for
corrigido, o teste vira XPASS e a suíte falha, avisando que o marcador deve ser removido.
"""
import pytest


def _bug(codigo: str, titulo: str) -> pytest.MarkDecorator:
    return pytest.mark.xfail(strict=True, reason=f"{codigo}: {titulo}")


BUG_01 = _bug("BUG-01", "contador de pendentes mostra 1 a menos (chega a -1)")
BUG_02 = _bug("BUG-02", "Mark all as complete com 1 pendente reabre todas as tarefas")
BUG_03 = _bug("BUG-03", "duas abas abertas: a última gravação apaga tarefas da outra")
BUG_04 = _bug("BUG-04", "localStorage cheio: tarefa não é salva e o campo trava desabilitado")
BUG_05 = _bug("BUG-05", "dado inválido no localStorage deixa a aplicação em branco")
BUG_06 = _bug("BUG-06", "campo de nova tarefa fica com 3 espaços depois de adicionar")
BUG_07 = _bug("BUG-07", "com todas concluídas, Mark all aparece desmarcado e exige 2 cliques")
BUG_08 = _bug("BUG-08", "excluir e editar não funcionam pelo teclado")
BUG_09 = _bug("BUG-09", "sem meta viewport: no celular a página é desenhada com 980 px")
BUG_11 = _bug("BUG-11", "indicador de foco removido (:focus { outline: 0 })")
BUG_12 = _bug("BUG-12", "checkbox de cada tarefa não tem nome acessível")
BUG_13 = _bug("BUG-13", "botão Clear aparece sem nenhuma tarefa concluída")
BUG_14 = _bug("BUG-14", "tooltip do botão excluir mostra TODO:REMOVE THIS EVENTUALLY")
BUG_15 = _bug("BUG-15", "comentário ofensivo no HTML público")
BUG_16 = _bug("BUG-16", "placeholder com erro: What need's to be done?")
BUG_17 = _bug("BUG-17", "instrução do rodapé com erro: toodo")
BUG_18 = _bug("BUG-18", "filtro active em minúsculas")
BUG_19 = _bug("BUG-19", "botão diz Clear em vez de Clear completed")
BUG_20 = _bug("BUG-20", "rota inválida mostra tudo sem filtro destacado")
BUG_22 = _bug("BUG-22", "sem proteção contra clickjacking (X-Frame-Options/CSP)")
BUG_23 = _bug("BUG-23", "404 no console a cada carregamento (/api e /learn.json)")
