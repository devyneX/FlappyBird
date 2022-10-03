from .controller import Game
import pygame


def init_game():
    pygame.init()
    game = Game(500, 600, 15)
    return game
