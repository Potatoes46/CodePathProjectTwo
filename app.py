import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.divider()

# ---------------------------------------------------------------------------
# Owner + Pet setup
# ---------------------------------------------------------------------------

st.subheader("Owner Info")
owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@email.com")
available_minutes = st.number_input("Available minutes today", min_value=10, max_value=480, value=90)

st.subheader("Pet Info")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=3)

# ---------------------------------------------------------------------------
# Task input
# ---------------------------------------------------------------------------

st.divider()
st.subheader("Add Tasks")
st.caption("Add tasks below. Each task will be added to your pet and fed into the scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    preferred_time = st.selectbox("Preferred time", ["morning", "afternoon", "evening"])
with col5:
    start_time = st.text_input("Start time (HH:MM)", value="07:00")

if st.button("Add task"):
    st.session_state.tasks.append({
        "title": task_title,
        "duration_minutes": int(duration),
        "priority": priority,
        "preferred_time": preferred_time,
        "start_time": start_time
    })

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

# ---------------------------------------------------------------------------
# Generate schedule
# ---------------------------------------------------------------------------

st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Please add at least one task before generating a schedule.")
    else:
        # Build owner and pet from UI inputs
        owner = Owner(
            name=owner_name,
            email=owner_email,
            available_minutes=int(available_minutes)
        )
        pet = Pet(name=pet_name, species=species, age=int(pet_age))

        # Add each task from session state to the pet
        for t in st.session_state.tasks:
            task = Task(
                title=t["title"],
                duration_minutes=t["duration_minutes"],
                priority=t["priority"],
                preferred_time=t["preferred_time"],
                start_time=t["start_time"]
            )
            pet.add_task(task)

        owner.add_pet(pet)

        # Run scheduler
        scheduler = Scheduler(owner=owner, pet=pet)
        scheduler.build_schedule()

        st.success(f"Schedule generated for {pet.name}!")

        # ---------------------------------------------------------------------------
        # Sorted schedule table
        # ---------------------------------------------------------------------------

        st.markdown("### 🗓 Today's Schedule (Sorted by Time)")
        sorted_tasks = scheduler.sort_by_time()

        if sorted_tasks:
            st.table([
                {
                    "Start Time": t.start_time,
                    "Task": t.title,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority.capitalize(),
                    "Preferred Time": t.preferred_time or "—",
                    "Done": "✅" if t.completed else "⬜"
                }
                for t in sorted_tasks
            ])
        else:
            st.info("No tasks with a start time to display. Make sure build_schedule() is implemented.")

        # ---------------------------------------------------------------------------
        # Filter by priority
        # ---------------------------------------------------------------------------

        st.markdown("### 🔍 Filter by Priority")
        col_a, col_b, col_c = st.columns(3)

        for col, level in zip([col_a, col_b, col_c], ["high", "medium", "low"]):
            with col:
                filtered = scheduler.filter_by_priority(level)
                label = level.capitalize()
                if filtered:
                    st.success(f"{label} priority ({len(filtered)} task(s))")
                    for t in filtered:
                        st.markdown(f"- {t.title} ({t.duration_minutes} min)")
                else:
                    st.info(f"No {label.lower()} priority tasks.")

        # ---------------------------------------------------------------------------
        # Conflict detection
        # ---------------------------------------------------------------------------

        st.markdown("### ⚠️ Conflict Detection")
        conflicts = scheduler.detect_conflicts()

        if conflicts:
            for w in conflicts:
                st.warning(w)
        else:
            st.success("No scheduling conflicts found!")