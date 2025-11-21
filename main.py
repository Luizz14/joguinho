import pygame
import sys
import os
from settings import *
from sprites import Player, Food, FloatingText

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font('comicsansms')
        self.start_time = 0

        # Load Ground
        self.ground_image = pygame.image.load(os.path.join(ASSETS_DIR, 'Terreno_01.png')).convert_alpha()
        # Tile the ground
        self.ground_surface = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT))
        ground_width = self.ground_image.get_width()
        for x in range(0, SCREEN_WIDTH, ground_width):
            self.ground_surface.blit(self.ground_image, (x, 0))

        # Event system state (Junk Food Rain)
        self.event_state = 0  # 0=NORMAL, 1=WARNING, 2=ACTIVE
        self.event_timer = 0
        self.triggered_events = []  # Track which score thresholds have triggered
        self.foods_hit_during_event = 0

    def new(self):
        # Start a new game
        self.score = 0
        self.health = PLAYER_MAX_HEALTH
        self.victory = False
        self.all_sprites = pygame.sprite.Group()
        self.foods = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.start_time = pygame.time.get_ticks()

        # Reset event variables
        self.event_state = 0  # NORMAL
        self.event_timer = 0
        self.triggered_events = []
        self.foods_hit_during_event = 0

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        self.last_spawn = pygame.time.get_ticks()
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.texts.update()

        # Update event system
        self.update_event_system()

        # Get current difficulty multiplier
        difficulty = self.get_difficulty_multiplier()

        # Spawning food - use different spawn rate during event
        now = pygame.time.get_ticks()
        base_spawn_rate = JUNK_RAIN_SPAWN_RATE if self.event_state == 2 else SPAWN_RATE

        # Apply difficulty ONLY to normal gameplay (events have fixed difficulty)
        if self.event_state == 2:  # ACTIVE event
            current_spawn_rate = base_spawn_rate  # Fixed rate during events
        else:
            current_spawn_rate = base_spawn_rate / difficulty  # Scaling during normal gameplay

        if now - self.last_spawn > current_spawn_rate:
            self.last_spawn = now

            # During junk rain event, spawn only unhealthy food at higher speed
            # Events have FIXED difficulty (don't scale with time)
            if self.event_state == 2:  # ACTIVE
                food = Food(force_type='unhealthy', speed_multiplier=1.5, difficulty_multiplier=1.0)
            else:
                food = Food(difficulty_multiplier=difficulty)

            self.all_sprites.add(food)
            self.foods.add(food)

        # Collision with food
        hits = pygame.sprite.spritecollide(self.player, self.foods, True)
        for hit in hits:
            if hit.type == 'healthy':
                # Healthy food: heal and add score
                self.score += SCORE_HEALTHY
                old_health = self.health
                self.health = min(PLAYER_MAX_HEALTH, self.health + HEAL_HEALTHY)
                actual_heal = self.health - old_health

                # Show score text
                text = FloatingText(f"+{SCORE_HEALTHY}", 30, GREEN, hit.rect.centerx, hit.rect.centery)
                self.all_sprites.add(text)
                self.texts.add(text)

                # Show heal text if health was restored
                if actual_heal > 0:
                    heal_text = FloatingText(f"+{int(actual_heal)} HP", 24, GREEN,
                                            hit.rect.centerx, hit.rect.centery - 30)
                    self.all_sprites.add(heal_text)
                    self.texts.add(heal_text)
            else:
                # Unhealthy food: damage and subtract score
                self.score += SCORE_UNHEALTHY

                # Determine damage amount based on event state
                damage = DAMAGE_UNHEALTHY_EVENT if self.event_state == 2 else DAMAGE_UNHEALTHY
                self.health -= damage

                # Show score text
                text = FloatingText(f"{SCORE_UNHEALTHY}", 30, RED, hit.rect.centerx, hit.rect.centery)
                self.all_sprites.add(text)
                self.texts.add(text)

                # Show damage text
                damage_text = FloatingText(f"-{damage} HP", 24, RED,
                                          hit.rect.centerx, hit.rect.centery - 30)
                self.all_sprites.add(damage_text)
                self.texts.add(damage_text)

                # Track unhealthy food hits during event
                if self.event_state == 2:  # ACTIVE
                    self.foods_hit_during_event += 1

        # Check Game Over conditions
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        if self.health <= 0:
            self.victory = False
            self.playing = False
        elif elapsed_time >= GAME_DURATION:
            self.victory = True
            self.playing = False

    def events(self):
        # Game Loop - Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(SKY_BLUE)

        # Draw Ground
        self.screen.blit(self.ground_surface, (0, SCREEN_HEIGHT - GROUND_HEIGHT))

        self.all_sprites.draw(self.screen)
        self.texts.draw(self.screen)

        # Draw HUD
        self.draw_text(f"Pontuação: {self.score}", 30, WHITE, SCREEN_WIDTH / 2, 15, shadow=True)

        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        time_left = max(0, GAME_DURATION - elapsed_time)
        self.draw_text(f"Tempo: {int(time_left)}", 30, WHITE, SCREEN_WIDTH - 100, 15, shadow=True)

        # Draw Health Bar
        health_bar_x = 10
        health_bar_y = 10

        # Background (dark gray)
        pygame.draw.rect(self.screen, (50, 50, 50),
                        (health_bar_x, health_bar_y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))

        # Health bar color based on percentage
        health_percentage = self.health / PLAYER_MAX_HEALTH
        if health_percentage > 0.6:
            health_color = GREEN
        elif health_percentage > 0.3:
            health_color = YELLOW
        else:
            health_color = RED

        # Health bar (proportional to current health)
        current_bar_width = int((self.health / PLAYER_MAX_HEALTH) * HEALTH_BAR_WIDTH)
        if current_bar_width > 0:
            pygame.draw.rect(self.screen, health_color,
                           (health_bar_x, health_bar_y, current_bar_width, HEALTH_BAR_HEIGHT))

        # Border (black)
        pygame.draw.rect(self.screen, BLACK,
                        (health_bar_x, health_bar_y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT), 2)

        # Event visuals
        now = pygame.time.get_ticks()

        # Warning phase
        if self.event_state == 1:  # WARNING
            # Flash red warning
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(80)
            overlay.fill(RED)
            self.screen.blit(overlay, (0, 0))

            self.draw_text("JUNK FOOD RAIN INCOMING!", 48, RED,
                          SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, shadow=True)

            warning_time_left = (JUNK_RAIN_WARNING_TIME - (now - self.event_timer)) / 1000
            self.draw_text(f"{warning_time_left:.1f}s", 36, YELLOW,
                          SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shadow=True)

        # Active phase
        elif self.event_state == 2:  # ACTIVE
            # Red border around screen
            pygame.draw.rect(self.screen, RED, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

            # Event timer
            event_time_left = (JUNK_RAIN_DURATION - (now - self.event_timer)) / 1000
            self.draw_text(f"DODGE! {event_time_left:.1f}s", 40, RED,
                          SCREEN_WIDTH / 2, 60, shadow=True)

        pygame.display.flip()

    def get_difficulty_multiplier(self):
        """Calculate difficulty multiplier based on elapsed time (1.0 to 3.0)"""
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        progress = min(1.0, elapsed_time / GAME_DURATION)  # 0.0 to 1.0
        multiplier = DIFFICULTY_MIN_MULTIPLIER + (progress * (DIFFICULTY_MAX_MULTIPLIER - DIFFICULTY_MIN_MULTIPLIER))
        return multiplier

    def check_event_trigger(self):
        """Check if score has crossed a threshold to trigger junk rain event"""
        for threshold in EVENT_SCORE_THRESHOLDS:
            if self.score >= threshold and threshold not in self.triggered_events:
                self.triggered_events.append(threshold)
                self.start_warning()
                break

    def start_warning(self):
        """Start warning phase before junk food rain"""
        self.event_state = 1  # WARNING
        self.event_timer = pygame.time.get_ticks()

    def start_junk_rain(self):
        """Start the junk food rain event"""
        self.event_state = 2  # ACTIVE
        self.event_timer = pygame.time.get_ticks()
        self.foods_hit_during_event = 0

    def end_junk_rain(self):
        """End the junk food rain event and award survival bonus if applicable"""
        # Award survival bonus if player was hit 2 or fewer times
        if self.foods_hit_during_event <= JUNK_RAIN_MAX_HITS:
            self.score += JUNK_RAIN_SURVIVAL_BONUS
            text = FloatingText(f"+{JUNK_RAIN_SURVIVAL_BONUS} SURVIVED!", 35, YELLOW,
                              SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            self.all_sprites.add(text)
            self.texts.add(text)

        self.event_state = 0  # NORMAL
        self.event_timer = 0

    def update_event_system(self):
        """Update the event state machine"""
        now = pygame.time.get_ticks()

        if self.event_state == 0:  # NORMAL
            self.check_event_trigger()

        elif self.event_state == 1:  # WARNING
            if now - self.event_timer >= JUNK_RAIN_WARNING_TIME:
                self.start_junk_rain()

        elif self.event_state == 2:  # ACTIVE
            if now - self.event_timer >= JUNK_RAIN_DURATION:
                self.end_junk_rain()

    def show_start_screen(self):
        self.screen.fill(SKY_BLUE)
        self.draw_text(TITLE, 64, YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, shadow=True)
        self.draw_text("Setas para mover, ESPAÇO para pular", 30, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 10, shadow=True)
        self.draw_text("Colete Comida Saudável!", 30, GREEN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40, shadow=True)
        self.draw_text("Evite Comida Lixo!", 30, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80, shadow=True)
        self.draw_text("Sobreviva à Chuva de Comida Lixo!", 28, YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120, shadow=True)
        self.draw_text("Pressione uma tecla para jogar", 24, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4, shadow=True)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 64, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, shadow=True)
        self.draw_text(f"Final Score: {self.score}", 30, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shadow=True)
        self.draw_text("Press a key to play again", 24, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4, shadow=True)
        pygame.display.flip()

        # Add delay before accepting input (prevents accidental restart)
        delay_start = pygame.time.get_ticks()
        delay_duration = 1500  # 1.5 seconds delay

        # Wait and ignore all input during delay
        while pygame.time.get_ticks() - delay_start < delay_duration:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

        # Clear any remaining events from the queue
        pygame.event.clear()

        # Now wait for intentional key press
        self.wait_for_key()

    def show_victory_screen(self):
        if not self.running:
            return
        self.screen.fill(SKY_BLUE)
        self.draw_text("VITÓRIA!", 72, YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, shadow=True)
        self.draw_text("Você sobreviveu!", 40, GREEN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 80, shadow=True)
        self.draw_text(f"Pontuação Final: {self.score}", 32, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shadow=True)
        self.draw_text("Parabéns!", 36, YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60, shadow=True)
        self.draw_text("Pressione uma tecla para jogar novamente", 24, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4, shadow=True)
        pygame.display.flip()

        # Add delay before accepting input (prevents accidental restart)
        delay_start = pygame.time.get_ticks()
        delay_duration = 1500  # 1.5 seconds delay

        # Wait and ignore all input during delay
        while pygame.time.get_ticks() - delay_start < delay_duration:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

        # Clear any remaining events from the queue
        pygame.event.clear()

        # Now wait for intentional key press
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y, shadow=False):
        font = pygame.font.SysFont("comicsansms", size, bold=True)
        if shadow:
            text_surface_shadow = font.render(text, True, BLACK)
            text_rect_shadow = text_surface_shadow.get_rect()
            text_rect_shadow.midtop = (x + 2, y + 2)
            self.screen.blit(text_surface_shadow, text_rect_shadow)
            
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    if g.victory:
        g.show_victory_screen()
    else:
        g.show_go_screen()

pygame.quit()
