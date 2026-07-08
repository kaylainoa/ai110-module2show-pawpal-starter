import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

# Streamlit reruns this whole script on every interaction, so the Owner instance
# must live in st.session_state or it would be re-created (and emptied) each time.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

st.divider()

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        new_pet_name = st.text_input("Pet name")
    with col2:
        new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    with col3:
        new_pet_breed = st.text_input("Breed (optional)")
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if new_pet_name.strip():
        owner.add_pet(Pet(name=new_pet_name.strip(), species=new_pet_species, breed=new_pet_breed or None))
        st.success(f"Added {new_pet_name}.")
    else:
        st.warning("Enter a pet name before adding.")

if owner.pets:
    st.table(
        [
            {"name": p.name, "species": p.species, "breed": p.breed or "—", "tasks": len(p.tasks)}
            for p in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")
if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        pet_names = [p.name for p in owner.pets]
        selected_pet_name = st.selectbox("Pet", pet_names)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        with col4:
            category = st.text_input("Category", value="walk")
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        pet = owner.get_pet(selected_pet_name)
        task_id = f"t{len(owner.all_tasks()) + 1}"
        pet.add_task(
            Task(
                id=task_id,
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                category=category,
            )
        )
        st.success(f"Added '{task_title}' to {pet.name}.")
else:
    st.info("Add a pet before adding tasks.")

all_tasks = owner.all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": t.pet_name,
                "title": t.title,
                "duration_minutes": t.duration_minutes,
                "priority": t.priority,
                "category": t.category,
            }
            for t in all_tasks
        ]
    )
else:
    st.info("No tasks yet.")

st.divider()

st.subheader("Build Schedule")
available_minutes = st.number_input("Time available today (minutes)", min_value=1, max_value=600, value=60)

if st.button("Generate schedule"):
    if not all_tasks:
        st.warning("Add at least one task first.")
    else:
        plan = scheduler.build_plan(all_tasks, int(available_minutes))
        st.text(scheduler.explain_plan(plan))
