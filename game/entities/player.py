import pygame
from .. import assets
from ..settings import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    PLAYER_WIDTH,
    GROUND_HEIGHT,
    JUMP_POWER,
    GRAVITY,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = assets.load_scaled("Boneco_Gordinho_A1.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - GROUND_HEIGHT + 20  # Slight overlap for perspective
        self.speed = PLAYER_SPEED

        # Jump physics
        self.velocity_y = 0
        self.is_jumping = False
        self.jump_power = JUMP_POWER
        self.gravity = GRAVITY
        self.ground_y = SCREEN_HEIGHT - GROUND_HEIGHT + 20  # Store ground position

    def update(self):
        self._handle_input()
        self._apply_gravity()
        self._clamp_horizontal()
        self._handle_ground_collision()

    def _handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def _clamp_horizontal(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def _apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

    def _handle_ground_collision(self):
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        """Trigger a jump if on ground."""
        if not self.is_jumping:
            self.velocity_y = self.jump_power
            self.is_jumping = True
