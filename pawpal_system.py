"""Logic layer for PawPal+.

Class skeletons generated from diagrams/uml.mmd. Attributes and method
signatures only — scheduling logic is implemented in later phases.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    id: str
    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    category: str  # e.g. "walk", "feeding", "meds", "enrichment", "grooming"
    is_recurring: bool = False
    completed: bool = False

    def mark_complete(self) -> None:
        raise NotImplementedError


@dataclass
class Pet:
    name: str
    species: str
    breed: Optional[str] = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def remove_task(self, task_id: str) -> None:
        raise NotImplementedError


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)
    preferences: dict = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def get_pet(self, name: str) -> Optional[Pet]:
        raise NotImplementedError


class Scheduler:
    def __init__(self, available_minutes: int):
        self.available_minutes = available_minutes

    def build_plan(self, pet: Pet, available_minutes: int) -> list[Task]:
        raise NotImplementedError

    def explain_plan(self, plan: list[Task]) -> str:
        raise NotImplementedError
