from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle


class Jogo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Fundo personalizado
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Fundo cinza claro
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Título
        self.layout.add_widget(
            Label(
                text="Palavra Cruzada Matemática",
                font_size="24sp",
                size_hint=(0.8, None),
                height=50,
                pos_hint={"center_x": 0.5, "top": 0.95},
                bold=True,
                color=(0, 0, 0, 1),  # Preto
            )
        )

        # Adicionar o tabuleiro
        self.board = GameBoard(size_hint=(0.9, 0.7), pos_hint={"center_x": 0.5, "center_y": 0.55})
        self.layout.add_widget(self.board)


# Botão de verificar
        verificar_btn = Button(
            text="Verificar",
            size_hint=(0.3, None),
            height=60,
            pos_hint={"center_x": 0.5, "y": 0.05},
            background_color=(0, 0.6, 0, 1),  # Verde
            color=(1, 1, 1, 1),  # Branco
            on_release=self.verificar_respostas,
        )
        self.layout.add_widget(verificar_btn)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def verificar_respostas(self, *args):
        """Verifica as respostas preenchidas no tabuleiro."""
        if self.board.check_answers():
            print("Parabéns! Todas as respostas estão corretas!")
        else:
            print("Algumas respostas estão incorretas. Tente novamente!")


class GameBoard(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Estrutura do tabuleiro
        self.board_structure = [
            ["", "+", "7", "=", "17", None, None],
            ["+", None, "+", None, None, None, None],
            ["", None, "", None, "", "+", "3"],
            ["=", None, "=", None, "-", None, None],
            ["19", "-", "", "=", "7", None, None],
        ]

        self.cells = []  # Armazena as células interativas
        self.create_board()

    def create_board(self):
        # Limpa o layout atual
        self.clear_widgets()

        rows = len(self.board_structure)
        cols = len(self.board_structure[0])
        cell_width = self.width / cols
        cell_height = self.height / rows

        for row_index, row in enumerate(self.board_structure):
            for col_index, cell in enumerate(row):
                x = col_index * cell_width
                y = self.height - (row_index + 1) * cell_height

                if cell is None:
                    # Espaços pretos
                    with self.canvas:
                        Color(0, 0, 0, 1)
                        Rectangle(pos=(x, y), size=(cell_width, cell_height))
                elif cell == "":
                    # Campos interativos
                    text_input = TextInput(
                        multiline=False,
                        halign="center",
                        font_size=20,
                        size_hint=(None, None),
                        size=(cell_width - 6, cell_height - 6),
                        pos=(x + 3, y + 3),
                        background_color=(1, 1, 1, 1),
                    )
                    self.add_widget(text_input)
                    self.cells.append((row_index, col_index, text_input))
                else:
                    # Campos fixos
                    label = Label(
                        text=str(cell),
                        font_size=20,
                        halign="center",
                        valign="middle",
                        size_hint=(None, None),
                        size=(cell_width, cell_height),
                        pos=(x, y),
                        color=(0, 0, 0, 1),
                    )
                    self.add_widget(label)

    def check_answers(self):
        """Valida as respostas do jogador."""
        for row, col, widget in self.cells:
            if not widget.text.isdigit():
                return False

            # Converte o valor digitado para inteiro
            value = int(widget.text)

            # Valida com base na lógica do tabuleiro
            if self.board_structure[row][col] == "=":
                left = int(self.board_structure[row][col - 2])
                operator = self.board_structure[row][col - 1]
                right = int(self.board_structure[row][col + 1])

                if operator == "+" and left + right != value:
                    return False
                if operator == "-" and left - right != value:
                    return False

        return True

