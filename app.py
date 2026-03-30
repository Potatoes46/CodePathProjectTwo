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
    start_time: Optional[str] = None     # "HH:MM" format, e.g. "08:30"
    completed: bool = False

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is 'high'."""
        ...

    def mark_complete(self) -> None:
        """Set the task's completed status to True."""
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
        """Append the given Task to this pet's task list."""
        ...

    def get_tasks_by_priority(self) -> list[Task]:
        """Return this pet's tasks sorted from high to low priority."""
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
        """Append the given Pet to this owner's pet list."""
        ...

    def get_schedule(self, date: str) -> list[Task]:
        """Return the list of scheduled tasks for the given date string."""
        ...


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self, owner: Owner, pet: Pet) -> None:
        """Initialize the Scheduler with an Owner, a Pet, and an empty task list."""
        self.owner = owner
        self.pet = pet
        self.total_minutes: int = owner.available_minutes
        self.scheduled_tasks: list[Task] = []

    def build_schedule(self) -> list[Task]:
        """Sort tasks by priority and greedily select those that fit in the available time window."""
        ...

    def explain_plan(self) -> str:
        """Return a human-readable summary of each scheduled task with its start time and priority."""
        ...

    def filter_by_priority(self, level: str) -> list[Task]:
        """Return only the scheduled tasks whose priority matches the given level."""
        ...

    def fits_in_window(self, task: Task) -> bool:
        """Return True if the task's duration fits within the remaining available time."""
        ...

    def sort_by_time(self) -> list[Task]:
        """Return scheduled tasks sorted chronologically by their start_time in HH:MM format."""
        return sorted(
            [t for t in self.scheduled_tasks if t.start_time is not None],
            key=lambda t: tuple(int(x) for x in t.start_time.split(":"))
        )

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None
    ) -> list[Task]:
        """Return scheduled tasks filtered by completion status and/or pet name."""
        results = self.scheduled_tasks

        if completed is not None:
            results = [t for t in results if t.completed == completed]

        if pet_name is not None:
            results = [t for t in results if self.pet.name.lower() == pet_name.lower()]

        return results