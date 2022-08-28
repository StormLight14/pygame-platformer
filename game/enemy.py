import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, id, player, groups):
        super().__init__(groups)
        self.player = player
        self.hurt_time = 30

        self.lives = 3

        self.image = pygame.image.load(f"./game/assets/enemy0.png")
        self.rect = self.image.get_rect(topleft = pos)

    def player_collide(self):
        if self.rect.colliderect(self.player.rect):
            self.kill()

    def update(self):
        self.player_collide()
