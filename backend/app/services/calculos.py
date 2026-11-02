"""Fórmulas de lucro, margem, markup e preço ideal do My Profit.

Regras (Fase 1, RN01 a RN05):
- Custos em R$ somam direto ao custo total.
- Custos em % (impostos, taxa e comissão) incidem sobre o preço de venda.
- Margem = lucro / preço de venda. Markup = lucro / custo total.
"""
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

CENTAVOS = Decimal("0.01")
CEM = Decimal("100")
ZERO = Decimal("0")
UM = Decimal("1")

REAIS = "R$"
PERCENTUAL = "%"


@dataclass(frozen=True)
class Custo:
    """Um custo que pode ser informado em R$ ou em % do preço de venda."""

    valor: Decimal = ZERO
    tipo: str = REAIS

    def __post_init__(self):
        if self.tipo not in (REAIS, PERCENTUAL):
            raise ValueError('o tipo deve ser "R$" ou "%"')
        if self.valor < 0:
            raise ValueError("o valor não pode ser negativo")


@dataclass(frozen=True)
class Custos:
    custo: Decimal
    frete: Decimal = ZERO
    embalagem: Decimal = ZERO
    imposto: Custo = Custo()
    taxa: Custo = Custo()
    comissao: Custo = Custo()

    def __post_init__(self):
        if self.custo < 0 or self.frete < 0 or self.embalagem < 0:
            raise ValueError("custo, frete e embalagem não podem ser negativos")


@dataclass(frozen=True)
class Resultado:
    preco_venda: Decimal
    custo_total: Decimal
    lucro: Decimal
    margem: Decimal
    markup: Decimal


def _dinheiro(valor: Decimal) -> Decimal:
    return valor.quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def _separar(custos: Custos) -> tuple[Decimal, Decimal]:
    """Devolve (soma dos custos em R$, soma dos custos em % como fração)."""
    fixos = custos.custo + custos.frete + custos.embalagem
    percentual = ZERO
    for item in (custos.imposto, custos.taxa, custos.comissao):
        if item.tipo == PERCENTUAL:
            percentual += item.valor / CEM
        else:
            fixos += item.valor
    return fixos, percentual


def calcular_lucro(custos: Custos, preco_venda: Decimal) -> Resultado:
    if preco_venda <= 0:
        raise ValueError("o preço de venda deve ser maior que zero")
    fixos, percentual = _separar(custos)
    custo_total = fixos + percentual * preco_venda
    if custo_total <= 0:
        raise ValueError("informe ao menos um custo maior que zero")
    lucro = preco_venda - custo_total
    return Resultado(
        preco_venda=_dinheiro(preco_venda),
        custo_total=_dinheiro(custo_total),
        lucro=_dinheiro(lucro),
        margem=_dinheiro(lucro / preco_venda * CEM),
        markup=_dinheiro(lucro / custo_total * CEM),
    )


def calcular_preco_ideal(custos: Custos, meta: Decimal, tipo_meta: str) -> Resultado:
    """Calcula o preço de venda para atingir uma margem ou um markup desejado."""
    tipo_meta = tipo_meta.lower()
    if tipo_meta not in ("margem", "markup"):
        raise ValueError('o tipo da meta deve ser "margem" ou "markup"')
    if meta < 0:
        raise ValueError("a meta não pode ser negativa")
    fixos, percentual = _separar(custos)
    if fixos <= 0:
        raise ValueError("informe ao menos um custo em R$ maior que zero")

    fracao = meta / CEM
    if tipo_meta == "margem":
        divisor = UM - fracao - percentual
        numerador = fixos
    else:
        divisor = UM - percentual * (UM + fracao)
        numerador = fixos * (UM + fracao)
    if divisor <= 0:
        raise ValueError("a meta somada aos custos em % passa de 100%; reduza algum valor")

    preco = _dinheiro(numerador / divisor)
    return calcular_lucro(custos, preco)
