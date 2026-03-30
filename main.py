from pawpal_system import Owner, Pet, Task, Scheduler


# --- Tasks for Mochi (dog) ---
morning_walk = Task(
    title="Morning Walk",
    duration_minutes=30,
    priority="high",
    preferred_time="morning",
    start_time="07:00"
)

bath_time = Task(
    title="Bath Time",
    duration_minutes=20,
    priority="medium",
    preferred_time="afternoon",
    start_time="14:00"
)

feeding = Task(
    title="Feeding",
    duration_minutes=10,
    priority="high",
    preferred_time="morning",
    start_time="07:15"  # intentional conflict: overlaps with Morning Walk (07:00 - 07:30)
)

# --- Tasks for Luna (cat) ---
playtime = Task(
    title="Playtime",
    duration_minutes=15,
    priority="medium",
    preferred_time="evening",
    start_time="18:00"
)

litter_box = Task(
    title="Clean Litter Box",
    duration_minutes=10,
    priority="high",
    preferred_time="morning",
    start_time="07:30"
)

grooming = Task(
    title="Grooming",
    duration_minutes=20,
    priority="low",
    preferred_time="afternoon",
    start_time="14:10"  # intentional cross-pet conflict: overlaps with Mochi's Bath Time (14:00 - 14:20)
)


# --- Pets (tasks added out of order intentionally) ---
mochi = Pet(name="Mochi", species="dog", age=3)
mochi.add_task(bath_time)      # afternoon task added first
mochi.add_task(morning_walk)   # morning task added second
mochi.add_task(feeding)        # morning task added last (conflicts with morning_walk)

luna = Pet(name="Luna", species="cat", age=5)
luna.add_task(playtime)        # evening task added first
luna.add_task(grooming)        # afternoon task added second (conflicts cross-pet with bath_time)
luna.add_task(litter_box)      # morning task added last


# --- Owner ---
jordan = Owner(
    name="Jordan",
    email="jordan@email.com",
    available_minutes=90
)
jordan.add_pet(mochi)
jordan.add_pet(luna)


# --- Build schedulers ---
scheduler_mochi = Scheduler(owner=jordan, pet=mochi)
scheduler_mochi.build_schedule()

scheduler_luna = Scheduler(owner=jordan, pet=luna)
scheduler_luna.build_schedule()


# --- Print schedules ---
print("=" * 40)
print("        PAWPAL+ TODAY'S SCHEDULE")
print("=" * 40)

for pet, scheduler in [(mochi, scheduler_mochi), (luna, scheduler_luna)]:
    print(f"\n--- {pet.name} ({pet.species}) ---")
    print("Unsorted order:")
    for t in scheduler.scheduled_tasks:
        print(f"  {t.start_time} - {t.title}")

    print("Sorted by time:")
    for t in scheduler.sort_by_time():
        print(f"  {t.start_time} - {t.title}")

    print(scheduler.explain_plan())

# --- Conflict detection ---
print("\n" + "=" * 40)
print("         CONFLICT DETECTION")
print("=" * 40)

print("\nMochi (same-pet conflicts):")
mochi_conflicts = scheduler_mochi.detect_conflicts()
if mochi_conflicts:
    for w in mochi_conflicts:
        print(f"  {w}")
else:
    print("  No conflicts found.")

print("\nMochi vs Luna (cross-pet conflicts):")
cross_conflicts = scheduler_mochi.detect_conflicts(other_tasks=scheduler_luna.scheduled_tasks)
if cross_conflicts:
    for w in cross_conflicts:
        print(f"  {w}")
else:
    print("  No conflicts found.")

print("=" * 40)