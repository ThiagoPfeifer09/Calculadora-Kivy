import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import numpy as np
import matplotlib.pyplot as plt
from kivy.utils import get_color_from_hex
from kivy_garden.matplotlib import FigureCanvasKivyAgg
import math
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
import re
from kivy.clock import Clock
from kivy.uix.scatter import Scatter


class Calculadora(App):
    def build(self):
        self.mode = "Padrão"
        self.main_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.text_input = TextInput(
            text="",
            font_size=80,
            halign="right",
            size_hint=(1, 0.2),
            multiline=False,
            readonly=True,
            font_name="DejaVuSans.ttf",
            background_color=get_color_from_hex("#333333"),
            foreground_color=get_color_from_hex("#FFFFFF"),
        )
        self.main_layout.add_widget(self.text_input)

        self.spinner = Spinner(
            text="Padrão",
            values=["Padrão", "Científica", "Conversão", "Gráfica"],
            size_hint=(1, 0.1),
            background_color=get_color_from_hex("#444444"),
            color=get_color_from_hex("#FFFFFF"),
        )
        self.spinner.bind(text=self.seleciona_modo)
        self.main_layout.add_widget(self.spinner)

        self.buttons_layout = BoxLayout(size_hint=(1, 0.7))
        self.main_layout.add_widget(self.buttons_layout)

        self.atualiza_botoes()
        return self.main_layout

    def seleciona_modo(self, spinner, text):
        if text == "Gráfica":
            self.troca_spinner_grafico()
        else:
            self.mode = text
            self.atualiza_botoes()
            self.restaura_text_input()

    def troca_spinner_grafico(self):
        self.main_layout.remove_widget(self.spinner)
        self.oculta_text_input()

        self.spinner_grafica = Spinner(
            text="Selecione",
            values=["Voltar", "Polinômios", "Trigonométricas"],
            size_hint=(1, 0.1),
            background_color=get_color_from_hex("#444444"),
            color=get_color_from_hex("#FFFFFF"),
        )
        self.spinner_grafica.bind(text=self.seleciona_modo_grafico)
        self.main_layout.add_widget(self.spinner_grafica, index=1)

        self.spinner_grafica.trigger_action(duration=0.1)

    def seleciona_modo_grafico(self, spinner, text):
        if text == "Voltar":
            self.main_layout.remove_widget(self.spinner_grafica)
            self.spinner = Spinner(
                text="Gráfica",
                values=["Padrão", "Científica", "Conversão", "Gráfica"],
                size_hint=(1, 0.1),
                background_color=get_color_from_hex("#444444"),
                color=get_color_from_hex("#FFFFFF"),
            )
            self.spinner.bind(text=self.seleciona_modo)
            self.main_layout.add_widget(self.spinner, index=1)
            self.restaura_text_input()

        elif text == "Polinômios":
            self.botoes_grafica()
            self.spinner_grafica.text = "Polinômios"

        elif text == "Trigonométricas":
            self.remove_grafico()
            self.botoes_trigonometrica()
            self.spinner_grafica.text = "Trigonométricas"

    def oculta_text_input(self):
        if self.text_input in self.main_layout.children:
            self.main_layout.remove_widget(self.text_input)

    def restaura_text_input(self):
        if self.text_input not in self.main_layout.children:
            self.main_layout.add_widget(self.text_input, index=len(self.main_layout.children))

    def atualiza_botoes(self):
        self.remove_grafico()
        self.buttons_layout.clear_widgets()
        if self.mode == "Padrão":
            self.botoes_padrao()
        elif self.mode == "Científica":
            self.botoes_cientifica()
        elif self.mode == "Conversão":
            self.botoes_conversao()

    def botoes_padrao(self):
        layout = GridLayout(cols=4, spacing=10)
        buttons = [
            {"text": "%", "color": "#FFAA00"},
            {"text": "CE", "color": "#888888"},
            {"text": "C", "color": "#888888"},
            {"text": "⌫", "color": "#888888"},
            {"text": "1/x", "color": "#CCCC00"},
            {"text": "x²", "color": "#CCCC00"},
            {"text": "√", "color": "#CCCC00"},
            {"text": "÷", "color": "#CCCC00"},
            {"text": "7", "color": "#0077FF"},
            {"text": "8", "color": "#0077FF"},
            {"text": "9", "color": "#0077FF"},
            {"text": "x", "color": "#CCCC00"},
            {"text": "4", "color": "#0077FF"},
            {"text": "5", "color": "#0077FF"},
            {"text": "6", "color": "#0077FF"},
            {"text": "-", "color": "#CCCC00"},
            {"text": "1", "color": "#0077FF"},
            {"text": "2", "color": "#0077FF"},
            {"text": "3", "color": "#0077FF"},
            {"text": "+", "color": "#CCCC00"},
            {"text": "+/-", "color": "#CCCC00"},
            {"text": "0", "color": "#0077FF"},
            {"text": ".", "color": "#CCCC00"},
            {"text": "=", "color": "#FF5500"},
        ]

        for button in buttons:
            layout.add_widget(
                Button(
                    text=button["text"],
                    font_size=60,
                    font_name="DejaVuSans.ttf",
                    background_color=get_color_from_hex(button["color"]),
                    on_press=self.botao_pressionado,
                )
            )
        self.buttons_layout.add_widget(layout)

    def botoes_cientifica(self):
        layout = GridLayout(cols=5, spacing=10)
        buttons = [
            {"text": "sin", "color": "#888888"},
            {"text": "cos", "color": "#888888"},
            {"text": "tan", "color": "#888888"},
            {"text": "C", "color": "#888888"},
            {"text": "⌫", "color": "#888888"},
            {"text": "|x|", "color": "#CCCC00"},
            {"text": "√", "color": "#CCCC00"},
            {"text": "e", "color": "#CCCC00"},
            {"text": "π", "color": "#CCCC00"},
            {"text": "x²", "color": "#CCCC00"},
            {"text": "1/x", "color": "#CCCC00"},
            {"text": "(", "color": "#888888"},
            {"text": ")", "color": "#888888"},
            {"text": "n!", "color": "#888888"},
            {"text": "÷", "color": "#CCCC00"},
            {"text": "%", "color": "#CCCC00"},
            {"text": "7", "color": "#0077FF"},
            {"text": "8", "color": "#0077FF"},
            {"text": "9", "color": "#0077FF"},
            {"text": "x", "color": "#CCCC00"},
            {"text": "10ˣ", "color": "#CCCC00"},
            {"text": "4", "color": "#0077FF"},
            {"text": "5", "color": "#0077FF"},
            {"text": "6", "color": "#0077FF"},
            {"text": "-", "color": "#CCCC00"},
            {"text": "log", "color": "#CCCC00"},
            {"text": "1", "color": "#0077FF"},
            {"text": "2", "color": "#0077FF"},
            {"text": "3", "color": "#0077FF"},
            {"text": "+", "color": "#CCCC00"},
            {"text": "ln", "color": "#CCCC00"},
            {"text": "+/-", "color": "#CCCC00"},
            {"text": "0", "color": "#0077FF"},
            {"text": ".", "color": "#CCCC00"},
            {"text": "=", "color": "#FF5500"},
        ]

        for button in buttons:
            layout.add_widget(
                Button(
                    text=button["text"],
                    font_size=60,
                    font_name="DejaVuSans.ttf",
                    background_color=get_color_from_hex(button["color"]),
                    on_press=self.botao_pressionado,
                )
            )
        self.buttons_layout.add_widget(layout)

    def formatar_numero(self, numero):
        if isinstance(numero, float):
            numero_formatado = f"{numero:.5f}".rstrip("0").rstrip(".")
            return numero_formatado
        return str(numero)

    def botao_pressionado(self, instance):
        text = instance.text
        max_length = 15  # Número máximo de caracteres a serem exibidos
        try:
            if text == "C" or text == "CE":
                self.text_input.text = ""
            elif text == "⌫":
                self.text_input.text = self.text_input.text[:-1]
            elif text == "=":
                self.resultado_calculo()
            elif text == "%":
                self.text_input.text = self.formatar_numero(float(self.text_input.text) / 100)
            elif text == "10ˣ":
                value = float(self.text_input.text) if self.text_input.text else 0
                self.text_input.text = self.formatar_numero(10 ** value)
            elif text in ["sin", "cos", "tan", "√", "log", "ln", "1/x", "x²", "n!", "|x|"]:
                self.aplica_funcao(text)
            elif text in ["π", "e"]:
                self.text_input.text += self.formatar_numero(math.pi if text == "π" else math.e)
            elif text == "÷":
                self.text_input.text += "/"
            elif text == "x":
                self.text_input.text += "*"
            elif text == "+/-":
                if self.text_input.text:
                    if self.text_input.text.startswith("-"):
                        self.text_input.text = self.text_input.text[1:]  # Remove o sinal de negativo
                    else:
                        self.text_input.text = f"-{self.text_input.text}"  # Adiciona o sinal de negativo
            else:
                self.text_input.text += text

            # Limita a exibição ao início do texto, se exceder o máximo
            if len(self.text_input.text) > max_length:
                self.text_input.text = self.text_input.text[:max_length]
        except Exception as e:
            print(f"Erro ao processar botão: {e}")
            self.text_input.text = "Erro"

    def aplica_funcao(self, func):
        try:
            value = float(self.text_input.text)
            if func == "sin":
                resultado = math.sin(math.radians(value))
            elif func == "cos":
                resultado = math.cos(math.radians(value))
            elif func == "tan":
                resultado = math.tan(math.radians(value))
            elif func == "√":
                resultado = math.sqrt(value)
            elif func == "log":
                resultado = math.log10(value)
            elif func == "ln":
                resultado = math.log(value)
            elif func == "1/x":
                resultado = 1 / value if value != 0 else "Error"
            elif func == "x²":
                resultado = value ** 2
            elif func == "n!":
                resultado = math.factorial(int(value)) if value >= 0 and value.is_integer() else "Error"
            elif func == "|x|":
                resultado = abs(value)
            elif func == "10ˣ":
                resultado = 10 ** value

            self.text_input.text = self.formatar_numero(resultado) if resultado != "Error" else "Error"

        except ValueError:
            self.text_input.text = "Error"

    def resultado_calculo(self):
        try:
            expressao = self.text_input.text
            resultado = eval(expressao)
            self.text_input.text = self.formatar_numero(resultado)
        except Exception as e:
            print(f"Erro ao calcular expressão: {e}")
            self.text_input.text = "Erro"

    def botoes_conversao(self):
        layout = FloatLayout()

        # Entrada de valor
        self.value_input = TextInput(
            font_size=70,
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.3, 'y': 0.9}
        )

        # Spinner para unidade de origem
        self.spinner_from = Spinner(
            text="Quilômetros",
            values=["Quilômetros", "Metros", "Milímetros", "Centímetros"],
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.1, 'y': 0.7}  # Ajustado para melhor alinhamento
        )

        # Spinner para unidade de destino
        self.spinner_to = Spinner(
            text="Metros",
            values=["Quilômetros", "Metros", "Milímetros", "Centímetros"],
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.5, 'y': 0.7}  # Ajustado para melhor alinhamento
        )

        # Rótulo "De:" acima do spinner_from
        self.de_label = Label(
            text="De:",
            font_size=50,
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.1, 'y': 0.8}  # Ajustado para ficar acima do spinner
        )

        # Rótulo "Para:" acima do spinner_to
        self.para_label = Label(
            text="Para:",
            font_size=50,
            size_hint=(0.4, 0.1),
            pos_hint={'x': 0.5, 'y': 0.8}  # Ajustado para ficar acima do spinner
        )

        # Botão de conversão
        self.convert_button = Button(
            text="Converter",
            size_hint=(0.9, 0.1),
            pos_hint={'x': 0.05, 'y': 0.55},
            on_press=self.converte_valor
        )

        # Rótulo para mostrar o resultado
        self.result_label = Label(
            text="Resultado:",
            font_size=70,
            size_hint=(0.9, 0.1),
            pos_hint={'x': 0.05, 'y': 0.4}
        )

        # Adicionando widgets ao FloatLayout
        layout.add_widget(self.value_input)
        layout.add_widget(self.spinner_from)
        layout.add_widget(self.spinner_to)
        layout.add_widget(self.convert_button)
        layout.add_widget(self.result_label)
        layout.add_widget(self.para_label)
        layout.add_widget(self.de_label)
        self.buttons_layout.add_widget(layout)

    def converte_valor(self, instance):
        try:
            value = float(self.value_input.text)
            unit_from = self.spinner_from.text
            unit_to = self.spinner_to.text

            # Conversão de unidades
            if unit_from == "Quilômetros":
                if unit_to == "Metros":
                    result = value * 1000
                elif unit_to == "Milímetros":
                    result = value * 1_000_000
                elif unit_to == "Centímetros":
                    result = value * 100_000
                else:
                    result = value
            elif unit_from == "Metros":
                if unit_to == "Quilômetros":
                    result = value / 1000
                elif unit_to == "Milímetros":
                    result = value * 1000
                elif unit_to == "Centímetros":
                    result = value * 100
                else:
                    result = value
            elif unit_from == "Milímetros":
                if unit_to == "Quilômetros":
                    result = value / 1_000_000
                elif unit_to == "Metros":
                    result = value / 1000
                elif unit_to == "Centímetros":
                    result = value / 10
                else:
                    result = value
            elif unit_from == "Centímetros":
                if unit_to == "Quilômetros":
                    result = value / 100_000
                elif unit_to == "Metros":
                    result = value / 100
                elif unit_to == "Milímetros":
                    result = value * 10
                else:
                    result = value

            self.result_label.text = f"Resultado: {result}"
        except ValueError:
            self.result_label.text = "Erro na conversão!"


    def botoes_grafica(self):
        layout = FloatLayout(size_hint=(1, 0.8))

        # Criação dos campos de entrada e labels para A, B e C
        self.a_input = TextInput(
            text="1", multiline=False, font_size=45, size_hint=(0.3, 0.15), height=50, pos_hint={"x": 0.08, "y": 0.85})
        self.b_input = TextInput(
            text="0", multiline=False, font_size=45, size_hint=(0.3, 0.15), height=50, pos_hint={"x": 0.08, "y": 0.65})
        self.c_input = TextInput(
            text="0", multiline=False, font_size=45, size_hint=(0.3, 0.15), height=50, pos_hint={"x": 0.08, "y": 0.45})

        # Labels para os coeficientes
        a_label = Label(text="a:", font_size=40, size_hint=(0.1, None), height=50, pos_hint={"x": 0.009, "y": 0.9})
        b_label = Label(text="b:", font_size=40, size_hint=(0.1, None), height=50, pos_hint={"x": 0.009, "y": 0.7})
        c_label = Label(text="c:", font_size=40, size_hint=(0.1, None), height=50, pos_hint={"x": 0.008, "y": 0.5})

        # Sliders
        self.a_slider = Slider(min=-10, max=10, value=1, size_hint=(0.5, None), step=1, height=50, pos_hint={"x": 0.43, "y": 0.9})
        self.b_slider = Slider(min=-10, max=10, value=0, size_hint=(0.5, None), step=1,height=50, pos_hint={"x": 0.43, "y": 0.7})
        self.c_slider = Slider(min=-10, max=10, value=0, size_hint=(0.5, None), step=1,height=50, pos_hint={"x": 0.43, "y": 0.5})

        # Atualização dos campos de texto com sliders
        self.a_slider.bind(value=self.atualiza_a)
        self.b_slider.bind(value=self.atualiza_b)
        self.c_slider.bind(value=self.atualiza_c)

        layout.add_widget(a_label)
        layout.add_widget(self.a_input)
        layout.add_widget(self.a_slider)

        layout.add_widget(b_label)
        layout.add_widget(self.b_input)
        layout.add_widget(self.b_slider)

        layout.add_widget(c_label)
        layout.add_widget(self.c_input)
        layout.add_widget(self.c_slider)

        # Botão de Atualizar
        plot_button = Button(
            text="Atualizar",
            font_size=50,
            size_hint=(0.3, 0.15),
            height=45,
            pos_hint={"x": 0.35, "y": 0.2},
            on_press=self.gera_grafico,
        )
        layout.add_widget(plot_button)

        # Botão de Limpar (Menor, Vermelho, Mesma Altura que "Atualizar")
        limpar_button = Button(
            text="Limpar",
            font_size=35,  # Fonte menor
            size_hint=(0.2, 0.1),  # Menor tamanho
            height=40,
            pos_hint={"x": 0.7, "y": 0.2},  # Mesma altura do botão "Atualizar"
            background_color=(1, 0, 0, 1),  # Vermelho
            on_press=self.limpar_grafico,
        )
        layout.add_widget(limpar_button)

        self.buttons_layout.clear_widgets()
        self.buttons_layout.add_widget(layout)

        # Plotar gráfico inicial
        self.gera_grafico(None)


    def limpar_grafico(self, *args):
        """ Reseta os sliders B e C para 0 e A para 1, mantém os valores nas entradas e atualiza o gráfico """
        self.a_slider.value = 1
        self.b_slider.value = 0
        self.c_slider.value = 0

        # Mantém os valores nas TextInput
        self.a_input.text = "1"
        self.b_input.text = "0"
        self.c_input.text = "0"

        # Atualiza o gráfico
        self.gera_grafico(None)


    def gera_grafico(self, instance):
        try:
            a = int(float(self.a_input.text))
            b = int(float(self.b_input.text))
            c = int(float(self.c_input.text))

            x_vals = np.linspace(-10, 10, 400)
            y_vals = a * x_vals**2 + b * x_vals + c

            fig, ax = plt.subplots(figsize=(6, 4))  # Tamanho menor para não extrapolar o layout
            ax.set_title(f"f(x) = {a}x² + {b}x + {c}", fontsize=20)
            ax.set_xlabel("Eixo X", fontsize=16)
            ax.set_ylabel("Eixo Y", fontsize=16)
            ax.tick_params(axis='both', labelsize=12)

            ax.set_xticks(np.arange(np.floor(x_vals[0]), np.ceil(x_vals[-1]) + 1, 1))
            ax.set_yticks(np.arange(-10, 11, 1))

            ax.set_ylim(-10, 10)
            ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
            ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
            ax.grid(color='gray', linestyle='--', linewidth=0.5)
            ax.plot(x_vals, y_vals, label=f"{a}x² + {b}x + {c}", color="blue")
            ax.legend(fontsize=14)

            self.remove_grafico()

            # Cria o widget do gráfico
            self.graph_widget = FigureCanvasKivyAgg(fig)

            # Cria o scatter com tamanho e posição definidos
            self.scatter = Scatter(size_hint=(1, 0.6), pos_hint={"x": 0, "y": 0.3}, do_rotation=False)
            self.scatter.add_widget(self.graph_widget)

            # Adiciona ao layout principal
            self.main_layout.add_widget(self.scatter)

        except Exception as e:
            print(f"Erro ao gerar gráfico: {e}")

    def atualiza_a(self, instance, value):
        self.a_input.text = str(round(value, 2))
        self.gera_grafico(None)

    def atualiza_b(self, instance, value):
        self.b_input.text = str(round(value, 2))
        self.gera_grafico(None)

    def atualiza_c(self, instance, value):
        self.c_input.text = str(round(value, 2))
        self.gera_grafico(None)

    def remove_grafico(self):
        if hasattr(self, 'scatter') and self.scatter:
            if self.scatter in self.main_layout.children:
                self.main_layout.remove_widget(self.scatter)
            self.scatter.clear_widgets()
            self.scatter = None
        plt.close()


    def botoes_trigonometrica(self):
        import numexpr as ne
        self.layout = FloatLayout()
        self.remove_grafico()

        self.entrada_funcao = TextInput(
            text="1 + sin(x)",
            font_size=55,
            size_hint=(0.6, 0.06),
            pos_hint={"x": 0.2, "y": 0.9}
        )
        self.layout.add_widget(self.entrada_funcao)

        # Sliders
        self.slider_amplitude = Slider(min=-10, max=10, value=1, step=1, size_hint=(0.4, 0.05), pos_hint={"x": 0.55, "y": 0.85})
        self.slider_frequencia = Slider(min=-10, max=10, value=1, step=1, size_hint=(0.4, 0.05), pos_hint={"x": 0.55, "y": 0.77})
        self.slider_deslocamento = Slider(min=-10, max=10, value=0, step=1, size_hint=(0.4, 0.05), pos_hint={"x": 0.55, "y": 0.69})

        self.label_amplitude = Label(text=f"Amplitude: {self.slider_amplitude.value}", font_size=45, size_hint=(0.2, 0.05), pos_hint={"x": 0.1, "y": 0.85})
        self.label_frequencia = Label(text=f"Frequência: {self.slider_frequencia.value}", font_size=45, size_hint=(0.2, 0.05), pos_hint={"x": 0.1, "y": 0.77})
        self.label_deslocamento = Label(text=f"Deslocamento: {self.slider_deslocamento.value}", font_size=45, size_hint=(0.2, 0.05), pos_hint={"x": 0.1, "y": 0.69})

        self.layout.add_widget(self.label_amplitude)
        self.layout.add_widget(self.slider_amplitude)
        self.layout.add_widget(self.label_frequencia)
        self.layout.add_widget(self.slider_frequencia)
        self.layout.add_widget(self.label_deslocamento)
        self.layout.add_widget(self.slider_deslocamento)

        botao_atualizar = Button(text="Atualizar", font_size=35, size_hint=(0.3, 0.05), pos_hint={"x": 0.35, "y": 0.63})
        botao_atualizar.bind(on_press=self.atualizar_grafico_trig)
        self.layout.add_widget(botao_atualizar)

        self.figura, self.ax = plt.subplots(figsize=(12, 8))
        self.grafico = FigureCanvasKivyAgg(self.figura)
        self.grafico.size_hint = (1, 0.6)
        self.grafico.pos_hint = {"x": 0, "y": 0.02}
        self.layout.add_widget(self.grafico)

        self.slider_amplitude.bind(value=self.atualizar_equacao_trig)
        self.slider_frequencia.bind(value=self.atualizar_equacao_trig)
        self.slider_deslocamento.bind(value=self.atualizar_equacao_trig)

        self.buttons_layout.clear_widgets()
        self.buttons_layout.add_widget(self.layout)

        Clock.schedule_once(lambda dt: self.atualizar_grafico_trig(), 0.1)




    def atualizar_equacao_trig(self, *args):
        self.label_amplitude.text = f"Amplitude: {int(self.slider_amplitude.value)}"
        self.label_frequencia.text = f"Frequência: {int(self.slider_frequencia.value)}"
        self.label_deslocamento.text = f"Deslocamento: {int(self.slider_deslocamento.value)}"

    def atualizar_grafico_trig(self, *args):
        import numexpr as ne
        try:
            funcao = self.entrada_funcao.text.lower()
            funcao = funcao.replace("sen", "sin").replace("tg", "tan").replace("^", "**")

            x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
            freq = self.slider_frequencia.value
            amp = self.slider_amplitude.value
            desl = self.slider_deslocamento.value

            # A variável x que será passada ao numexpr precisa ser um array
            local_dict = {
                "x": x,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "cot": lambda x: 1 / np.tan(x),
                "csc": lambda x: 1 / np.sin(x),
                "sec": lambda x: 1 / np.cos(x),
                "arcsin": np.arcsin,
                "arccos": np.arccos,
                "arctan": np.arctan,
                "pi": np.pi,
                "e": np.e
            }

            y = ne.evaluate(funcao, local_dict)

            y = amp * y + desl  # Aplicar sliders

            self.ax.clear()
            self.ax.plot(x, y, label=self.entrada_funcao.text, linewidth=2, color="blue")

            self.ax.axhline(0, color='black', linewidth=1)
            self.ax.axvline(0, color='black', linewidth=1)
            self.ax.set_ylim(-10, 10)
            self.ax.set_xlim(x[0], x[-1])
            self.ax.grid(True, linestyle="--", linewidth=0.5)
            self.ax.set_title("Gráfico da Função Trigonométrica", fontsize=20)
            self.ax.set_xlabel("X", fontsize=16)
            self.ax.set_ylabel("Y", fontsize=16)
            self.ax.legend(fontsize=14)
            self.grafico.draw()

        except Exception as e:
            print("Erro ao calcular função trigonométrica:", e)


Calculadora().run()