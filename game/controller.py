import pygame
import time
from random import randint
from .models import Bar, Bird
from .views import Screen


class Game:
    def __init__(self, screen_width: int, screen_height: int,  fps: int) -> None:
        # constants
        self.G = screen_height // 60
        self.bird_size = screen_width // 10
        self.bar_width = screen_width // 10
        self.bar_velocity = screen_width // 50
        self.bar_hgap = screen_width - (screen_width // 2 - screen_width // 25)
        self.bar_vgap = screen_height // 3
        self.bar_min_top_height = screen_height // 6
        self.bar_max_top_height = screen_height - screen_height // 6 - self.bar_vgap
        self.fps = fps

        # others
        self.screen = Screen(screen_width, screen_height,
                             'Flappy Bird', self.bird_size)
        self.bird = Bird(screen_width // 2 - screen_width //
                         20, screen_height // 2, -screen_height // 20)

        self.cur_bar = Bar(2 * self.screen.WIDTH,
                           randint(self.bar_min_top_height, self.bar_max_top_height))
        self.next_bar = Bar(2 * self.screen.WIDTH + self.bar_hgap,
                            randint(self.bar_min_top_height, self.bar_max_top_height))

        self.game_over = False
        self.started = False

    def bar_change(self) -> None:
        if self.cur_bar.x == -self.bar_width:
            self.cur_bar = self.next_bar
            self.next_bar = Bar(self.cur_bar.x + self.bar_hgap,
                                randint(self.bar_min_top_height, self.bar_max_top_height))

    def check_status(self) -> None:
        if 0 < self.bird.y < self.screen.HEIGHT:
            if self.bird.x <= self.cur_bar.x <= self.bird.x + self.bird_size or self.bird.x <= self.cur_bar.x + self.bar_width <= self.bird.x + self.bird_size:
                if self.bird.y <= self.cur_bar.top_height:
                    self.handle_bird_pos(self.cur_bar, True)
                    self.game_over = True
                elif self.bird.y + self.bird_size >= self.cur_bar.top_height + self.bar_vgap:
                    self.handle_bird_pos(self.cur_bar, False)
                    self.game_over = True
            elif self.bird.x <= self.next_bar.x <= self.bird.x + self.bird_size or self.bird.x <= self.next_bar.x + self.bar_width <= self.bird.x + self.bird_size:
                if self.bird.y <= self.next_bar.top_height:
                    self.handle_bird_pos(self.next_bar, True)
                    self.game_over = True
                elif self.bird.y + self.bird_size >= self.next_bar.top_height + self.bar_vgap:
                    self.handle_bird_pos(self.next_bar, False)
                    self.game_over = True
        elif self.bird.y <= 0:
            self.bird.y = 0
            self.game_over = True
        else:
            self.game_over = True

    def handle_bird_pos(self, bar: Bar, top: bool) -> None:
        if top:
            if bar.top_height >= self.bird.y - self.bird.velocity:
                self.bird.x = bar.x - self.bird_size + self.bird_size // 5
                self.bird.y -= self.bird.velocity
            else:
                self.bird.y = bar.top_height - self.bird_size // 5
        else:
            if bar.top_height + self.bar_vgap <= self.bird.y - self.bird.velocity:
                self.bird.x = bar.x - self.bird_size + self.bird_size // 5
                self.bird.y -= self.bird.velocity
            else:
                self.bird.y = bar.top_height + self.bar_vgap - \
                    self.bird_size + self.bird_size // 5

    def update(self) -> None:
        if self.game_over:
            self.screen.game_over_screen()
        else:
            if self.started:
                self.bird.move(self.G)
                self.cur_bar.move(self.bar_velocity)
                self.next_bar.move(self.bar_velocity)
                self.bar_change()

                self.check_status()

            self.screen.update_display(self.bird.x, self.bird.y, self.cur_bar.x, self.cur_bar.top_height,
                                       self.next_bar.x, self.next_bar.top_height, self.bar_width, self.bar_vgap)

    def run(self) -> None:
        running = True
        clock = pygame.time.Clock()
        while running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_over:
                            self.__init__(self.screen.WIDTH,
                                          self.screen.HEIGHT, self.fps)
                        elif self.started:
                            self.bird.jumped = True
                        else:
                            self.started = True
                            self.bird.jumped = True

            self.update()

        pygame.quit()
