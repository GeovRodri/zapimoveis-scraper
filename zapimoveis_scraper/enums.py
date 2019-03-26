from enum import Enum


class ZapAcao(Enum):
    venda = 'venda'
    aluguel = 'aluguel'
    lancamentos = 'lancamentos'


class ZapTipo(Enum):
    todos = 'imoveis'
    apartamentos = 'apartamentos'
    casas = 'casas'
