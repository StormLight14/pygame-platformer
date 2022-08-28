from difflib import IS_LINE_JUNK
import pygame
from game.gun import Gun, PlayerBullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, gravity, groups, tile_sprites, enemy_sprites, visibile_sprites, bullet_sprites, level, screen):
        super().__init__(groups)

        self.lives = int(level.game_data[4])
        self.level = level

        # movement
        self.velocity = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(pos)
        self.speed = 6.5

        # collision
        self.tile_sprites = tile_sprites
        self.enemy_sprites = enemy_sprites
        self.visible_sprites = visibile_sprites 
        self.colliding = {"x": False, "y": False}

        # gravity
        self.default_gravity_speed = gravity
        self.gravity_speed = self.default_gravity_speed
        self.is_jumping = False

        # display
        self.image = pygame.image.load("./game/assets/player.png").convert()
        self.rect = self.image.get_rect(topleft = pos)

        # gun 
        self.reload_cooldown = 10

        self.direction = 'right'
        self.screen = screen
        self.bullet_sprites = bullet_sprites



    def create_bullet(self):
                
        if self.reload_cooldown <= 0:
                PlayerBullet(self.rect.centerx, self.rect.centery, [self.visible_sprites, self.bullet_sprites], self.direction, self.enemy_sprites, self.screen)
                self.reload_cooldown = 10

    def cooldown(self):
        if self.reload_cooldown > 0:
            self.reload_cooldown -= 1

    def input(self):
        # check for A and D keys
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        if keys[pygame.K_a]:
            self.velocity.x -= 1
            self.direction = 'left'

        if keys[pygame.K_d]:
            self.velocity.x += 1
            self.direction = 'right'

        if keys[pygame.K_r]:
            self.rect.y = 0
            self.gravity_speed = 0

        if mouse_keys[0]:
            self.create_bullet()

        if self.is_jumping == False:
            if keys[pygame.K_SPACE]:
                self.gravity_speed = -2.75
                self.is_jumping = True

    def move(self):
        
        # update position based on velocity
        self.rect.x += (self.velocity.x * self.speed)
        self.collision("horizontal")
        self.rect.y += (self.velocity.y * self.speed)
        self.collision("vertical")


        # reset velocity every frame
        self.velocity.x = 0

        if self.colliding["y"]:
            self.velocity.y = 0

    def gravity(self):
        if self.velocity.y > 0:
            self.is_jumping = True
        if not self.colliding["y"]:
            if self.gravity_speed < 4:
                if self.is_jumping == True:
                    self.gravity_speed += 0.1
                elif self.is_jumping == False:
                    self.gravity_speed += 0.02
            self.velocity.y = self.gravity_speed

        for sprite in self.tile_sprites:
            if not sprite.rect.colliderect(self.rect):
                self.colliding["y"] = False

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.tile_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.velocity.x < 0:
                        self.colliding["x"] = True
                        self.rect.left = sprite.rect.right
                    if self.velocity.x > 0:
                        self.colliding["x"] = True
                        self.rect.right = sprite.rect.left

        if direction == 'vertical':
            for sprite in self.tile_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.velocity.y > 0:
                        self.colliding["y"] = True
                        self.gravity_speed = self.default_gravity_speed
                        self.is_jumping = False
                        self.rect.bottom = sprite.rect.top
                    elif self.velocity.y < 0:
                        self.gravity_speed /= 2
                        self.rect.top = sprite.rect.bottom

    def enemy_collision(self):
        for sprite in self.enemy_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.kill()
                self.lives -= 1
                if self.lives <= 0:
                    self.lives = 3
                    self.level.reset_game()

    def update(self):
        self.input()
        self.move()
        self.gravity()
        self.enemy_collision()
        self.cooldown()
