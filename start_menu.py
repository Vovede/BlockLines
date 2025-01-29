from main import main
import pygame
import sys

pygame.init()

window_width = 500
window_height = 700

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Block Lines")

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)


# Функция для отрисовки текста
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# Класс для кнопок
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, text_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False

    def draw(self, surface):
        if self.hovered:
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        draw_text(self.text, small_font, self.text_color, surface, self.rect.centerx, self.rect.centery)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self):
        return self.hovered


# Функция главного меню
def main_menu():
    infinite_button = Button("Бесконечный", window_width // 2 - 125, window_height // 2 - 50, 250, 50,
                             pygame.Color("blue"), pygame.Color("green"), pygame.Color("white"))
    adventure_button = Button("Приключения", window_width // 2 - 125, window_height // 2 + 50, 250, 50,
                              pygame.Color("blue"), pygame.Color("green"), pygame.Color("white"))
    quit_button = Button("Выйти", window_width // 2 - 125, window_height // 2 + 150, 250, 50,
                         pygame.Color("blue"), pygame.Color("red"), pygame.Color("white"))

    while True:
        screen.fill((50, 130, 255))

        draw_text("Block Lines", font, pygame.Color("black"), screen, window_width // 2, window_height // 4)

        infinite_button.draw(screen)
        adventure_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                infinite_button.check_hover(event.pos)
                adventure_button.check_hover(event.pos)
                quit_button.check_hover(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if infinite_button.is_clicked():
                        return "play"
                    if infinite_button.is_clicked():
                        return "adventure"
                    if quit_button.is_clicked():
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()


def start_game():
    while True:
        menu = main_menu()

        if menu == "play":
            main()
        if menu == "adventure":
            pass


if __name__ == "__main__":
    start_game()
