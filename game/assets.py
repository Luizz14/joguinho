import os
import pygame
from .settings import ASSETS_DIR


def load_image(name: str) -> pygame.Surface:
    """Load an image from assets with alpha."""
    path = os.path.join(ASSETS_DIR, name)
    return pygame.image.load(path).convert_alpha()


def load_scaled(name: str, size: tuple[int, int]) -> pygame.Surface:
    """Load and scale an image."""
    image = load_image(name)
    return pygame.transform.scale(image, size)


def get_font(size: int, bold: bool = True) -> pygame.font.Font:
    """Central font helper to keep styling consistent."""
    return pygame.font.SysFont("comicsansms", size, bold=bold)
