from datetime import date, timedelta

from pawpal_system import Pet, Scheduler, Task


def test_mark_complete_changes_task_status():
    task = Task(id="t1", title="Feeding", duration_minutes=10, priority="high", category="feeding")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="cat")
    assert len(pet.tasks) == 0

    pet.add_task(Task(id="t1", title="Feeding", duration_minutes=10, priority="high", category="feeding"))

    assert len(pet.tasks) == 1


def test_sort_by_time_orders_chronologically():
    scheduler = Scheduler()
    tasks = [
        Task(id="t1", title="Evening walk", duration_minutes=30, priority="high", category="walk", time="18:00"),
        Task(id="t2", title="Feeding", duration_minutes=10, priority="high", category="feeding", time="08:00"),
        Task(id="t3", title="Lunch check", duration_minutes=5, priority="low", category="feeding", time="12:00"),
    ]

    ordered = scheduler.sort_by_time(tasks)

    assert [t.id for t in ordered] == ["t2", "t3", "t1"]


def test_filter_tasks_by_pet_and_completion_status():
    scheduler = Scheduler()
    mochi_task = Task(id="t1", title="Feeding", duration_minutes=10, priority="high", category="feeding")
    mochi_task.pet_name = "Mochi"
    biscuit_task = Task(id="t2", title="Walk", duration_minutes=30, priority="high", category="walk")
    biscuit_task.pet_name = "Biscuit"
    biscuit_task.completed = True
    tasks = [mochi_task, biscuit_task]

    assert scheduler.filter_tasks(tasks, pet_name="Mochi") == [mochi_task]
    assert scheduler.filter_tasks(tasks, completed=True) == [biscuit_task]


def test_mark_task_complete_schedules_next_occurrence_for_daily_task():
    pet = Pet(name="Mochi", species="cat")
    pet.add_task(
        Task(
            id="t1",
            title="Feeding",
            duration_minutes=10,
            priority="high",
            category="feeding",
            frequency="daily",
        )
    )

    pet.mark_task_complete("t1")

    assert len(pet.tasks) == 2
    original, next_task = pet.tasks
    assert original.completed is True
    assert next_task.completed is False
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_mark_task_complete_does_not_recur_for_one_off_task():
    pet = Pet(name="Mochi", species="cat")
    pet.add_task(Task(id="t1", title="Vet visit", duration_minutes=45, priority="high", category="meds"))

    pet.mark_task_complete("t1")

    assert len(pet.tasks) == 1
    assert pet.tasks[0].completed is True


def test_detect_conflicts_flags_same_time_tasks():
    scheduler = Scheduler()
    task_a = Task(id="t1", title="Morning walk", duration_minutes=30, priority="high", category="walk", time="08:00")
    task_a.pet_name = "Biscuit"
    task_b = Task(id="t2", title="Feeding", duration_minutes=10, priority="high", category="feeding", time="08:00")
    task_b.pet_name = "Mochi"

    conflicts = scheduler.detect_conflicts([task_a, task_b])

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_detect_conflicts_ignores_completed_tasks():
    scheduler = Scheduler()
    task_a = Task(id="t1", title="Old feeding", duration_minutes=10, priority="high", category="feeding", time="08:00")
    task_a.completed = True
    task_b = Task(id="t2", title="New feeding", duration_minutes=10, priority="high", category="feeding", time="08:00")

    assert scheduler.detect_conflicts([task_a, task_b]) == []
