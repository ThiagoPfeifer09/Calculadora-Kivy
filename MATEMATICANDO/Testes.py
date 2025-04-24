import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 60
BG_COLOR = (230, 230, 230)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 153, 0)
TEXT_COLOR = (0, 0, 0)

# Configura a fonte
FONT = pygame.font.SysFont("arial", 20)

# Estrutura do tabuleiro (formato irregular)
BOARD_STRUCTURE = [
    ["", "+", "7", "=", "17", None, None, None, None],
    ["+", None, "+", None, None, None, None, None, None],
    ["", None, "", None, "", "+", "3", "=", ""],
    ["=", None, "=", None, "-", None, None, None, None],
    ["19", "-", "", "=", "7", None, None, None, None],
    [None, None, None, None, "=", None, None, None, None],
    [None, None, None, None, "10", None, None, None, None],
]


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Palavra Cruzada Matemática")
        self.running = True
        self.cells = self.create_board()
        self.input_active = None  # Célula atualmente ativa para entrada

    def create_board(self):
        """Cria os elementos do tabuleiro com base na estrutura."""
        cells = []
        rows = len(BOARD_STRUCTURE)
        cols = len(BOARD_STRUCTURE[0])
        board_width = cols * CELL_SIZE
        board_height = rows * CELL_SIZE
        origin_x = (SCREEN_WIDTH - board_width) // 2
        origin_y = (SCREEN_HEIGHT - board_height) // 2

        for row_index, row in enumerate(BOARD_STRUCTURE):
            for col_index, cell in enumerate(row):
                x = origin_x + col_index * CELL_SIZE
                y = origin_y + row_index * CELL_SIZE
                if cell is None:
                    cells.append({"type": "black", "rect": pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)})
                elif cell == "":
                    cells.append({"type": "input", "rect": pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), "value": ""})
                else:
                    cells.append({"type": "static", "rect": pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), "value": cell})
        return cells

    def draw_board(self):
        """Desenha o tabuleiro na tela."""
        self.screen.fill(BG_COLOR)

        # Título
        title_text = FONT.render("Palavra Cruzada Matemática", True, TEXT_COLOR)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))

        # Desenha as células
        for cell in self.cells:
            rect = cell["rect"]
            if cell["type"] == "black":
                pygame.draw.rect(self.screen, BLACK, rect)
            elif cell["type"] == "input":
                pygame.draw.rect(self.screen, WHITE, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 2)  # Borda
                if cell["value"]:
                    value_text = FONT.render(cell["value"], True, TEXT_COLOR)
                    self.screen.blit(
                        value_text,
                        (rect.x + CELL_SIZE // 2 - value_text.get_width() // 2, rect.y + CELL_SIZE // 2 - value_text.get_height() // 2),
                    )
            elif cell["type"] == "static":
                pygame.draw.rect(self.screen, WHITE, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 2)  # Borda
                value_text = FONT.render(str(cell["value"]), True, TEXT_COLOR)
                self.screen.blit(
                    value_text,
                    (rect.x + CELL_SIZE // 2 - value_text.get_width() // 2, rect.y + CELL_SIZE // 2 - value_text.get_height() // 2),
                )

        # Botão de verificar
        self.verify_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50)
        pygame.draw.rect(self.screen, GREEN, self.verify_button)
        button_text = FONT.render("Verificar", True, WHITE)
        self.screen.blit(button_text, (self.verify_button.x + 50, self.verify_button.y + 10))

    def handle_event(self, event):
        """Lida com eventos do teclado e mouse."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Verifica se clicou em uma célula de entrada
            for cell in self.cells:
                if cell["type"] == "input" and cell["rect"].collidepoint(pos):
                    self.input_active = cell
                    break
            # Verifica se clicou no botão "Verificar"
            if self.verify_button.collidepoint(pos):
                self.verify_answers()

        if event.type == pygame.KEYDOWN and self.input_active:
            # Permite digitar apenas números
            if event.unicode.isdigit():
                self.input_active["value"] += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                self.input_active["value"] = self.input_active["value"][:-1]

    def verify_answers(self):
        """Verifica as respostas no tabuleiro."""
        def get_cell_value(row, col):
            """Retorna o valor da célula, seja estático ou preenchido pelo jogador."""
            for cell in self.cells:
                cell_row = (cell["rect"].y - ((SCREEN_HEIGHT - len(BOARD_STRUCTURE) * CELL_SIZE) // 2)) // CELL_SIZE
                cell_col = (cell["rect"].x - ((SCREEN_WIDTH - len(BOARD_STRUCTURE[0]) * CELL_SIZE) // 2)) // CELL_SIZE
                if cell_row == row and cell_col == col:
                    if cell["type"] == "input":
                        return int(cell["value"]) if cell["value"].isdigit() else None
                    elif cell["type"] == "static":
                        return int(cell["value"]) if str(cell["value"]).isdigit() else cell["value"]
            return None

        correct = True
        for row_index, row in enumerate(BOARD_STRUCTURE):
            for col_index, cell in enumerate(row):
                if cell == "=":
                    left_value = get_cell_value(row_index, col_index - 2)
                    operator = get_cell_value(row_index, col_index - 1)
                    result = get_cell_value(row_index, col_index + 1)
                    if operator == "+" and left_value + result != result:
                        correct = False
                    elif operator == "-" and left_value - result != result:
                        correct = False
                    elif operator == "=" and result != left_value:
                        correct = False

        if correct:
            print("Parabéns! Todas as respostas estão corretas!")
        else:
            print("Algumas respostas estão incorretas. Tente novamente!")

    def run(self):
        """Roda o loop principal do jogo."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)

            self.draw_board()
            pygame.display.flip()


# Executa o jogo
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
