# sistema-estacionamento-python 🚗🅿️

> **PROJETO EM GRUPO** – Aplicação Prática de Algoritmos em Python (P2) - UNISAGRADO
> 
> **Integrantes do Grupo:**
> * Felipe Daltoé
> * Guilherme Alexandre Clementino
> * José Francisco Dos Santos Neto
> * Nicolas Galli Coradazzi

---

Este projeto tem como objetivo a criação de um software interativo para o gerenciamento de fluxo (entradas, saídas e faturamento) de um estacionamento comercial, resolvendo um problema prático do mundo real.

## 🛠️ Tecnologias Utilizadas
- **Python** (Lógica de programação e tratamento de dados)
- **Flet** (Framework de interface gráfica)

## 📋 Conceitos de Algoritmos Aplicados
Para atender aos critérios exigidos na avaliação, o sistema implementa:
- **Comandos de Entrada e Saída**: Captura dinâmica de dados via inputs da interface com formatação de máscara de placa em tempo real e saída estruturada de dados através de recibos e tabelas de consulta.
- **Estruturas de Decisão**: Múltiplas validações de consistência lógica na entrada e saída de veículos, impedindo duplicidade de placas no pátio e formatos inválidos.
- **Estruturas de Repetição**: Uso de laços iterativos (`for`) para varredura e renderização dinâmica dos elementos na tabela de veículos estacionados.
- **Vetores e Objetos**: Armazenamento indexado em listas para gerenciar a persistência em memória dos registros operacionais de forma eficiente.

## 🚀 Como Executar o Projeto

1. Certifique-se de ter o Python instalado na sua máquina.
2. Instale as dependências necessárias executando o comando abaixo no terminal:
   ```bash
   pip install flet
3. Garanta que a árvore de diretórios esteja organizada com a pasta models/ contendo os arquivos de regras de negócio (estacionamento.py, veiculo.py, tipo_veiculo.py).

4. Execute o arquivo principal para abrir a interface gráfica:
   ```bash
   python main.py
