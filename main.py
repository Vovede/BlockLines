import pygame
import random

shapes = [
    [[1, 1],
     [1, 0]],

    [[1, 1],
     [0, 1]],

    [[1, 1, 1],
     [0, 1, 0]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1, 1]],

    [[1],
     [1],
     [1],
     [1]],

    [[1, 1],
     [1, 0],
     [1, 0]]
]

colors = [
    pygame.Color("red"),
    pygame.Color("green"),
    pygame.Color("blue"),
    pygame.Color("yellow")
]


class Block:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.width = len(shape[0])
        self.height = len(shape)
        self.position = (0, 0)

    def set_position(self, x, y):
        self.position = (x, y)

    def draw(self, screen, cell_size, offset):
        ox, oy = offset
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color,
                                     (self.position[0] + x * cell_size + ox,
                                      self.position[1] + y * cell_size + oy,
                                      cell_size, cell_size))

    def is_mouse_over_block(self, mouse_pos, cell_size):
        mouse_x, mouse_y = mouse_pos
        block_x, block_y = self.position
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    hitbox = pygame.Rect(block_x + (x + 1) * cell_size,
                                         block_y + (y + 1) * cell_size,
                                         cell_size, cell_size)
                    if hitbox.collidepoint(mouse_x, mouse_y):
                        return True
        return False


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color((0, 40, 100)),
                         (self.cell_size, self.cell_size,
                          self.width * self.cell_size,
                          self.height * self.cell_size,), 2)
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color((0, 40, 100)),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def add_block(self, block, position):
        px, py = position
        for y in range(block.height):
            for x in range(block.width):
                if block.shape[y][x] == 1:
                    self.board[py + y][px + x] = 1


def generate_random_block():
    shape = random.choice(shapes)
    color = random.choice(colors)
    return Block(shape, color)


def main():
    pygame.init()
    pygame.display.set_caption("Block Lines")

    board = Board(8, 8)
    board.set_view(50, 50, 50)

    size = ((board.width + 2) * board.left, (board.height + 6) * board.top)
    screen = pygame.display.set_mode(size)

    current_block = generate_random_block()
    running = True
    dragging = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if current_block.is_mouse_over_block(event.pos, board.cell_size):
                        dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    current_block.set_position(event.pos[0] - board.cell_size,
                                               event.pos[1] - board.cell_size)

        screen.fill((50, 130, 255))
        board.render(screen)

        current_block.draw(screen, board.cell_size, (board.left, board.top))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
