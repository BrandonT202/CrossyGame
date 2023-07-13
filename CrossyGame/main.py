import pygame
from game import Game

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("assets/untitledv3.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

game = Game()
game.run_game_loop()

pygame.quit()
quit()