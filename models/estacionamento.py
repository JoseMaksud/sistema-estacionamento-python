import math
from datetime import datetime

from models.veiculo import Veiculo
from models.tipo_veiculo import TipoVeiculo

class Estacionamento:

    """
    self representa o próprio objeto criado a partir da classe.

    É através do self que conseguimos acessar
    e armazenar informações do objeto,
    como atributos e métodos.
    """

    def __init__(self):
        """
        __init__ é o método construtor da classe.

        Ele é executado automaticamente sempre que um novo
        objeto da classe é criado (instanciado).

        Serve para inicializar os atributos do objeto.
        basicamente: “o que o objeto já começa tendo quando é criado”
        """
        self.veiculos: list[Veiculo] = []
        self.historico: list[dict] = []
        self.faturamento: float  = 0

    def registrar_entrada(self, veiculo: Veiculo) -> None:
        veiculo.hora_entrada = datetime.now()
        self.veiculos.append(veiculo)

    def buscar_veiculo(self, placa: str) -> Veiculo | None:
        for v in self.veiculos:
            if v.placa.upper() == placa.upper():
                return v
        return None

    def registrar_saida(self, placa:str) -> Veiculo | None:
        veiculo = self.buscar_veiculo(placa)
        if veiculo is None:
            return None

        veiculo.hora_saida = datetime.now()
        diferenca = veiculo.hora_saida - veiculo.hora_entrada
        horas = math.floor(diferenca.seconds / 3600)

        tipo = TipoVeiculo(veiculo.tipo_veiculo)
        valor = tipo.tarifa_base() + (tipo.tarifa_hora() * horas)

        self.faturamento += valor
        self.veiculos.remove(veiculo)

        registro = {
            "placa": veiculo.placa,
            "proprietario": veiculo.proprietario,
            "tipo": tipo.descricao(),
            "cor": veiculo.cor,
            "hora_entrada": veiculo.hora_entrada,
            "hora_saida": veiculo.hora_saida,
            "valor": valor,
        }
        self.historico.append(registro)
        return registro

    def listar_veiculos(self) -> list[Veiculo]:
        return self.veiculos

    def get_faturamento(self) -> float:
        return self.faturamento