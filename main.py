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
            border_radius=12,
            padding=20,
            bgcolor=ft.Colors.GREY_900,
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
            width=160,
            max_length=8,
            on_change=formatar_placa,
            capitalization=ft.TextCapitalization.CHARACTERS,
        )

    # ── aba 1: Entrada ────────────────────────────────────────

    f_placa = novo_campo_placa()
    f_nome  = ft.TextField(label="Proprietário", width=210)
    f_cor   = ft.TextField(label="Cor", width=130)
    f_tipo  = ft.Dropdown(
        label="Tipo",
        width=180,
        options=[ft.dropdown.Option(t.value, t.descricao()) for t in TipoVeiculo],
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
            ft.Text("Registrar entrada", size=18, weight="bold"),
            ft.Row([f_placa, f_nome], spacing=10),
            ft.Row([f_cor,   f_tipo], spacing=10),
            ft.Button(
                "Registrar entrada",
                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                on_click=registrar_entrada,
                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
            ),
        ], spacing=14)
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
            ft.Text("Registrar saída", size=18, weight="bold"),
            ft.Row([
                f_saida_placa,
                ft.Button(
                    "Confirmar saída",
                    icon=ft.Icons.LOGOUT,
                    on_click=registrar_saida,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_800, color=ft.Colors.WHITE),
                ),
            ], spacing=10),
            resultado_saida,
        ], spacing=14)
    )

    # ── aba 3: Veículos estacionados ──────────────────────────

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Placa")),
            ft.DataColumn(ft.Text("Proprietário")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Cor")),
            ft.DataColumn(ft.Text("Entrada")),
        ],
        rows=[],
        border=ft.Border.all(1, ft.Colors.GREY_700),
        border_radius=8,
        heading_row_color=ft.Colors.GREY_800,
    )

    txt_rodape = ft.Text("", size=13, color=ft.Colors.GREY_500)

    def atualizar_lista():
        veiculos = estacionamento.listar_veiculos()
        tabela.rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(v.placa, weight="bold")),
                ft.DataCell(ft.Text(v.proprietario)),
                ft.DataCell(ft.Text(TipoVeiculo(v.tipo_veiculo).descricao())),
                ft.DataCell(ft.Text(v.cor or "—")),
                ft.DataCell(ft.Text(v.hora_entrada.strftime("%H:%M"))),
            ])
            for v in veiculos
        ]
        fat = estacionamento.get_faturamento()
        txt_rodape.value = f"{len(veiculos)} veículo(s) no pátio  •  Faturamento: R$ {fat:.2f}"
        page.update()

    aba_lista = card(
        ft.Column([
            ft.Row([
                ft.Text("Veículos estacionados", size=18, weight="bold"),
                ft.IconButton(ft.Icons.REFRESH, on_click=lambda e: atualizar_lista(), tooltip="Atualizar"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            tabela,
            txt_rodape,
        ], spacing=14)
    )

    # ── Navegação ─────────────────────────────────────────────

    abas = [
        ft.Container(aba_entrada, padding=ft.Padding.only(top=12)),
        ft.Container(aba_saida,   padding=ft.Padding.only(top=12)),
        ft.Container(aba_lista,   padding=ft.Padding.only(top=12)),
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

    page.add(ft.Container(conteudo, expand=True, padding=16))

ft.run(main)