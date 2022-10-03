import pygame
import os


class BirdView:
    def __init__(self, size: int) -> None:
        self.image = pygame.transform.scale(pygame.image.load(
            os.path.join('images', 'bird.png')), (size, size))

    def draw(self,  win: pygame.Surface, x: int, y: int) -> None:
        win.blit(self.image, (x, y))


class BarView:
    def __init__(self) -> None:
        self.bottom_image = pygame.image.load(
            os.path.join('images', 'pipe.png'))
        self.top_image = pygame.transform.flip(self.bottom_image, False, True)

    def draw(self, win: pygame.Surface, x: int, y_bottom: int, top_height: int, bottom_height: int, width: int) -> None:
        img1 = pygame.transform.scale(self.top_image, (width, top_height))
        img2 = pygame.transform.scale(
            self.bottom_image, (width, bottom_height))
        win.blit(img1, (x, 0))
        win.blit(img2, (x, y_bottom))


class Screen:
    def __init__(self, width: int, height: int, text: int, bird_size: int) -> None:
        self.BG = pygame.image.load(os.path.join('images', 'bg.png'))
        self.WIDTH = width
        self.HEIGHT = height
        self.CAPTION = text
        self.window = self.make_window()
        self.bird_view = BirdView(bird_size)
        self.bar_view = BarView()

    def make_window(self) -> pygame.Surface:
        win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.CAPTION)
        self.BG = pygame.transform.scale(self.BG, (self.WIDTH, self.HEIGHT))
        win.blit(self.BG, (0, 0))
        return win

    def game_over_screen(self) -> None:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game Over !!', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (self.WIDTH // 2, self.HEIGHT //
                            2 - self.HEIGHT // 4)
        self.window.blit(text, text_rect)
        pygame.display.update()

    def update_display(self, bird_x: int, bird_y: int, bar_x1: int, top_height1: int, bar_x2: int, top_height2: int, bar_width: int, gap: int) -> None:
        self.window.blit(self.BG, (0, 0))
        self.bird_view.draw(self.window, bird_x, bird_y)
        bar_y1 = top_height1 + gap
        bottom_height1 = self.HEIGHT - top_height1 - gap
        self.bar_view.draw(self.window, bar_x1, bar_y1,
                           top_height1, bottom_height1, bar_width)
        bar_y2 = top_height2 + gap
        bottom_height2 = self.HEIGHT - top_height2 - gap
        self.bar_view.draw(self.window, bar_x2, bar_y2,
                           top_height2, bottom_height2, bar_width)
        pygame.display.update()
