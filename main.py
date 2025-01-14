import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
        colors = [pygame.Color("black"), pygame.Color("white")]
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, colors[self.board[y][x]],
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size))

                pygame.draw.rect(screen, pygame.Color("white"),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, pos):
        pass
        # cell = self.get_cell(pos)
        # if cell:
        #     self.on_click(cell)
        # else:
        #     print(cell)

    def get_cell(self, pos):
        pass
        # pos_x = (pos[0] - self.left) // self.cell_size
        # pos_y = (pos[1] - self.left) // self.cell_size
        #
        # if pos_x < 0 or pos_x >= self.width or pos_y < 0 or pos_y >= self.height:
        #     return None
        # else:
        #     return pos_x, pos_y

    def on_click(self, cell):
        pass
        # for x in range(self.width):
        #     self.board[cell[1]][x] = (self.board[cell[1]][x] + 1) % 2
        # for y in range(self.height):
        #     if y == cell[1]:
        #         continue
        #     self.board[y][cell[0]] = (self.board[y][cell[0]] + 1) % 2


def main():
    pygame.init()
    pygame.display.set_caption("Color invertion")

    board = Board(8, 8)
    board.set_view(50, 50, 50)

    size = ((board.width + 2) * board.left, (board.height + 6) * board.top)
    screen = pygame.display.set_mode(size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
