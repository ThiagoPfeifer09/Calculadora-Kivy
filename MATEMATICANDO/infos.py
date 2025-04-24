from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen


class TelaInformacoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()


        scroll_view = ScrollView(
            size_hint=(0.9, 0.6), pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        text_label = MDLabel(
            text=(
                "Para jogar, você deve ir para a tela inicial, clicar em jogar e escolher o seu nível. "
                "O nível está separado pelos níveis do colégio. Após, escolha se deseja operações básicas ou jogos e se divirta!"
                "Operações básicas incluem soma, subtração, multiplicação e divisão, com questões adaptadas ao nível de dificuldade escolhido. "
                "Os jogos são atividades interativas projetadas para testar suas habilidades de uma maneira divertida e desafiadora."
                "No nível Fundamental I, você encontrará desafios simples para consolidar as operações básicas. "
                "No nível Fundamental II, as questões tornam-se um pouco mais complexas, com maior foco em raciocínio lógico. "
                "No Ensino Médio, os desafios envolvem conceitos mais avançados, como álgebra e geometria básica."
                "Se precisar de ajuda durante o jogo, volte para esta tela para reler as instruções. Divirta-se jogando e aprendendo!"
            ),
            halign="center",
            font_style="Body1",
            theme_text_color="Primary",
            size_hint_y=None,
            height=500,  # Altura maior para ativar o ScrollView
        )
        scroll_view.add_widget(text_label)
        layout.add_widget(scroll_view)

        # Botão de voltar
        voltar_button = MDRaisedButton(
            text="Voltar",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            on_release=self.voltar_tela_inicial,
            md_bg_color=(0, 0.5, 0.5, 1),  # Verde-azulado
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(voltar_button)

        self.add_widget(layout)

    def voltar_tela_inicial(self, instance):
        self.manager.current = "inicial"
