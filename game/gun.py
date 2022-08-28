import pygame
import math

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        pass
    

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, direction, enemy_sprites, display):
        super().__init__(groups)
        self.image = pygame.image.load('./game/assets/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center = (x, y))
        self.lifetime = 0

        self.speed = 15
        self.direction = direction
        self.bullet_velocity = pygame.math.Vector2()

        self.display = display

        self.enemy_sprites = enemy_sprites

        if direction == 'right':
            self.bullet_velocity.x = self.speed
        elif direction == 'left':
            self.bullet_velocity.x = -self.speed

    def time(self):
        self.lifetime += 1
        if self.lifetime >= 240:
            self.kill()

    def collide(self):
        for sprite in self.enemy_sprites:
            if self.rect.colliderect(sprite.rect):
                self.kill()
                sprite.kill()


    def main(self, display):
        self.rect.x += int(self.bullet_velocity.x)
        display.blit(self.image, self.rect)

    def update(self):
        self.collide()
        self.time()
        self.main(self.display)