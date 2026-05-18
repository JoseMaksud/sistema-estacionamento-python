from enum import  Enum

class TipoVeiculo(Enum):
    Moto = "0"
    Carro = "1"
    CarroGrande = "2"

    """
    Enum (Enumeração) é um tipo especial em Python
    usado para representar um conjunto fixo de valores.

    Ele serve para dar nomes mais claros e organizados
    para valores que não mudam, como tipos, categorias ou opções.
    """

    def descricao(self):
        descricoes = {
            "0": "Moto",
            "1": "Carro",
            "2": "CarroGrande / Van",
        }
        return descricoes[self.value]

    def tarifa_base(self):
        tarifas = {
            "0": 5,
            "1": 10,
            "2": 15,
        }
        return tarifas[self.value]

    def tarifa_hora(self):
        tarifas = {
            "0": 5,
            "1": 6,
            "2": 7,
        }
        return tarifas[self.value]