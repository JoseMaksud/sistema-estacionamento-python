import flet as ft
from models.estacionamento import Estacionamento
from models.veiculo import Veiculo
from models.tipo_veiculo import TipoVeiculo

estacionamento = Estacionamento()

def main(page: ft.Page):
    page.title = "Estacionamento"
    page.window.width = 700
    page.window.height = 660
    page.theme_mode = ft.ThemeMode.DARK

    # ── helpers ───────────────────────────────────────────────

    def notificar(msg: str, sucesso: bool = True):
        cor = ft.Colors.GREEN_600 if sucesso else ft.Colors.RED_600
        icone = ft.Icons.CHECK_CIRCLE_OUTLINE if sucesso else ft.Icons.ERROR_OUTLINE
        page.overlay.append(
            ft.SnackBar(
                content=ft.Row([
                    ft.Icon(icone, color=ft.Colors.WHITE, size=20),
                    ft.Text(msg, color=ft.Colors.WHITE),
                ]),
                bgcolor=cor,
                open=True,
            )
        )
        page.update()

    def card(content):
        return ft.Container(
            content=content,
            border_radius=16,
            padding=28,
            # Jeito correto no Flet: passamos a opacidade direto como um parâmetro do Container!
            bgcolor="#da09090b", # Cor GREY_950 (quase preto) com 85% de opacidade em formato Hexadecimal
            # Borda sutil: usamos uma string de cor que já aceita opacidade nativamente
            border=ft.Border.all(1, "white10"), # white10 é o branco com 10% de opacidade
        )

    # ── campo de placa com máscara ────────────────────────────

    def formatar_placa(e):
        raw = e.control.value.upper().replace("-", "")
        if len(raw) <= 3:
            e.control.value = raw
        elif len(raw) <= 7:
            e.control.value = raw[:3] + "-" + raw[3:]
        else:
            e.control.value = raw[:3] + "-" + raw[3:7]
        e.control.update()

    def novo_campo_placa():
        return ft.TextField(
            label="Placa",
            hint_text="AAA-0000",
            width=245, # <- Mude de 160 para 245
            max_length=8,
            on_change=formatar_placa,
            capitalization=ft.TextCapitalization.CHARACTERS,
            border_color="white30",
            label_style=ft.TextStyle(color="white70"),
            bgcolor="#cc1c1c1e",
        )

    # ── aba 1: Entrada ────────────────────────────────────────

    f_placa = novo_campo_placa()
    f_nome  = ft.TextField(
        label="Proprietário", 
        width=245, # <- Mude de 330 para 245
        border_color="white30",  
        label_style=ft.TextStyle(color="white70"),
        bgcolor="#cc1c1c1e",
    )
    f_cor   = ft.TextField(
        label="Cor", 
        width=240, 
        border_color="white30",
        label_style=ft.TextStyle(color="white70"),
        bgcolor="#cc1c1c1e",
    )
    f_tipo  = ft.Dropdown(
        label="Tipo",
        width=250,               # Somado com a cor (240) também dá 490! Tudo alinhado.
        border_color="white30",
        label_style=ft.TextStyle(color="white70"),
        options=[ft.dropdown.Option(t.value, t.descricao()) for t in TipoVeiculo],

        filled=True,
        fill_color="#cc1c1c1e",
    )

    def registrar_entrada(e):
        placa = f_placa.value.strip()
        if len(placa) < 8:
            notificar("Placa inválida! Use o formato AAA-0000.", sucesso=False)
            return
        if not f_nome.value.strip():
            notificar("Informe o nome do proprietário.", sucesso=False)
            return
        if not f_tipo.value:
            notificar("Selecione o tipo do veículo.", sucesso=False)
            return
        if estacionamento.buscar_veiculo(placa):
            notificar(f"Placa {placa} já está no pátio!", sucesso=False)
            return

        veiculo = Veiculo(placa, f_nome.value.strip(), f_tipo.value, f_cor.value.strip())
        estacionamento.registrar_entrada(veiculo)

        f_placa.value = ""
        f_nome.value  = ""
        f_cor.value   = ""
        f_tipo.value  = None

        atualizar_lista()
        notificar(f"Veículo {placa} registrado com sucesso!")

    aba_entrada = card(
        ft.Column([
            ft.Text("Registrar entrada", size=22, weight="bold", color=ft.Colors.WHITE),
            ft.Row([f_placa, f_nome], spacing=10, vertical_alignment="start", alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([f_cor,   f_tipo], spacing=10, vertical_alignment="start", alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=15), # Espaço elegante antes do botão
            ft.Row([
                ft.ElevatedButton(
                    "Registrar entrada",
                    icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                    on_click=registrar_entrada,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_600, 
                        color=ft.Colors.WHITE,
                        padding=22, 
                        shape=ft.RoundedRectangleBorder(radius=8), 
                    ),
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], 
        spacing=18,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER # <- ESSA LINHA CENTRALIZA O TÍTULO E OS GRUPOS
        )
    )

    # ── aba 2: Saída ──────────────────────────────────────────

    f_saida_placa   = novo_campo_placa()
    resultado_saida = ft.Column()

    def registrar_saida(e):
        placa = f_saida_placa.value.strip()
        if not placa:
            notificar("Informe a placa!", sucesso=False)
            return

        registro = estacionamento.registrar_saida(placa)
        if registro is None:
            notificar(f"Placa '{placa}' não encontrada no pátio!", sucesso=False)
            return

        resultado_saida.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Text("Comprovante de saída", size=15, weight="bold"),
                    ft.Divider(height=1),
                    ft.Row([ft.Text("Placa:",        color=ft.Colors.GREY_400), ft.Text(registro["placa"],       weight="bold")]),
                    ft.Row([ft.Text("Proprietário:", color=ft.Colors.GREY_400), ft.Text(registro["proprietario"])]),
                    ft.Row([ft.Text("Tipo:",         color=ft.Colors.GREY_400), ft.Text(registro["tipo"])]),
                    ft.Row([ft.Text("Cor:",          color=ft.Colors.GREY_400), ft.Text(registro["cor"] or "—")]),
                    ft.Row([ft.Text("Entrada:",      color=ft.Colors.GREY_400), ft.Text(registro["hora_entrada"].strftime("%d/%m/%Y %H:%M"))]),
                    ft.Row([ft.Text("Saída:",        color=ft.Colors.GREY_400), ft.Text(registro["hora_saida"].strftime("%d/%m/%Y %H:%M"))]),
                    ft.Divider(height=1),
                    ft.Row([
                        ft.Text("Total:", size=15, weight="bold"),
                        ft.Text(f"R$ {registro['valor']:.2f}", size=20, weight="bold", color=ft.Colors.GREEN_400),
                    ]),
                ], spacing=7),
                bgcolor=ft.Colors.GREEN_900,
                border_radius=10,
                padding=16,
                border=ft.Border.all(1, ft.Colors.GREEN_700),
            )
        ]
        f_saida_placa.value = ""
        atualizar_lista()
        notificar(f"Saída de {registro['placa']}! Total: R$ {registro['valor']:.2f}")

    aba_saida = card(
        ft.Column([
            # Título da página
            ft.Text("Registrar saída", size=22, weight="bold", color=ft.Colors.WHITE),
            
            ft.Container(height=5), # Espaçamento elegante antes dos campos
            
            # Campo e Botão alinhados perfeitamente pelo TOPO (ignorando o 0/8 embaixo)
            ft.Row([
                f_saida_placa,
                ft.ElevatedButton(
                    "Confirmar saída",
                    icon=ft.Icons.LOGOUT, # Ícone combinando com saída
                    on_click=registrar_saida,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.ORANGE_700, # Mantendo o seu tom laranja de destaque
                        color=ft.Colors.WHITE,
                        padding=22, # Botão robusto igual ao da entrada
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                )
            ], 
            alignment=ft.MainAxisAlignment.CENTER,      # Centraliza horizontalmente
            
            # ── ALTERADO AQUI: Mudamos de CENTER para "start" ──
            vertical_alignment="start",                 # Alinha pelo topo (ignora o espaço do 0/8)
            # ──────────────────────────────────────────────────
            
            spacing=15                                   # Dá um espaço entre a placa e o botão
            ),
            
            ft.Container(height=10), # Espaço elegante antes do comprovante aparecer
            
            resultado_saida,
        ], 
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER # Mantém o bloco todo no eixo central
        )
    )

    # ── aba 3: Veículos estacionados ──────────────────────────

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Placa", weight="bold")),
            ft.DataColumn(ft.Text("Proprietário", weight="bold")),
            ft.DataColumn(ft.Text("Tipo", weight="bold")),
            ft.DataColumn(ft.Text("Cor", weight="bold")),
            ft.DataColumn(ft.Text("Entrada", weight="bold")),
        ],
        rows=[],
        border=ft.Border.all(1, "white10"), # Borda sutil combinando com o painel
        border_radius=8,
        heading_row_color="#cc1c1c1e",
        data_row_color="#cc242426",
    )

    txt_rodape = ft.Text("", size=13, color=ft.Colors.GREY_400, weight="w500")

    def atualizar_lista():
        veiculos = estacionamento.listar_veiculos()
        tabela.rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(v.placa, weight="bold", color=ft.Colors.BLUE_400)), # Destaca a placa com cor
                ft.DataCell(ft.Text(v.proprietario, color=ft.Colors.WHITE70)),
                ft.DataCell(ft.Text(TipoVeiculo(v.tipo_veiculo).descricao(), color=ft.Colors.WHITE70)),
                ft.DataCell(ft.Text(v.cor or "—", color=ft.Colors.WHITE70)),
                ft.DataCell(ft.Text(v.hora_entrada.strftime("%H:%M"), color=ft.Colors.WHITE70)),
            ])
            for v in veiculos
        ]
        fat = estacionamento.get_faturamento()
        txt_rodape.value = f" 📊 {len(veiculos)} veículo(s) no pátio   •   💰 Faturamento: R$ {fat:.2f}"
        page.update()

    aba_veiculos = card(
        ft.Column([
            # Cabeçalho com o título e botão REFRESH moderno alineados nas pontas
            ft.Row([
                ft.Text("Veículos estacionados", size=22, weight="bold", color=ft.Colors.WHITE),
                ft.IconButton(
                    ft.Icons.REFRESH, 
                    icon_color=ft.Colors.WHITE70,
                    on_click=lambda e: atualizar_lista(), 
                    tooltip="Atualizar lista"
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Divider(color="white10", height=1), # Linha divisória fina e elegante
            
            # Colocamos a tabela dentro de uma linha com Scroll para evitar que ela corte na tela
            ft.Row([tabela], scroll=ft.ScrollMode.AUTO, expand=True),
            
            ft.Container(height=5), # Pequeno respiro antes do rodapé
            
            # Rodapé estilizado
            txt_rodape,
        ], spacing=15, expand=True)
    )

    # ── Navegação ─────────────────────────────────────────────

    abas = [
        ft.Container(aba_entrada, padding=ft.Padding.only(top=12)),
        ft.Container(aba_saida,   padding=ft.Padding.only(top=12)),
        ft.Container(aba_veiculos,   padding=ft.Padding.only(top=12)),
    ]
    conteudo = ft.Container(content=abas[0], expand=True)

    def on_nav(e):
        conteudo.content = abas[e.control.selected_index]
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.ADD_CIRCLE_OUTLINE, label="Entrada"),
            ft.NavigationBarDestination(icon=ft.Icons.LOGOUT,             label="Saída"),
            ft.NavigationBarDestination(icon=ft.Icons.LIST,               label="Veículos"),
        ],
        selected_index=0,
        on_change=on_nav,
    )

    # page.add(ft.Container(conteudo, expand=True, padding=16))

    page.add(
        ft.Container(
            content=conteudo,
            expand=True,
            padding=16,
            
            # Formato correto para as versões novas do Flet:
            image=ft.DecorationImage(
                src="fundo.jpg", # Ou o link da internet
                fit="cover",
            )
        )
    )

# ft.run(main)

ft.run(main, assets_dir="assets")
