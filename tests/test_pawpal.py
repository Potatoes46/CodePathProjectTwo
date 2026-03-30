from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


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


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Jordan", email="jordan@email.com", available_minutes=120)
    pet = Pet(name="Mochi", species="dog", age=3)

    t1 = Task(title="Evening Walk",  duration_minutes=20, priority="low",    start_time="18:00")
    t2 = Task(title="Morning Walk",  duration_minutes=30, priority="high",   start_time="07:00")
    t3 = Task(title="Afternoon Nap", duration_minutes=15, priority="medium", start_time="13:30")

    scheduler = Scheduler(owner=owner, pet=pet)
    scheduler.scheduled_tasks = [t1, t2, t3]  # added out of order intentionally

    sorted_tasks = scheduler.sort_by_time()
    times = [t.start_time for t in sorted_tasks]
    assert times == ["07:00", "13:30", "18:00"], f"Unexpected order: {times}"
    print("PASSED: sort_by_time() correctly returns tasks in chronological order.")


def test_daily_task_creates_next_occurrence():
    today = date.today()
    task = Task(
        title="Feeding",
        duration_minutes=10,
        priority="high",
        frequency="daily",
        due_date=today
    )

    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(task)
    assert len(pet.tasks) == 1

    pet.mark_task_complete(task)
    assert len(pet.tasks) == 2

    next_task = pet.tasks[1]
    assert next_task.completed == False
    assert next_task.due_date == today + timedelta(days=1)
    print("PASSED: completing a daily task correctly creates a new task for the next day.")


def test_detect_conflicts_flags_overlapping_tasks():
    owner = Owner(name="Jordan", email="jordan@email.com", available_minutes=120)
    pet = Pet(name="Mochi", species="dog", age=3)

    t1 = Task(title="Morning Walk", duration_minutes=30, priority="high",   start_time="07:00")
    t2 = Task(title="Feeding",      duration_minutes=10, priority="high",   start_time="07:15")  # overlaps t1
    t3 = Task(title="Bath Time",    duration_minutes=20, priority="medium", start_time="14:00")  # no overlap

    scheduler = Scheduler(owner=owner, pet=pet)
    scheduler.scheduled_tasks = [t1, t2, t3]

    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1, f"Expected 1 conflict, got {len(warnings)}"
    assert "Morning Walk" in warnings[0]
    assert "Feeding" in warnings[0]
    print("PASSED: detect_conflicts() correctly flags overlapping tasks.")


if __name__ == "__main__":
    test_mark_complete()
    test_add_task_increases_count()
    test_sort_by_time_returns_chronological_order()
    test_daily_task_creates_next_occurrence()
    test_detect_conflicts_flags_overlapping_tasks()