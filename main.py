"""Manual testing ground for the PawPal+ logic layer.

Run with: python main.py
"""

from pawpal_system import Owner, Pet, Scheduler, Task

owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="cat", breed="Tabby")
biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever")
owner.add_pet(mochi)
owner.add_pet(biscuit)

mochi.add_task(Task(id="t1", title="Feeding", duration_minutes=10, priority="high", category="feeding"))
mochi.add_task(Task(id="t2", title="Litter box cleanup", duration_minutes=15, priority="medium", category="grooming"))
biscuit.add_task(Task(id="t3", title="Morning walk", duration_minutes=30, priority="high", category="walk"))
biscuit.add_task(Task(id="t4", title="Fetch playtime", duration_minutes=20, priority="low", category="enrichment"))

scheduler = Scheduler()
plan = scheduler.build_plan(owner.all_tasks(), available_minutes=60)

print(scheduler.explain_plan(plan))
