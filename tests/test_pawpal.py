from pawpal_system import Pet, Task


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
