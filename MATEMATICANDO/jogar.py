from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen

class TelaJogar(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = MDLabel(
            text="Selecione o seu nível",
            halign="center",
            font_style="H4",
            size_hint=(0.8, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.9},
        )
        layout.add_widget(title)

        # Botão Jogar
        primario_button = MDRaisedButton(
            text="Fundamental I",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            on_release=self.voltar_fundamental_i,
            md_bg_color=(0, 0.6, 0, 1),  # Verde
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(primario_button)

        # Botão Informações Gerais
        fund_button = MDRaisedButton(
            text="Fundamental II",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.voltar_fundamental_ii,
            md_bg_color=(0, 0, 0.8, 1),  # Azul
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(fund_button)

        medio_button = MDRaisedButton(
            text="Ensino Médio",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.voltar_medio,
            md_bg_color=(0.6, 0, 0.6, 1),  # Roxo
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(medio_button)

        # Botão Voltar no final
        voltar_button = MDRaisedButton(
            text="Voltar",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_release=self.voltar_tela_inicial,
            md_bg_color=(0.5, 0.5, 0.5, 1),
            text_color=(1, 1, 1, 1),
        )
        layout.add_widget(voltar_button)

        self.add_widget(layout)

    def voltar_tela_inicial(self, instance):
        self.manager.current = "inicial"

    def voltar_fundamental_i(self, instance):
        self.manager.current = "primario"

    def voltar_fundamental_ii(self, instance):
        self.manager.current = "fundamental"

    def voltar_medio(self, instance):
        self.manager.current = "medio"



class Primario(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = MDLabel(
            text="Fundamental I",
            halign="center",
            font_style="H4",
            size_hint=(0.8, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.9},
        )
        layout.add_widget(title)

        # Botão para ir para a tela de cálculos
        calculos_button = MDRaisedButton(
            text="Cálculos Básicos",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            on_release=self.ir_calculos_fundamental_i,
            md_bg_color=(0, 0.6, 0, 1),  # Verde
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(calculos_button)

        # Botão para ir para a tela de cálculos
        jogo_button = MDRaisedButton(
            text="Jogos",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            on_release=self.ir_jogo,
            md_bg_color=(0, 0, 0.8, 1),  #Azul
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(jogo_button)

        # Botão Voltar
        voltar_button = MDRaisedButton(
            text="Voltar",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_release=self.voltar_tela_inicial,
            md_bg_color=(0.5, 0.5, 0.5, 1),
            text_color=(1, 1, 1, 1),
        )
        layout.add_widget(voltar_button)

        self.add_widget(layout)

    def voltar_tela_inicial(self, instance):
        self.manager.current = "jogar"

    def ir_calculos_fundamental_i(self, instance):
        # Passa a dificuldade para a tela de cálculos (Fundamental I)
        self.manager.current = "soma"
        # Aqui você poderia passar um parâmetro de dificuldade para a tela de cálculos
        self.manager.get_screen("soma").define_dificul("primario")

    def ir_jogo(self, instance):
        self.manager.current = "jogos"

class Fundamental(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = MDLabel(
            text="Fundamental II",
            halign="center",
            font_style="H4",
            size_hint=(0.8, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.9},
        )
        layout.add_widget(title)

        # Botão para ir para a tela de cálculos
        calculos_button = MDRaisedButton(
            text="Cálculos Intermediários",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            on_release=self.ir_calculos_fundamental_ii,
            md_bg_color=(0, 0.6, 0, 1),  # Verde
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(calculos_button)

        # Botão para ir para a tela de cálculos
        jogo_button = MDRaisedButton(
            text="Jogos",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            on_release=self.ir_jogo,
            md_bg_color=(0, 0, 0.8, 1),  # Verde claro
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(jogo_button)

        # Botão Voltar
        voltar_button = MDRaisedButton(
            text="Voltar",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_release=self.voltar_tela_inicial,
            md_bg_color=(0.5, 0.5, 0.5, 1),
            text_color=(1, 1, 1, 1),
        )
        layout.add_widget(voltar_button)

        self.add_widget(layout)

    def voltar_tela_inicial(self, instance):
        self.manager.current = "jogar"

    def ir_calculos_fundamental_ii(self, instance):
        # Passa a dificuldade para a tela de cálculos (Fundamental II)
        self.manager.current = "soma"
        self.manager.get_screen("soma").define_dificul("fundamental")

    def ir_jogo(self, instance):
        self.manager.current = "jogos"

class Medio(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = MDLabel(
            text="Ensino Médio",
            halign="center",
            font_style="H4",
            size_hint=(0.8, None),
            height=50,
            pos_hint={"center_x": 0.5, "top": 0.9},
        )
        layout.add_widget(title)

        # Botão para ir para a tela de cálculos
        calculos_button = MDRaisedButton(
            text="Cálculos Avançados",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            on_release=self.ir_calculos_medio,
            md_bg_color=(0.2, 0.8, 0.2, 1),  # Verde claro
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(calculos_button)

        # Botão para ir para a tela de cálculos
        jogo_button = MDRaisedButton(
            text="Jogos",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            on_release=self.ir_jogo,
            md_bg_color=(0, 0, 0.8, 1),  #Azul
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(jogo_button)

        # Botão Voltar
        voltar_button = MDRaisedButton(
            text="Voltar",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_release=self.voltar_tela_inicial,
            md_bg_color=(0.5, 0.5, 0.5, 1),
            text_color=(1, 1, 1, 1),
        )
        layout.add_widget(voltar_button)

        self.add_widget(layout)

    def voltar_tela_inicial(self, instance):
        self.manager.current = "jogar"

    def ir_calculos_medio(self, instance):
        # Passa a dificuldade para a tela de cálculos (Ensino Médio)
        self.manager.current = "soma"
        self.manager.get_screen("soma").define_dificul("medio")

    def ir_jogo(self, instance):
        self.manager.current = "jogos"

