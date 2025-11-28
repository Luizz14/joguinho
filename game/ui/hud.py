import pygame
from ..assets import get_font
from ..settings import (
    HEALTH_BAR_HEIGHT,
    HEALTH_BAR_WIDTH,
    PLAYER_MAX_HEALTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    BLACK,
    GREEN,
    YELLOW,
    RED,
    WHITE,
)


class HUD:
    def __init__(self):
        self.font_cache = {}

    def draw(self, screen, score, health, time_left, event_state, warning_time_left=None, event_time_left=None):
        self._draw_score(screen, score)
        self._draw_timer(screen, time_left)
        self._draw_health_bar(screen, health)
        self._draw_event_overlay(screen, event_state, warning_time_left, event_time_left)

    def _get_font(self, size):
        if size not in self.font_cache:
            self.font_cache[size] = get_font(size)
        return self.font_cache[size]

    def _draw_shadow_text(self, surface, text, size, color, x, y):
        font = self._get_font(size)
        text_surface_shadow = font.render(text, True, BLACK)
        text_rect_shadow = text_surface_shadow.get_rect()
        text_rect_shadow.midtop = (x + 2, y + 2)
        surface.blit(text_surface_shadow, text_rect_shadow)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def _draw_score(self, screen, score):
        self._draw_shadow_text(screen, f"Pontuação: {score}", 30, WHITE, SCREEN_WIDTH / 2, 15)

    def _draw_timer(self, screen, time_left):
        self._draw_shadow_text(screen, f"Tempo: {int(time_left)}", 30, WHITE, SCREEN_WIDTH - 100, 15)

    def _draw_health_bar(self, screen, health):
        x = 10
        y = 10

        pygame.draw.rect(screen, (50, 50, 50), (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))

        health_percentage = health / PLAYER_MAX_HEALTH
        if health_percentage > 0.6:
            health_color = GREEN
        elif health_percentage > 0.3:
            health_color = YELLOW
        else:
            health_color = RED

        current_bar_width = int(health_percentage * HEALTH_BAR_WIDTH)
        if current_bar_width > 0:
            pygame.draw.rect(screen, health_color, (x, y, current_bar_width, HEALTH_BAR_HEIGHT))

        pygame.draw.rect(screen, BLACK, (x, y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT), 2)

    def _draw_event_overlay(self, screen, event_state, warning_time_left, event_time_left):
        if event_state == 1:  # WARNING
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(80)
            overlay.fill(RED)
            screen.blit(overlay, (0, 0))
            self._draw_shadow_text(screen, "JUNK FOOD RAIN INCOMING!", 48, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            if warning_time_left is not None:
                self._draw_shadow_text(
                    screen,
                    f"{warning_time_left:.1f}s",
                    36,
                    YELLOW,
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT / 2,
                )
        elif event_state == 2:  # ACTIVE
            pygame.draw.rect(screen, RED, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)
            if event_time_left is not None:
                self._draw_shadow_text(
                    screen,
                    f"DODGE! {event_time_left:.1f}s",
                    40,
                    RED,
                    SCREEN_WIDTH / 2,
                    60,
                )
