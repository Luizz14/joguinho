import pygame
import random
import os
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, 'Boneco_Gordinho_A1.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT + 20 # Slight overlap for perspective
        self.speed = PLAYER_SPEED

        # Jump physics
        self.velocity_y = 0
        self.is_jumping = False
        self.jump_power = JUMP_POWER
        self.gravity = GRAVITY
        self.ground_y = SCREEN_HEIGHT - GROUND_HEIGHT + 20  # Store ground position

    def update(self):
        # Horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Horizontal boundary checks
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Jump physics
        # Apply gravity
        self.velocity_y += self.gravity

        # Update vertical position
        self.rect.y += self.velocity_y

        # Ground collision detection
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        """Trigger a jump if on ground"""
        if not self.is_jumping:
            self.velocity_y = self.jump_power
            self.is_jumping = True

class Food(pygame.sprite.Sprite):
    def __init__(self, force_type=None, speed_multiplier=1.0, difficulty_multiplier=1.0):
        super().__init__()

        # Use forced type if provided, otherwise random
        if force_type:
            self.type = force_type
        else:
            self.type = random.choice(['healthy', 'unhealthy'])

        if self.type == 'healthy':
            # Healthy foods: Alface, Banana, Maçã, Pêra
            filename = random.choice(['Alface.png', 'Banana.png', 'Maçã.png', 'Pêra.png'])
        else:
            # Unhealthy foods: Chocolate, Hamburguer, Refrigerante, Sorvete
            filename = random.choice(['Chocolate.png', 'Hamburguer.png', 'Refrigerante.png', 'Sorvete.png'])

        self.image = pygame.image.load(os.path.join(ASSETS_DIR, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (FOOD_SIZE, FOOD_SIZE))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - FOOD_SIZE)
        self.rect.y = random.randrange(-100, -40)

        # Calculate speed with progressive difficulty
        if force_type == 'unhealthy' and speed_multiplier > 1.0:
            # Event mode: use faster speeds
            base_speed = random.randrange(JUNK_RAIN_FOOD_MIN_SPEED, JUNK_RAIN_FOOD_MAX_SPEED)
        else:
            # Normal mode
            base_speed = random.randrange(FOOD_MIN_SPEED, FOOD_MAX_SPEED)

        # Apply both speed_multiplier (for events) and difficulty_multiplier (progressive)
        self.speedy = int(base_speed * speed_multiplier * difficulty_multiplier)

    def update(self):
        self.rect.y += self.speedy
        # Kill if it goes off screen
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, text, size, color, x, y):
        super().__init__()
        self.font = pygame.font.SysFont("comicsansms", size, bold=True)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = -2
        self.timer = 0
        self.max_duration = 60 # frames

    def update(self):
        self.rect.y += self.speedy
        self.timer += 1
        if self.timer > self.max_duration:
            self.kill()
