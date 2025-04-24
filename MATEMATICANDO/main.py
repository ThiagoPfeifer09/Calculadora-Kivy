from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase

# Import das subclasses das telas
from jogar import TelaJogar, Fundamental, Medio, Primario
from Jogos import Jogo
from Calculos import Calculos
from infos import TelaInformacoes
from creditos import TelaCreditos

# Define o tamanho da janela para simular um celular (somente no computador)


LabelBase.register(name="Lemonada", fn_regular="Lemonada-VariableFont_wght.ttf")

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Título com animação
        title = MDLabel(
            text="MATEMATICANDO",
            halign="center",
            font_style="H4",
            size_hint=(0.8, None),
            height=30,
            pos_hint={"center_x": 0.5, "top": 0.9},
            theme_text_color="Custom",
            text_color=(1, 0.8, 0, 1),  # Dourado
        )
        layout.add_widget(title)
        self.animate_title(title)

        # Botão Jogar
        jogar_button = MDRaisedButton(
            text="JOGAR",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            on_release=lambda x: self.ir_para_jogar(),
            md_bg_color=(0, 0.6, 0, 1),  # Verde
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(jogar_button)

        # Botão Informações Gerais
        info_button = MDRaisedButton(
            text="INFORMAÇÕES GERAIS",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=lambda x: self.ir_para_informacoes(),
            md_bg_color=(0, 0, 0.8, 1),  # Azul
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(info_button)

        # Botão Créditos
        creditos_button = MDRaisedButton(
            text="DESENVOLVEDORES",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=lambda x: self.ir_para_creditos(),
            md_bg_color=(0.6, 0, 0.6, 1),  # Roxo
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(creditos_button)

        # Botão Sair
        sair_button = MDRaisedButton(
            text="SAIR",
            size_hint=(0.6, None),
            height=50,
            md_bg_color=(1, 0.3, 0.3, 1),  # Vermelho claro
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            on_release=lambda x: MDApp.get_running_app().stop(),
        )
        layout.add_widget(sair_button)

        self.add_widget(layout)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def animate_title(self, label):
        anim = Animation(opacity=0.7, duration=1) + Animation(opacity=1, duration=1)
        anim.repeat = True
        anim.start(label)

    def ir_para_jogar(self):
        self.manager.current = "jogar"

    def ir_para_informacoes(self):
        self.manager.current = "informacoes"

    def ir_para_creditos(self):
        self.manager.current = "creditos"


class MobileApp(MDApp):
    def build(self):
        # Configura o tema do aplicativo para claro
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"  # Paleta de cores do aplicativo

        sm = ScreenManager()
        sm.add_widget(TelaInicial(name="inicial"))
        sm.add_widget(TelaJogar(name="jogar"))
        sm.add_widget(TelaInformacoes(name="informacoes"))
        sm.add_widget(TelaCreditos(name="creditos"))
        sm.add_widget(Primario(name="primario"))
        sm.add_widget(Fundamental(name="fundamental"))
        sm.add_widget(Medio(name="medio"))
        sm.add_widget(Jogo(name="jogos"))
        sm.add_widget(Calculos(name="soma"))
        return sm


if __name__ == "__main__":
    MobileApp().run()
