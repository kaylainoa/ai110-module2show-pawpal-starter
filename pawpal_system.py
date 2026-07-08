"""Logic layer for PawPal+.

Implements the four classes from diagrams/uml.mmd: Task, Pet, Owner, Scheduler.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from typing import Optional

PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}
DAY_START = time(8, 0)


@dataclass
class Task:
    id: str
    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    category: str  # e.g. "walk", "feeding", "meds", "enrichment", "grooming"
    is_recurring: bool = False
    completed: bool = False
    pet_name: Optional[str] = None  # set automatically by Pet.add_task

    def mark_complete(self) -> None:
        """Flip this task's completed flag to True."""
        self.completed = True


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
            tasks,
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
