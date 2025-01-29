from pick_block_parameter import pick_parameters
import pygame


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

    def set_position(self, x, y):
        self.position = (x, y)

    def draw(self, screen, cell_size):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color,
                                     (self.position[0] + x * cell_size,
                                      self.position[1] + y * cell_size,
                                      cell_size, cell_size))

    def is_mouse_over_block(self, mouse_pos, cell_size):
        mouse_x, mouse_y = mouse_pos
        block_x, block_y = self.position
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    hitbox = pygame.Rect(block_x + x * cell_size,
                                         block_y + y * cell_size,
                                         cell_size, cell_size)
                    if hitbox.collidepoint(mouse_x, mouse_y):
                        return True
        return False

    def snap_to_grid(self, cell_size, grid_offset, grid_width, grid_height, board):
        gx, gy = grid_offset
        px, py = self.position

        block_snapped_to_x = round((px - gx) / cell_size) * cell_size + gx
        block_snapped_to_y = round((py - gy) / cell_size) * cell_size + gy

        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    cell_pos_in_grid_x = (block_snapped_to_x - gx) // cell_size + x
                    cell_pos_in_grid_y = (block_snapped_to_y - gy) // cell_size + y

                    if (cell_pos_in_grid_x < 0 or cell_pos_in_grid_x >= grid_width or
                            cell_pos_in_grid_y < 0 or cell_pos_in_grid_y >= grid_height):
                        self.set_position(*self.block_origin)
                        return

        self.set_position(block_snapped_to_x, block_snapped_to_y)
        self.is_placed = True

        if not board.check_block(self):
            self.set_position(*self.block_origin)


# Класс для представления игрового поля
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[Cell() for _ in range(width)] for _ in range(height)]
        self.start_blocks = []
        self.block_positions = []
        self.blocks_placed = 0

        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
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

    def check_block(self, block):
        px, py = block.position
        grid_x = (px - self.left) // self.cell_size
        grid_y = (py - self.top) // self.cell_size

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

    def add_block(self, block):
        if not self.check_block(block):
            block.set_position(*block.block_origin)
        px, py = block.position
        grid_x = (px - self.left) // self.cell_size
        grid_y = (py - self.top) // self.cell_size

        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell and 0 <= grid_x + x < self.width and 0 <= grid_y + y < self.height:
                    self.board[grid_y + y][grid_x + x].set_occupied(block.color)

        self.blocks_placed += 1
        self.start_blocks.remove(block)

        if self.blocks_placed == 3:
            self.generate_three_blocks()
            self.blocks_placed = 0

        self.check_and_clear_lines()
        return True

    def generate_three_blocks(self):
        self.start_blocks = [generate_random_block() for _ in range(3)]
        self.block_positions = [(i * 150 + 50, 500) for i in range(3)]

        for block, pos in zip(self.start_blocks, self.block_positions):
            block.block_origin = pos
            block.set_position(*pos)

    def check_and_clear_lines(self):
        # Проверяем горизонтальные линии
        for y in range(self.height):
            if all(cell.occupied for cell in self.board[y]):
                for x in range(self.width):
                    self.board[y][x].clear()

        # Проверяем вертикальные линии
        for x in range(self.width):
            if all(self.board[y][x].occupied for y in range(self.height)):
                for y in range(self.height):
                    self.board[y][x].clear()


# Функция для генерации случайного блока
def generate_random_block():
    return Block(*pick_parameters())


# Основная функция игры
def main():
    pygame.init()
    pygame.display.set_caption("Block Lines")

    board = Board(8, 8)
    board.set_view(50, 50, 50)

    size = ((board.width + 2) * board.left, (board.height + 6) * board.top)
    screen = pygame.display.set_mode(size)

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
                    if board.check_block(dragging):
                        board.add_block(dragging)
                        # for row in board.board:
                        #     for cell in row:
                        #         print(cell.occupied, end=" ")
                        #     print("\n")
                        # print("_____________________________")
                    dragging = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mx, my = event.pos
                    offset_x, offset_y = drag_offset
                    dragging.set_position(mx - offset_x, my - offset_y)

        screen.fill((50, 130, 255))
        board.render(screen)

        for block in board.start_blocks:
            block.draw(screen, board.cell_size)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
