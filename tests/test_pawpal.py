from pawpal_system import Task, Pet


def test_mark_complete():
    task = Task(title="Morning Walk", duration_minutes=30, priority="high")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True
    print("PASSED: mark_complete() correctly updates task status.")


def test_add_task_increases_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    assert len(pet.tasks) == 1
    pet.add_task(Task(title="Bath Time", duration_minutes=20, priority="medium"))
    assert len(pet.tasks) == 2
    print("PASSED: add_task() correctly increases pet task count.")


if __name__ == "__main__":
    test_mark_complete()
    test_add_task_increases_count()