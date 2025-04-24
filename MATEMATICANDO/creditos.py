from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen


class TelaCreditos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal com ScrollView
        layout = FloatLayout()
        scroll_view = ScrollView(size_hint=(1, 0.8), pos_hint={"center_x": 0.5, "top": 0.9})

        # Layout vertical para organizar os desenvolvedores
        content = BoxLayout(orientation="vertical", size_hint_y=None, spacing=20)
        content.bind(minimum_height=content.setter("height"))

        # Adicionando informações dos desenvolvedores
        devs = [
            {
                "nome": "Desenvolvedor 1",
                "texto": "Possui graduação em licenciatura em matemática, especialização em modelagem matemática e computacional...",
                "imagem": "/mnt/data/image.png",  # Substitua pelo caminho da imagem carregada
            },
            {
                "nome": "Desenvolvedor 2",
                "texto": "Graduado em Licenciatura Matemática pela UNIJUÍ, Mestre em Modelagem Matemática pela mesma instituição...",
                "imagem": "/mnt/data/image.png",  # Substitua pelo caminho da imagem carregada
            },
        ]

        for dev in devs:
            dev_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=200, spacing=10)

            # Adicionando imagem do desenvolvedor
            dev_image = Image(source=dev["imagem"], size_hint=(0.3, 1))
            dev_layout.add_widget(dev_image)

            # Adicionando texto do desenvolvedor
            dev_text = MDLabel(
                text=f"[b]{dev['nome']}[/b]\n{dev['texto']}",
                markup=True,
                halign="left",
                size_hint=(0.7, 1),
                theme_text_color="Primary",
            )
            dev_layout.add_widget(dev_text)

            content.add_widget(dev_layout)

        scroll_view.add_widget(content)
        layout.add_widget(scroll_view)

        # Botão de voltar
        voltar_button = MDRaisedButton(
            text="Voltar",
            size_hint=(0.4, None),
            height=50,
            pos_hint={"center_x": 0.5, "y": 0.05},
            on_release=self.voltar_tela_inicial,
            md_bg_color=(0.3, 0.3, 1, 1),  # Azul claro
            text_color=(1, 1, 1, 1),  # Branco
        )
        layout.add_widget(voltar_button)

        self.add_widget(layout)

    def voltar_tela_inicial(self, instance):
        self.manager.current = "inicial"
