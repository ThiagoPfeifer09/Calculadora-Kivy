from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
import random

class Calculos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer = 0
        self.running = False
        self.operacao = "Soma"  # Operação padrão
        self.rodadas = 0  # Número total de rodadas
        self.rodada_atual = 0  # Rodada atual
        self.nivel_atual = 1  # Nível atual
        self.resp_correta = 0  # Contador de acertos
        self.resp_errada = 0  # Contador de erros
        self.dialog = None
        self.nivel_max = 4  # Total de níveis
        self.dificuldade = "primario"  # Padrão para primário (mais fácil)
        self.tudo_desbloqueado = False  # Indica se tudo está desbloqueado

        # Layout principal
        layout = FloatLayout()

        # Título
        layout.add_widget(Label(text="MATEMATICANDO", font_size=40, bold=True,
                                pos_hint={"center_x": 0.5, "center_y": 0.95}))

        # Pergunta (Movida para cima)
        self.question_label = Label(
            text="Escolha uma operação e um nível para começar!",
            font_size=42,
            pos_hint={"center_x": 0.5, "center_y": 0.86},
        )
        layout.add_widget(self.question_label)

        # Entrada de resposta (Movida para cima)
        self.answer_input = MDTextField(
            hint_text="Digite a resposta",
            size_hint=(0.6, None),
            height=45,
            pos_hint={"center_x": 0.55, "center_y": 0.8},
            multiline=False,
        )
        layout.add_widget(self.answer_input)

        layout.add_widget(
            Label(
                text="Operações:",
                font_size=35,
                pos_hint={"center_x": 0.3, "center_y": 0.57},  # CORRETO
            )
        )

        layout.add_widget(
            Label(
                text="Níveis:",
                font_size=35,
                pos_hint={"center_x": 0.72, "center_y": 0.57},  # CORRETO
            )
        )

        #Botão de responder
        layout.add_widget(
            MDRaisedButton(
                text="Responder",
                size_hint=(0.3, 0.08),
                pos_hint={"center_x": 0.5, "center_y": 0.7},
                md_bg_color=(0.2, 0.6, 0.8, 1),
                text_color=(1, 1, 1, 1),
                on_release=self.verifica_resposta,
            )
        )

        # Botão de voltar (Retorna para o nível a tela de selecionar os níveis)
        layout.add_widget(
            MDRaisedButton(
                text="Voltar",
                size_hint=(0.1, 0.05),
                pos_hint={"center_x": 0.15, "center_y": 0.95},
                md_bg_color=(1, 0.3, 0.3, 1),
                text_color=(1, 1, 1, 1),
                on_release=self.ir_para_niveis,
            )
        )

        self.score_label = Label(
            text="Acertos: 0 | Erros: 0",
            font_size=40,
            pos_hint={"center_x": 0.5, "center_y": 0.63},
        )
        layout.add_widget(self.score_label)

        buttons_operacaos = [
            ("Soma", 0.52, (0, 0.6, 0, 1)),
            ("Subt", 0.42, (0, 0, 0.8, 1)),
            ("Mult", 0.32, (0.6, 0, 0.6, 1)),
            ("Div", 0.22, (0.5, 0.5, 0.5, 1)),
        ]

        for text, pos_y, color in buttons_operacaos:
            layout.add_widget(
                MDRaisedButton(
                    text=text,
                    size_hint=(0.33, 0.08),  # Aumentado de 0.2 para 0.3
                    pos_hint={"center_x": 0.3, "center_y": pos_y},
                    md_bg_color=color,
                    text_color=(1, 1, 1, 1),
                    on_release=lambda btn: self.escolhe_operacao(btn.text),
                )
            )

        self.nivel_botoes = {}
        nivel_cores = [(0, 0.6, 0, 1), (0, 0, 0.8, 1), (0.6, 0, 0.6, 1), (0.5, 0.5, 0.5, 1)]

        for level, pos_y, color in zip(range(1, self.nivel_max + 1), [0.52, 0.42, 0.32, 0.22], nivel_cores):
            btn = MDRaisedButton(
                text=f"Nível {level}",
                size_hint=(0.35, 0.08),
                pos_hint={"center_x": 0.72, "center_y": pos_y},
                md_bg_color=(0.7, 0.7, 0.7, 1) if level != 1 else color,  # Cinza se bloqueado
                text_color=(1, 1, 1, 1),
                on_release=lambda _, lvl=level: self.inicia_nivel(lvl),
            )
            btn.disabled = level != 1  # Apenas o nível 1 começa habilitado
            btn.original_color = color  # Salva a cor original para desbloqueio
            self.nivel_botoes[level] = btn
            layout.add_widget(btn)



        self.timer_label = Label(
            text="00:00:00",
            font_size=50,
            pos_hint={"center_x": 0.5, "center_y": 0.13},
        )
        layout.add_widget(self.timer_label)

        control_buttons = [
            ("Iniciar", 0.26, self.start_timer, (0, 0.6, 0, 1)),
            ("Parar", 0.5, self.pause_timer, (0.6, 0, 0.6, 1)),
            ("Reiniciar", 0.75, self.reset_timer, (0, 0, 0.8, 1)),
        ]

        for text, pos_x, callback, color in control_buttons:
            layout.add_widget(
                MDRaisedButton(
                    text=text,
                    size_hint=(0.2, 0.05),
                    pos_hint={"center_x": pos_x, "center_y": 0.05},
                    md_bg_color=color,
                    text_color=(1, 1, 1, 1),
                    on_release=callback,
                )
            )

        self.add_widget(layout)

    def define_dificul(self, dificuldade):
        self.dificuldade = dificuldade
        self.nivel_atual = 1  # Reseta o nível para 1 ao alterar a dificuldade
        self.cria_questao()  # Atualiza a questão com a nova dificuldade

    def on_enter(self):
        """Exibe o popup ao entrar na tela."""
        self.mostra_popup()

    def mostra_popup(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Configurar Rodadas",
                text="Quantas rodadas você deseja jogar em cada nível?",
                type="custom",
                content_cls=MDTextField(hint_text="Digite o número de rodadas", multiline=False),
                buttons=[MDRaisedButton(text="Confirmar", on_release=self.confirma_rodadas)],
            )
        self.dialog.open()

    def confirma_rodadas(self, *args):
        try:
            input_value = int(self.dialog.content_cls.text)
            if input_value > 0:
                self.rodadas = input_value
                self.dialog.dismiss()
            else:
                self.dialog.content_cls.hint_text = "Digite um número válido!"
        except ValueError:
            self.dialog.content_cls.hint_text = "Digite um número inteiro!"

    def escolhe_operacao(self, operacao):
        self.operacao = operacao
        self.question_label.text = f"Operação escolhida: {operacao}"

    def inicia_nivel(self, level):
        if level != self.nivel_atual:
            return
        self.rodada_atual = 0
        self.question_label.text = f"Iniciando nível {level}..."
        self.cria_questao()

    def cria_questao(self):
        if self.dificuldade == "primario":
            max_value = 10  # Números até 10 (mais simples)
        elif self.dificuldade == "fundamental":
            max_value = 50  # Números até 50 (médio)
        else:  # Ensino Médio
            max_value = 100  # Números até 100 (difícil)

        num1 = random.randint(1, max_value)
        num2 = random.randint(1, max_value)

        if self.operacao == "Soma":
            self.question = f"{num1} + {num2}"
            self.answer = num1 + num2
        elif self.operacao == "Subt":
            self.question = f"{num1} - {num2}"
            self.answer = num1 - num2
        elif self.operacao == "Mult":
            self.question = f"{num1} x {num2}"
            self.answer = num1 * num2
        elif self.operacao == "Div":
            num1 = num1 * num2  # Garante que a divisão será exata
            self.question = f"{num1} ÷ {num2}"
            self.answer = num1 // num2

        self.question_label.text = self.question

    def verifica_resposta(self, *args):
        user_answer = self.answer_input.text
        try:
            if int(user_answer) == self.answer:
                self.resp_correta += 1
                self.question_label.text = "Correto!"
            else:
                self.resp_errada += 1
                self.question_label.text = "Errado!"
        except ValueError:
            self.resp_errada += 1
            self.question_label.text = "Insira um número válido!"

        # Atualiza o placar de acertos/erros
        self.score_label.text = f"Acertos: {self.resp_correta} | Erros: {self.resp_errada}"

        self.answer_input.text = ""
        self.rodada_atual += 1

        # Verifica se o número de acertos é suficiente para passar de nível
        if self.rodada_atual >= self.rodadas:
            # Só avança de nível se acertar o número necessário de questões
            if self.resp_correta >= self.rodadas:
                if self.nivel_atual < self.nivel_max:
                    self.nivel_atual += 1
                    # Desbloqueia o botão do próximo nível
                    next_button = self.nivel_botoes[self.nivel_atual]
                    next_button.disabled = False
                    next_button.md_bg_color = next_button.original_color  # Restaura a cor original
                    self.question_label.text = f"Nível {self.nivel_atual} desbloqueado!"
                else:
                    self.question_label.text = "Parabéns! Você concluiu todos os níveis!"
            # Se não tiver acertado o suficiente, o jogo continua normalmente sem interromper
            self.rodada_atual = 0  # Reinicia apenas a rodada
        else:
            self.cria_questao()  # Se ainda não terminou as rodadas, cria uma nova questão


    def start_timer(self, *args):
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.att_timer, 1)

    def pause_timer(self, *args):
        self.running = False
        Clock.unschedule(self.att_timer)

    def reset_timer(self, *args):
        self.running = False
        Clock.unschedule(self.att_timer)
        self.timer = 0
        self.timer_label.text = "00:00:00"

    def att_timer(self, dt):
        self.timer += 1
        minutes, seconds = divmod(self.timer, 60)
        hours, minutes = divmod(minutes, 60)
        self.timer_label.text = f"{hours:02}:{minutes:02}:{seconds:02}"

    def ir_para_niveis(self, instance):
        self.manager.current = "jogar"