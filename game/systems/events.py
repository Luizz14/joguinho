import pygame
from ..settings import (
    EVENT_SCORE_THRESHOLDS,
    JUNK_RAIN_WARNING_TIME,
    JUNK_RAIN_DURATION,
    JUNK_RAIN_MAX_HITS,
)


class EventSystem:
    NORMAL = 0
    WARNING = 1
    ACTIVE = 2

    def __init__(self):
        self.state = self.NORMAL
        self.event_timer = 0
        self.triggered_events: list[int] = []
        self.foods_hit_during_event = 0

    def reset(self):
        self.state = self.NORMAL
        self.event_timer = 0
        self.triggered_events = []
        self.foods_hit_during_event = 0

    def register_unhealthy_hit(self):
        if self.state == self.ACTIVE:
            self.foods_hit_during_event += 1

    def update(self, now: int, score: int):
        """
        Update the state machine.
        Returns a list of actions that occurred this tick for the caller to handle.
        """
        actions: list[tuple[str, object]] = []

        if self.state == self.NORMAL:
            if self._should_trigger(score):
                self._start_warning(now)
                actions.append(("warning_started", None))

        elif self.state == self.WARNING:
            if now - self.event_timer >= JUNK_RAIN_WARNING_TIME:
                self._start_active(now)
                actions.append(("event_started", None))

        elif self.state == self.ACTIVE:
            if now - self.event_timer >= JUNK_RAIN_DURATION:
                survived = self.foods_hit_during_event <= JUNK_RAIN_MAX_HITS
                self._end_active()
                actions.append(("event_ended", survived))

        return actions

    def _should_trigger(self, score: int) -> bool:
        for threshold in EVENT_SCORE_THRESHOLDS:
            if score >= threshold and threshold not in self.triggered_events:
                self.triggered_events.append(threshold)
                return True
        return False

    def _start_warning(self, now: int):
        self.state = self.WARNING
        self.event_timer = now

    def _start_active(self, now: int):
        self.state = self.ACTIVE
        self.event_timer = now
        self.foods_hit_during_event = 0

    def _end_active(self):
        self.state = self.NORMAL
        self.event_timer = 0
        self.foods_hit_during_event = 0

    def time_since_event(self, now: int) -> int:
        if self.state in (self.WARNING, self.ACTIVE):
            return now - self.event_timer
        return 0
