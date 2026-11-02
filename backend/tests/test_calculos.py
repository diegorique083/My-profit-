from decimal import Decimal as D

import pytest

from app.services.calculos import Custo, Custos, calcular_lucro, calcular_preco_ideal


def test_caso_do_prototipo_custo_250_preco_300():
    r = calcular_lucro(Custos(custo=D("250")), D("300"))
    assert r.lucro == D("50.00")
    assert r.margem == D("16.67")
    assert r.markup == D("20.00")


def test_taxa_em_percentual_incide_sobre_o_preco_de_venda():
    custos = Custos(custo=D("40"), frete=D("5"), embalagem=D("2"), taxa=Custo(D("10"), "%"))
    r = calcular_lucro(custos, D("100"))
    assert r.custo_total == D("57.00")
    assert r.lucro == D("43.00")
    assert r.margem == D("43.00")
    assert r.markup == D("75.44")


def test_taxa_em_reais_soma_direto_ao_custo():
    custos = Custos(custo=D("40"), frete=D("5"), embalagem=D("2"), taxa=Custo(D("10"), "R$"))
    r = calcular_lucro(custos, D("100"))
    assert r.lucro == D("43.00")


def test_imposto_e_comissao_em_percentual():
    custos = Custos(custo=D("100"), imposto=Custo(D("6"), "%"), comissao=Custo(D("14"), "%"))
    r = calcular_lucro(custos, D("200"))
    assert r.custo_total == D("140.00")
    assert r.lucro == D("60.00")
    assert r.margem == D("30.00")


def test_prejuizo_gera_lucro_e_percentuais_negativos():
    r = calcular_lucro(Custos(custo=D("100")), D("80"))
    assert r.lucro == D("-20.00")
    assert r.margem == D("-25.00")
    assert r.markup == D("-20.00")


def test_preco_ideal_por_margem():
    custos = Custos(custo=D("250"), taxa=Custo(D("10"), "%"))
    r = calcular_preco_ideal(custos, D("20"), "margem")
    assert r.preco_venda == D("357.14")
    assert r.lucro == D("71.43")
    assert r.margem == D("20.00")
    assert r.markup == D("25.00")


def test_preco_ideal_por_markup_coincide_com_a_margem_equivalente():
    custos = Custos(custo=D("250"), taxa=Custo(D("10"), "%"))
    r = calcular_preco_ideal(custos, D("25"), "markup")
    assert r.preco_venda == D("357.14")
    assert r.margem == D("20.00")


def test_preco_ideal_sem_custos_percentuais():
    r = calcular_preco_ideal(Custos(custo=D("250")), D("20"), "margem")
    assert r.preco_venda == D("312.50")
    assert r.lucro == D("62.50")


@pytest.mark.parametrize("preco", [D("0"), D("-10")])
def test_preco_de_venda_deve_ser_positivo(preco):
    with pytest.raises(ValueError):
        calcular_lucro(Custos(custo=D("10")), preco)


def test_sem_nenhum_custo_nao_calcula():
    with pytest.raises(ValueError):
        calcular_lucro(Custos(custo=D("0")), D("100"))


def test_margem_mais_percentuais_acima_de_100_e_recusada():
    custos = Custos(custo=D("100"), taxa=Custo(D("10"), "%"))
    with pytest.raises(ValueError):
        calcular_preco_ideal(custos, D("95"), "margem")


def test_markup_que_zera_o_divisor_e_recusado():
    custos = Custos(custo=D("100"), taxa=Custo(D("50"), "%"))
    with pytest.raises(ValueError):
        calcular_preco_ideal(custos, D("100"), "markup")


def test_tipo_de_meta_invalido():
    with pytest.raises(ValueError):
        calcular_preco_ideal(Custos(custo=D("100")), D("20"), "lucro")


def test_tipo_de_custo_invalido():
    with pytest.raises(ValueError):
        Custo(D("10"), "USD")


def test_valores_negativos_sao_recusados():
    with pytest.raises(ValueError):
        Custos(custo=D("-1"))
    with pytest.raises(ValueError):
        Custo(D("-5"), "%")
