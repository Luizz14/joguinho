import pygame
from ..assets import get_font


class FloatingText(pygame.sprite.Sprite):
    def __init__(self, text, size, color, x, y):
        super().__init__()
        self.font = get_font(size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = -2
        self.timer = 0
        self.max_duration = 60  # frames

    def update(self):
        self.rect.y += self.speedy
        self.timer += 1
        if self.timer > self.max_duration:
            self.kill()
