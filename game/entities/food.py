import random
import pygame
from .. import assets
from ..settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FOOD_SIZE,
    FOOD_MIN_SPEED,
    FOOD_MAX_SPEED,
    JUNK_RAIN_FOOD_MIN_SPEED,
    JUNK_RAIN_FOOD_MAX_SPEED,
)


class Food(pygame.sprite.Sprite):
    def __init__(self, force_type=None, speed_multiplier=1.0, difficulty_multiplier=1.0):
        super().__init__()

        # Use forced type if provided, otherwise random
        self.type = force_type if force_type else random.choice(["healthy", "unhealthy"])

        if self.type == "healthy":
            filename = random.choice(["Alface.png", "Banana.png", "Maçã.png", "Pêra.png"])
        else:
            filename = random.choice(["Chocolate.png", "Hamburguer.png", "Refrigerante.png", "Sorvete.png"])

        self.image = assets.load_scaled(filename, (FOOD_SIZE, FOOD_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - FOOD_SIZE)
        self.rect.y = random.randrange(-100, -40)

        if force_type == "unhealthy" and speed_multiplier > 1.0:
            base_speed = random.randrange(JUNK_RAIN_FOOD_MIN_SPEED, JUNK_RAIN_FOOD_MAX_SPEED)
        else:
            base_speed = random.randrange(FOOD_MIN_SPEED, FOOD_MAX_SPEED)

        self.speedy = int(base_speed * speed_multiplier * difficulty_multiplier)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()
