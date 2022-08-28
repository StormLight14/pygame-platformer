import pygame, sys
from game.level import Level
from game.player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920,1080))
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()

        self.level = Level(self.screen)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.level.save_game()
                    pygame.quit()
                    sys.exit()
            
            self.level.run()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
