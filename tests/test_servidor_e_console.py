"""Itens não funcionais: cabeçalhos de segurança da resposta e erros de rede no carregamento."""
from bugs import BUG_22, BUG_23


@BUG_22
def test_pagina_nao_pode_ser_embutida_em_iframe_de_outro_site(page, base_url):
    cabecalhos = page.request.get(f"{base_url}/").headers

    protegida = "x-frame-options" in cabecalhos or "frame-ancestors" in cabecalhos.get("content-security-policy", "")
    assert protegida, "sem X-Frame-Options nem CSP frame-ancestors: a página aceita clickjacking"


@BUG_23
def test_carregamento_sem_erros_de_rede(page, base_url):
    falhas = []
    page.on("response", lambda r: falhas.append(f"{r.status} {r.url}") if r.status >= 400 else None)

    page.goto(f"{base_url}/#/")
    page.wait_for_load_state("networkidle")

    assert falhas == []
