from pawpal_system import Owner, Pet, Task, Scheduler


# --- Tasks for Mochi (dog) ---
morning_walk = Task(
    title="Morning Walk",
    duration_minutes=30,
    priority="high",
    preferred_time="morning"
)

feeding = Task(
    title="Feeding",
    duration_minutes=10,
    priority="high",
    preferred_time="morning"
)

bath_time = Task(
    title="Bath Time",
    duration_minutes=20,
    priority="medium",
    preferred_time="afternoon"
)

# --- Tasks for Luna (cat) ---
litter_box = Task(
    title="Clean Litter Box",
    duration_minutes=10,
    priority="high",
    preferred_time="morning"
)

playtime = Task(
    title="Playtime",
    duration_minutes=15,
    priority="medium",
    preferred_time="evening"
)

grooming = Task(
    title="Grooming",
    duration_minutes=20,
    priority="low",
    preferred_time="afternoon"
)


# --- Pets ---
mochi = Pet(name="Mochi", species="dog", age=3)
mochi.add_task(morning_walk)
mochi.add_task(feeding)
mochi.add_task(bath_time)

luna = Pet(name="Luna", species="cat", age=5)
luna.add_task(litter_box)
luna.add_task(playtime)
luna.add_task(grooming)


# --- Owner ---
jordan = Owner(
    name="Jordan",
    email="jordan@email.com",
    available_minutes=90
)
jordan.add_pet(mochi)
jordan.add_pet(luna)


# --- Build and print schedules ---
print("=" * 40)
print("        PAWPAL+ TODAY'S SCHEDULE")
print("=" * 40)

for pet in jordan.pets:
    scheduler = Scheduler(owner=jordan, pet=pet)
    scheduler.build_schedule()

    print(f"\n--- {pet.name} ({pet.species}) ---")
    print(scheduler.explain_plan())

print("=" * 40)