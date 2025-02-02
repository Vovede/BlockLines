from pick_block_parameter import pick_parameters
import change_db
from _datetime import datetime
import pygame
import sys


# Принудительное завершение программы
def kill_program():
    pygame.quit()
    sys.exit()


# Класс для представления клетки на игровом поле
class Cell:
    def __init__(self, occupied=False, color=None):
        self.occupied = occupied
        self.color = color

    def set_occupied(self, color):
        self.occupied = True
        self.color = color

    def clear(self):
        self.occupied = False
        self.color = (50, 130, 255)


# Класс для представления блока
class Block:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.width = len(shape[0])
        self.height = len(shape)
        self.position = (0, 0)
        self.block_origin = (0, 0)
        self.is_placed = False

    def set_block_position(self, x, y):
        self.position = (x, y)

    # Отрисовка блока
    def draw_block(self, screen, cell_size):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color,
                                     (self.position[0] + x * cell_size,
                                      self.position[1] + y * cell_size,
                                      cell_size, cell_size))

    # Проверка курсора над блоком
    def is_mouse_over_block(self, mouse_pos, cell_size):
        mx, my = mouse_pos
        bx, by = self.position
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    hitbox = pygame.Rect(bx + x * cell_size, by + y * cell_size, cell_size, cell_size)
                    if hitbox.collidepoint(mx, my):
                        return True
        return False

    # Привязка блока к сетке
    def snap_to_grid(self, cell_size, grid_offset, grid_width, grid_height, board):
        gx, gy = grid_offset
        bx, by = self.position

        block_snapped_to_x = round((bx - gx) / cell_size) * cell_size + gx
        block_snapped_to_y = round((by - gy) / cell_size) * cell_size + gy

        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    cell_pos_in_grid_x = (block_snapped_to_x - gx) // cell_size + x
                    cell_pos_in_grid_y = (block_snapped_to_y - gy) // cell_size + y

                    if (cell_pos_in_grid_x < 0 or cell_pos_in_grid_x >= grid_width or
                            cell_pos_in_grid_y < 0 or cell_pos_in_grid_y >= grid_height):
                        self.set_block_position(*self.block_origin)
                        return

        self.set_block_position(block_snapped_to_x, block_snapped_to_y)
        self.is_placed = True

        if not board.can_place_block(self):
            self.set_block_position(*self.block_origin)


# Класс для представления игрового поля
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[Cell() for _ in range(width)] for _ in range(height)]
        self.start_blocks = []
        self.block_positions = []
        self.blocks_placed = 0
        self.score = 0
        self.score_multiplier = 0
        self.db = change_db.historyDB()
        self.historyData = {}

        self.left = 10
        self.top = 10
        self.cell_size = 30

    # Отрисовка игрового поля
    def render_board(self, screen):
        pygame.draw.rect(screen, pygame.Color("Black"),
                         (self.cell_size, self.cell_size,
                          self.width * self.cell_size,
                          self.height * self.cell_size,), 2)
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                if cell.occupied:
                    pygame.draw.rect(screen, cell.color, (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color("Black"), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # Проверка на возможность установки блока при перетаскивании
    def can_place_block(self, block):
        bx, by = block.position
        grid_x = (bx - self.left) // self.cell_size
        grid_y = (by - self.top) // self.cell_size

        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    board_x = grid_x + x
                    board_y = grid_y + y

                    if not (0 <= board_x < self.width and 0 <= board_y < self.height):
                        return False
                    if self.board[board_y][board_x].occupied:
                        return False
        return True

    # Установить блок на поле
    def set_block_on_board(self, block):
        if not self.can_place_block(block):
            block.set_block_position(*block.block_origin)

        bx, by = block.position
        grid_x = (bx - self.left) // self.cell_size
        grid_y = (by - self.top) // self.cell_size

        # Задать в матрице поля занятые клетки
        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell and 0 <= grid_x + x < self.width and 0 <= grid_y + y < self.height:
                    self.board[grid_y + y][grid_x + x].set_occupied(block.color)
                    self.score_multiplier += 1

        # Счёт
        self.score += 1 * self.score_multiplier
        self.score_multiplier = 0

        self.check_and_clear_lines()

        self.start_blocks.remove(block)

        # Проверка на возможность установки хотя бы одного из оставшихся блоков после установки
        if self.start_blocks:
            self.check_left_blocks_possibility()

        self.blocks_placed += 1
        if self.blocks_placed == 3:
            self.generate_three_blocks()
            self.blocks_placed = 0

        return True

    # Генерация трех новых блоков
    def generate_three_blocks(self):
        self.start_blocks = [Block(*pick_parameters()) for _ in range(3)]
        self.block_positions = [(i * 150 + 50, 500) for i in range(3)]

        for block, pos in zip(self.start_blocks, self.block_positions):
            block.block_origin = pos
            block.set_block_position(*pos)

        # Проверка на возможность установки хотя бы одного из сгенерированных блоков
        self.check_left_blocks_possibility()

    # Проверка собранных линий
    def check_and_clear_lines(self):
        # Проверяем горизонтальные линии
        for y in range(self.height):
            if all(cell.occupied for cell in self.board[y]):
                self.score_multiplier += 8
                for x in range(self.width):
                    self.board[y][x].clear()

        # Проверяем вертикальные линии
        for x in range(self.width):
            if all(self.board[y][x].occupied for y in range(self.height)):
                self.score_multiplier += 8
                for y in range(self.height):
                    self.board[y][x].clear()

        # Счёт
        self.score += 10 * self.score_multiplier
        print(self.score)
        self.score_multiplier = 0

    # Проверка на возможность установки хотя бы одного из оставшихся блоков
    def check_left_blocks_possibility(self):
        if not any(self.check_block_possibility(block) for block in self.start_blocks):
            return True
        return False

    # Проверка на возможность установки блока
    def check_block_possibility(self, block):
        for y in range(self.height):
            for x in range(self.width):
                block.set_block_position(x * self.cell_size + self.left, y * self.cell_size + self.top)
                if self.can_place_block(block):
                    block.set_block_position(*block.block_origin)
                    return True
        block.set_block_position(*block.block_origin)
        return False

    def save_history(self):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        self.historyData = {"Date": formatted_datetime,
                            "Score": self.score}
        self.db.add(self.historyData)


# Отрисовки текста
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# Класс для представления кнопок
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, text_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False

    # Отрисовка кнопки
    def draw(self, surface, small_font):
        if self.hovered:
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        draw_text(self.text, small_font, self.text_color, surface, self.rect.centerx, self.rect.centery)

    # Проверка пересечения с курсором
    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    # Нажатие
    def is_clicked(self):
        return self.hovered


# Функция стартового меню
def start_menu_window(size, screen, font, small_font):
    infinite_button = Button("Бесконечный", size[0] // 2 - 125, size[1] // 2 - 50, 250, 50,
                             pygame.Color("blue"), pygame.Color("green"), pygame.Color("white"))
    adventure_button = Button("Приключения", size[0] // 2 - 125, size[1] // 2 + 50, 250, 50,
                              pygame.Color("blue"), pygame.Color("green"), pygame.Color("white"))
    quit_button = Button("Выйти", size[0] // 2 - 125, size[1] // 2 + 150, 250, 50,
                         pygame.Color("blue"), pygame.Color("red"), pygame.Color("white"))

    while True:
        screen.fill((50, 130, 255))

        draw_text("Block Lines", font, pygame.Color("black"), screen, size[0] // 2, size[1] // 4)

        infinite_button.draw(screen, small_font)
        adventure_button.draw(screen, small_font)
        quit_button.draw(screen, small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kill_program()

            if event.type == pygame.MOUSEMOTION:
                infinite_button.check_hover(event.pos)
                adventure_button.check_hover(event.pos)
                quit_button.check_hover(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if infinite_button.is_clicked():
                        main(restart=True)
                    if adventure_button.is_clicked():
                        # return "adventure"
                        pass
                    if quit_button.is_clicked():
                        kill_program()

        pygame.display.flip()


# Основная функция игры
def main(restart=False):
    pygame.init()
    pygame.display.set_caption("Block Lines")

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)

    board = Board(8, 8)
    board.set_view(50, 50, 50)

    size = ((board.width + 2) * board.left, (board.height + 6) * board.top)
    screen = pygame.display.set_mode(size)

    if not restart:
        start_menu_window(size, screen, font, small_font)

    board.generate_three_blocks()

    running = True
    dragging = None
    drag_offset = (0, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for block in board.start_blocks:
                        if block.is_mouse_over_block(event.pos, board.cell_size):
                            dragging = block
                            mx, my = event.pos
                            bx, by = block.position
                            drag_offset = (mx - bx, my - by)
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging:
                    dragging.snap_to_grid(board.cell_size, (board.left, board.top), board.width,
                                          board.height, board)
                    if board.can_place_block(dragging):
                        board.set_block_on_board(dragging)
                        if board.check_left_blocks_possibility():
                            board.save_history()
                            game_over_window(size, screen, font, small_font)
                    dragging = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mx, my = event.pos
                    offset_x, offset_y = drag_offset
                    dragging.set_block_position(mx - offset_x, my - offset_y)

        screen.fill((50, 130, 255))
        board.render_board(screen)

        for block in board.start_blocks:
            block.draw_block(screen, board.cell_size)

        pygame.display.flip()

    kill_program()


# Функция окна проигрыша
def game_over_window(size, screen, font, small_font):
    main_menu_button = Button("Главное меню", size[0] // 2 - 125, size[1] // 2 - 50, 250, 50,
                              pygame.Color("blue"), pygame.Color("green"), pygame.Color("white"))
    restart_button = Button("Заново", size[0] // 2 - 125, size[1] // 2 + 50, 250, 50,
                            pygame.Color("blue"), pygame.Color("green"), pygame.Color("white"))
    quit_button = Button("Выйти", size[0] // 2 - 125, size[1] // 2 + 150, 250, 50,
                         pygame.Color("blue"), pygame.Color("red"), pygame.Color("white"))

    while True:
        screen.fill((50, 130, 255))

        draw_text("GAME OVER", font, pygame.Color("black"), screen, size[0] // 2, size[1] // 4)

        main_menu_button.draw(screen, small_font)
        restart_button.draw(screen, small_font)
        quit_button.draw(screen, small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                main_menu_button.check_hover(event.pos)
                restart_button.check_hover(event.pos)
                quit_button.check_hover(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if main_menu_button.is_clicked():
                        start_menu_window(size, screen, font, small_font)
                    if restart_button.is_clicked():
                        main(restart=True)
                    if quit_button.is_clicked():
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    main()
