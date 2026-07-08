"""Manual testing ground for the PawPal+ logic layer.

Run with: python main.py
"""

from pawpal_system import Owner, Pet, Scheduler, Task

owner = Owner(name="Jordan")

mochi = Pet(name="Mochi", species="cat", breed="Tabby")
biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever")
owner.add_pet(mochi)
owner.add_pet(biscuit)

# Added deliberately out of chronological order to exercise sort_by_time().
biscuit.add_task(
    Task(id="t1", title="Evening walk", duration_minutes=30, priority="high", category="walk", time="18:00")
)
mochi.add_task(
    Task(
        id="t2",
        title="Feeding",
        duration_minutes=10,
        priority="high",
        category="feeding",
        time="08:00",
        frequency="daily",
    )
)
biscuit.add_task(
    Task(id="t3", title="Morning walk", duration_minutes=30, priority="high", category="walk", time="08:00")
)
mochi.add_task(
    Task(id="t4", title="Litter box cleanup", duration_minutes=15, priority="medium", category="grooming", time="12:00")
)
biscuit.add_task(
    Task(id="t5", title="Fetch playtime", duration_minutes=20, priority="low", category="enrichment", time="17:00")
)

scheduler = Scheduler()

print("=== Sorted by time ===")
for task in scheduler.sort_by_time(owner.all_tasks()):
    print(f"  {task.time} — {task.title} ({task.pet_name})")

print()
print("=== Filtered: Mochi's incomplete tasks ===")
for task in scheduler.filter_tasks(owner.all_tasks(), pet_name="Mochi", completed=False):
    print(f"  {task.time} — {task.title}")

print()
print("=== Recurring task: completing Mochi's daily feeding (t2) ===")
mochi.mark_task_complete("t2")
for task in mochi.tasks:
    status = "done" if task.completed else "pending"
    print(f"  {task.id}: {task.title} ({status}), due {task.due_date}")

print()
print("=== Conflict detection ===")
biscuit.add_task(
    Task(id="t6", title="Vet check-in call", duration_minutes=15, priority="medium", category="admin", time="08:00")
)
conflicts = scheduler.detect_conflicts(owner.all_tasks())
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts found.")

print()
plan = scheduler.build_plan(owner.all_tasks(), available_minutes=60)
print(scheduler.explain_plan(plan))
