import pygame
from ..entities.food import Food
from ..settings import SPAWN_RATE, JUNK_RAIN_SPAWN_RATE


class FoodSpawner:
    def __init__(self):
        self.last_spawn = pygame.time.get_ticks()

    def reset(self):
        self.last_spawn = pygame.time.get_ticks()

    def tick(self, now: int, event_state: int, difficulty: float):
        """
        Returns a Food instance when it's time to spawn, otherwise None.
        """
        base_spawn_rate = JUNK_RAIN_SPAWN_RATE if event_state == 2 else SPAWN_RATE
        current_spawn_rate = base_spawn_rate if event_state == 2 else base_spawn_rate / difficulty

        if now - self.last_spawn > current_spawn_rate:
            self.last_spawn = now
            if event_state == 2:
                return Food(force_type="unhealthy", speed_multiplier=1.5, difficulty_multiplier=1.0)
            return Food(difficulty_multiplier=difficulty)
        return None
