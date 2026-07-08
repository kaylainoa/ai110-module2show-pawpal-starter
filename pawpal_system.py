"""Logic layer for PawPal+.

Implements the four classes from diagrams/uml.mmd: Task, Pet, Owner, Scheduler.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, datetime, time as dtime, timedelta
from typing import Optional

PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}
DAY_START = dtime(8, 0)
RECURRENCE_INTERVAL = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


@dataclass
class Task:
    id: str
    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    category: str  # e.g. "walk", "feeding", "meds", "enrichment", "grooming"
    time: str = "09:00"  # preferred/scheduled time of day, "HH:MM" 24-hour zero-padded
    frequency: str = "once"  # "once" | "daily" | "weekly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    pet_name: Optional[str] = None  # set automatically by Pet.add_task

    def mark_complete(self) -> None:
        """Flip this task's completed flag to True."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return a new Task for the next due date if this task recurs, else None."""
        interval = RECURRENCE_INTERVAL.get(self.frequency)
        if interval is None:
            return None
        next_due = date.today() + interval
        return replace(self, id=f"{self.id}-{next_due.isoformat()}", due_date=next_due, completed=False)


@dataclass
class Pet:
    name: str
    species: str
    breed: Optional[str] = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet, tagging it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove the task with the given id from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def mark_task_complete(self, task_id: str) -> None:
        """Complete a task by id, auto-scheduling its next occurrence if it recurs."""
        for task in self.tasks:
            if task.id == task_id:
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task is not None:
                    self.add_task(next_task)
                return


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)
    preferences: dict = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Return the pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def all_tasks(self) -> list[Task]:
        """Return tasks across every pet, for building a combined daily plan."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    """Retrieves, organizes, and orders tasks into a daily plan."""

    def build_plan(
        self, tasks: list[Task], available_minutes: int
    ) -> list[tuple[str, Task]]:
        """Select and order tasks by priority/duration to fit the time budget, assigning start times."""
        sorted_tasks = sorted(
            (t for t in tasks if not t.completed),
            key=lambda t: (PRIORITY_RANK.get(t.priority, len(PRIORITY_RANK)), t.duration_minutes),
        )

        selected: list[Task] = []
        remaining = available_minutes
        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                selected.append(task)
                remaining -= task.duration_minutes

        plan: list[tuple[str, Task]] = []
        current = datetime.combine(datetime.today(), DAY_START)
        for task in selected:
            plan.append((current.strftime("%H:%M"), task))
            current += timedelta(minutes=task.duration_minutes)
        return plan

    def explain_plan(self, plan: list[tuple[str, Task]]) -> str:
        """Render a plan as a human-readable 'Today's Schedule' string."""
        lines = ["Today's Schedule:"]
        for start_time, task in plan:
            pet_label = f" for {task.pet_name}" if task.pet_name else ""
            lines.append(
                f"  {start_time} — {task.title} ({task.duration_minutes} min) "
                f"[priority: {task.priority}]{pet_label}"
            )
        return "\n".join(lines)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered chronologically by their HH:MM time field."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(
        self,
        tasks: list[Task],
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> list[Task]:
        """Return tasks matching the given pet name and/or completion status."""
        filtered = tasks
        if pet_name is not None:
            filtered = [t for t in filtered if t.pet_name == pet_name]
        if completed is not None:
            filtered = [t for t in filtered if t.completed == completed]
        return filtered

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return a warning string for each set of tasks scheduled at the same time (never raises)."""
        by_time: dict[str, list[Task]] = {}
        for task in tasks:
            if task.completed:
                continue
            by_time.setdefault(task.time, []).append(task)

        warnings: list[str] = []
        for time_str, group in by_time.items():
            if len(group) > 1:
                names = ", ".join(f"{t.title} ({t.pet_name})" for t in group)
                warnings.append(f"Conflict at {time_str}: {names}")
        return warnings
