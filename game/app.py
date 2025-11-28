import sys
import pygame
from .settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    TITLE,
    SKY_BLUE,
    GREEN,
    RED,
    YELLOW,
    BLACK,
    GAME_DURATION,
    PLAYER_MAX_HEALTH,
    SCORE_HEALTHY,
    SCORE_UNHEALTHY,
    HEAL_HEALTHY,
    DAMAGE_UNHEALTHY,
    DAMAGE_UNHEALTHY_EVENT,
    JUNK_RAIN_SURVIVAL_BONUS,
    JUNK_RAIN_WARNING_TIME,
    JUNK_RAIN_DURATION,
    GROUND_HEIGHT,
    DIFFICULTY_MIN_MULTIPLIER,
    DIFFICULTY_MAX_MULTIPLIER,
)
from .assets import load_image, get_font
from .entities.player import Player
from .entities.floating_text import FloatingText
from .systems.events import EventSystem
from .systems.spawner import FoodSpawner
from .ui.hud import HUD


class GameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.hud = HUD()
        self.event_system = EventSystem()
        self.spawner = FoodSpawner()

        # Ground tiling
        self.ground_image = load_image("Terreno_01.png")
        self.ground_surface = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT))
        ground_width = self.ground_image.get_width()
        for x in range(0, SCREEN_WIDTH, ground_width):
            self.ground_surface.blit(self.ground_image, (x, 0))

    def run(self):
        self.show_start_screen()
        while self.running:
            result = self.play_round()
            if not self.running:
                break
            if result == "victory":
                self.show_victory_screen()
            else:
                self.show_go_screen()
        pygame.quit()
        sys.exit()

    # Scenes
    def show_start_screen(self):
        self.screen.fill(SKY_BLUE)
        self._draw_shadow_text(TITLE, 64, YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self._draw_shadow_text("Setas para mover, ESPAÇO para pular", 30, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 10)
        self._draw_shadow_text("Colete Comida Saudável!", 30, GREEN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40)
        self._draw_shadow_text("Evite Comida Lixo!", 30, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80)
        self._draw_shadow_text("Pressione uma tecla para jogar", 24, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()
        self._wait_for_key()

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BLACK)
        self._draw_shadow_text("GAME OVER", 64, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self._draw_shadow_text(f"Pontuação: {self.score}", 30, YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self._draw_shadow_text("Pressione uma tecla para jogar novamente", 24, YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()
        self._delay_input()
        self._wait_for_key()

    def show_victory_screen(self):
        if not self.running:
            return
        self.screen.fill(SKY_BLUE)
        self._draw_shadow_text("VITÓRIA!", 72, YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self._draw_shadow_text("Você sobreviveu!", 40, GREEN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 80)
        self._draw_shadow_text(f"Pontuação Final: {self.score}", 32, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self._draw_shadow_text("Pressione uma tecla para jogar novamente", 24, BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()
        self._delay_input()
        self._wait_for_key()

    def play_round(self):
        self.score = 0
        self.health = PLAYER_MAX_HEALTH
        self.victory = False
        self.all_sprites = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

        self.start_time = pygame.time.get_ticks()
        self.event_system.reset()
        self.spawner.reset()
        self.playing = True

        while self.playing and self.running:
            self.clock.tick(FPS)
            self._handle_events()
            self._update_game_state()
            self._draw()
        return "victory" if self.victory else "gameover"

    # Game loop helpers
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def _update_game_state(self):
        self.all_sprites.update()
        self.texts.update()

        now = pygame.time.get_ticks()
        difficulty = self._get_difficulty_multiplier(now)

        # Spawn food
        new_food = self.spawner.tick(now, self.event_system.state, difficulty)
        if new_food:
            self.all_sprites.add(new_food)
            self.foods.add(new_food)

        # Collisions
        hits = pygame.sprite.spritecollide(self.player, self.foods, True)
        for hit in hits:
            if hit.type == "healthy":
                self.score += SCORE_HEALTHY
                old_health = self.health
                self.health = min(PLAYER_MAX_HEALTH, self.health + HEAL_HEALTHY)
                actual_heal = self.health - old_health
                self._spawn_text(f"+{SCORE_HEALTHY}", 30, GREEN, hit.rect.centerx, hit.rect.centery)
                if actual_heal > 0:
                    self._spawn_text(f"+{int(actual_heal)} HP", 24, GREEN, hit.rect.centerx, hit.rect.centery - 30)
            else:
                self.score += SCORE_UNHEALTHY
                damage = DAMAGE_UNHEALTHY_EVENT if self.event_system.state == EventSystem.ACTIVE else DAMAGE_UNHEALTHY
                self.health -= damage
                self._spawn_text(f"{SCORE_UNHEALTHY}", 30, RED, hit.rect.centerx, hit.rect.centery)
                self._spawn_text(f"-{damage} HP", 24, RED, hit.rect.centerx, hit.rect.centery - 30)
                self.event_system.register_unhealthy_hit()

        # Update event machine
        actions = self.event_system.update(now, self.score)
        for action, payload in actions:
            if action == "event_ended" and payload:
                self.score += JUNK_RAIN_SURVIVAL_BONUS
                self._spawn_text(f"+{JUNK_RAIN_SURVIVAL_BONUS} SURVIVED!", 35, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

        # Win/Lose
        elapsed_time = (now - self.start_time) / 1000
        if self.health <= 0:
            self.victory = False
            self.playing = False
        elif elapsed_time >= GAME_DURATION:
            self.victory = True
            self.playing = False

    def _draw(self):
        self.screen.fill(SKY_BLUE)
        self.screen.blit(self.ground_surface, (0, SCREEN_HEIGHT - GROUND_HEIGHT))
        self.all_sprites.draw(self.screen)
        self.texts.draw(self.screen)

        now = pygame.time.get_ticks()
        elapsed_time = (now - self.start_time) / 1000
        time_left = max(0, GAME_DURATION - elapsed_time)

        warning_left = None
        event_left = None
        if self.event_system.state == EventSystem.WARNING:
            warning_left = max(0, (JUNK_RAIN_WARNING_TIME - (now - self.event_system.event_timer)) / 1000)
        elif self.event_system.state == EventSystem.ACTIVE:
            event_left = max(0, (JUNK_RAIN_DURATION - (now - self.event_system.event_timer)) / 1000)

        self.hud.draw(
            self.screen,
            self.score,
            self.health,
            time_left,
            self.event_system.state,
            warning_left,
            event_left,
        )

        pygame.display.flip()

    # Utilities
    def _draw_shadow_text(self, text, size, color, x, y):
        font = get_font(size)
        text_surface_shadow = font.render(text, True, BLACK)
        text_rect_shadow = text_surface_shadow.get_rect()
        text_rect_shadow.midtop = (x + 2, y + 2)
        self.screen.blit(text_surface_shadow, text_rect_shadow)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def _wait_for_key(self):
        waiting = True
        while waiting and self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def _delay_input(self, duration=1500):
        delay_start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - delay_start < duration and self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
        pygame.event.clear()

    def _spawn_text(self, text, size, color, x, y):
        floating = FloatingText(text, size, color, x, y)
        self.all_sprites.add(floating)
        self.texts.add(floating)

    def _get_difficulty_multiplier(self, now: int) -> float:
        elapsed_time = (now - self.start_time) / 1000
        progress = min(1.0, elapsed_time / GAME_DURATION)
        return DIFFICULTY_MIN_MULTIPLIER + (progress * (DIFFICULTY_MAX_MULTIPLIER - DIFFICULTY_MIN_MULTIPLIER))
