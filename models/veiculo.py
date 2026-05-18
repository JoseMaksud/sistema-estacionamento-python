from datetime import datetime

class Veiculo:
    def __init__(self, placa: str, proprietario: str, tipo_veiculo: str, cor: str):

        """
        Método construtor da classe.

        É executado automaticamente sempre que a classe
        é instanciada, ou seja, quando um novo objeto
        da classe Veiculo é criado.
        """

        self.placa = placa
        self.proprietario = proprietario
        self.tipo_veiculo = tipo_veiculo
        self.cor = cor
        self.hora_entrada: datetime | None = None
        self.hora_saida: datetime | None = None