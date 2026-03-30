from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str                        # "low" | "medium" | "high"
    preferred_time: Optional[str] = None # "morning" | "afternoon" | "evening"
    completed: bool = False

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is 'high'."""
        ...

    def mark_complete(self) -> None:
        """Set completed to True."""
        ...


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str                              # "dog" | "cat" | "other"
    age: int
    notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a Task to this pet's task list."""
        ...

    def get_tasks_by_priority(self) -> list[Task]:
        """Return tasks sorted high → medium → low."""
        ...


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

@dataclass
class Owner:
    name: str
    email: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Append a Pet to the owner's pet list."""
        ...

    def get_schedule(self, date: str) -> list[Task]:
        """Return the scheduled task list for a given date string (YYYY-MM-DD)."""
        ...


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self, owner: Owner, pet: Pet) -> None:
        self.owner = owner
        self.pet = pet
        self.total_minutes: int = owner.available_minutes
        self.scheduled_tasks: list[Task] = []

    def build_schedule(self) -> list[Task]:
        """Select and order tasks that fit within the owner's available time.

        Strategy (to implement):
          1. Sort tasks by priority (high first).
          2. Walk the sorted list; add each task if its duration fits in the
             remaining time window.
          3. Store the result in self.scheduled_tasks and return it.
        """
        ...

    def explain_plan(self) -> str:
        """Return a human-readable summary of the schedule.

        For each scheduled task, include:
          - task title and duration
          - why it was chosen (priority level)
          - estimated start time (cumulative offset from a start hour)
        """
        ...

    def filter_by_priority(self, level: str) -> list[Task]:
        """Return only the tasks whose priority matches the given level."""
        ...

    def fits_in_window(self, task: Task) -> bool:
        """Return True if task.duration_minutes <= remaining available time."""
        ...