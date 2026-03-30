from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from datetime import date, timedelta


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
    frequency: Optional[str] = None      # "daily" | "weekly" | None
    due_date: Optional[date] = None      # date this task is due

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is 'high'."""
        return self.priority == "high"

    def mark_complete(self) -> Optional[Task]:
        """Mark this task complete and return a new Task for the next occurrence if recurring."""
        self.completed = True

        if self.frequency == "daily":
            next_due = (self.due_date or date.today()) + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due = (self.due_date or date.today()) + timedelta(weeks=1)
        else:
            return None

        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            preferred_time=self.preferred_time,
            start_time=self.start_time,
            completed=False,
            frequency=self.frequency,
            due_date=next_due,
        )


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
        self.tasks.append(task)

    def get_tasks_by_priority(self) -> list[Task]:
        """Return this pet's tasks sorted from high to low priority."""
        order = {"high": 0, "medium": 1, "low": 2}
        return sorted(self.tasks, key=lambda t: order.get(t.priority, 3))

    def mark_task_complete(self, task: Task) -> None:
        """Mark a task complete and automatically add the next occurrence if recurring."""
        next_task = task.mark_complete()
        if next_task is not None:
            self.add_task(next_task)


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
        self.pets.append(pet)

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

    def _start_minutes(self, task: Task) -> Optional[int]:
        """Convert a task's HH:MM start_time to total minutes since midnight."""
        if task.start_time is None:
            return None
        h, m = task.start_time.split(":")
        return int(h) * 60 + int(m)

    def detect_conflicts(self, other_tasks: Optional[list[Task]] = None) -> list[str]:
        """Check for scheduling overlaps and return a list of warning strings.

        Compares tasks within scheduled_tasks and optionally against a second
        list (other_tasks) to support cross-pet conflict detection. Returns
        an empty list if no conflicts are found.
        """
        warnings = []
        all_tasks = self.scheduled_tasks

        # Build a combined list of (task, label) tuples for comparison
        labeled = [(t, self.pet.name) for t in all_tasks]
        if other_tasks:
            labeled += [(t, "other") for t in other_tasks]

        # Compare every pair of tasks exactly once
        for i in range(len(labeled)):
            for j in range(i + 1, len(labeled)):
                task_a, label_a = labeled[i]
                task_b, label_b = labeled[j]

                start_a = self._start_minutes(task_a)
                start_b = self._start_minutes(task_b)

                # Skip tasks with no start_time — nothing to compare
                if start_a is None or start_b is None:
                    continue

                end_a = start_a + task_a.duration_minutes
                end_b = start_b + task_b.duration_minutes

                # Overlap condition: one task starts before the other ends
                if start_a < end_b and start_b < end_a:
                    warnings.append(
                        f"WARNING: '{task_a.title}' ({label_a}, {task_a.start_time}) "
                        f"overlaps with '{task_b.title}' ({label_b}, {task_b.start_time})"
                    )

        return warnings