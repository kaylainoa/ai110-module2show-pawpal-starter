# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

A pet owner using PawPal+ should be able to:

1. **Add a pet (and owner profile).** The owner enters their own info once, then adds one or more pets with basic details (name, species, breed) so the app knows who it's planning care for.
2. **Add and manage care tasks for a pet.** For each pet, the owner adds recurring or one-off care tasks like walks, feeding, meds, enrichment, and grooming, specifying at minimum how long the task takes and how important it is (priority).
3. **Generate and view today's plan.** The owner asks PawPal+ to build a schedule for the day. The app picks and orders tasks based on priority and available time, shows the resulting plan with times, and explains why each task got included or ordered the way it did.

**a. Initial design**

My initial UML has four classes:

- **Owner** holds the pet owner's name, their list of `Pet`s, and free-form scheduling preferences. It's responsible for owning/managing pets (`add_pet`, `get_pet`) and doesn't know anything about tasks or scheduling directly.
- **Pet** holds basic identity info (name, species, breed) and its own list of `Task`s. It's responsible for managing which tasks belong to it (`add_task`, `remove_task`).
- **Task** is the smallest unit of work: title, duration, priority, category, whether it recurs, and whether it's done. It's only responsible for its own state (`mark_complete`) and has no knowledge of the pet or owner it belongs to.
- **Scheduler** takes a `Pet` and an available time budget, and turns that pet's task list into an ordered daily plan (`build_plan`) plus a human-readable explanation of the choices (`explain_plan`). I kept it separate from `Pet`/`Task` so the planning logic doesn't leak into simple data-holder classes.

The relationships are Owner 1-to-many Pet, Pet 1-to-many Task, and Scheduler reads from Pet/Task without owning them (a dependency, not composition).

**b. Design changes**

After writing the skeleton, I reviewed `pawpal_system.py` for missing relationships and logic bottlenecks and made two changes:

1. **Removed the duplicated `available_minutes`.** `Scheduler` originally took `available_minutes` in `__init__` and again as a `build_plan` argument, so there were two sources of truth with no clear rule for which one wins. I made `Scheduler` stateless and only pass `available_minutes` as a `build_plan` argument.
2. **Generalized `build_plan` to accept a task list instead of a single `Pet`.** Since I'd already decided an `Owner` can have multiple pets, a `Scheduler` that only accepted one `Pet` had no way to build a combined daily plan across an owner's pets. I changed the signature to `build_plan(tasks: list[Task], available_minutes: int)` and added `Owner.all_tasks()` to gather tasks across all pets, so the same method works for a single pet's plan or a combined household plan.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

`Scheduler.build_plan()` considers two constraints: task **priority** (`high`/`medium`/`low`) and the **available time budget** for the day. It sorts tasks by priority first, then by duration as a tiebreaker (shorter tasks first), and greedily adds tasks while they still fit in the remaining minutes. If a task doesn't fit, it just gets skipped instead of stopping the whole plan.

Separately, `Scheduler.sort_by_time()`, `filter_tasks()`, and `detect_conflicts()` work off each task's own declared `time` (a preferred clock time the owner sets) and `pet_name`/`completed` status, independent of the priority-based plan.

I decided priority and time budget mattered most because those are the two things a busy pet owner actually runs out of during a real day: attention (what's most important if I can only do a few things) and minutes (how much of the day is actually free). Category and recurrence affect what a task is, not whether it gets picked, so I didn't fold them into `build_plan`'s selection logic.

**b. Tradeoffs**

`Scheduler.detect_conflicts()` only flags tasks that share the exact same `time` string (like two tasks both at `"08:00"`). It doesn't check whether one task's duration overlaps into another task's start time, so a 30-minute "Morning walk" at `08:00` and a 10-minute "Feeding" at `08:15` wouldn't get flagged, even though the walk is technically still going when the feeding is supposed to start.

I chose this on purpose. Exact-match comparison is a simple string/dict lookup, no interval math needed, while true overlap detection means sorting tasks by start time and comparing each task's start-to-end window against its neighbors. That's more code and more edge cases (back-to-back tasks, zero-duration tasks, etc.) than I wanted to take on for a starter app. Exact-match conflicts are also the more common real mistake a pet owner would actually make (accidentally double-booking the same time slot), so catching that case covers most of the practical value. It's a reasonable v1 tradeoff, but I know it's a gap: it would miss a genuinely overlapping schedule that doesn't start at the exact same minute.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI across every phase of this project: brainstorming the class breakdown before writing any code, generating the full class implementations from the UML, extending the logic with new algorithms (sorting, filtering, recurrence, conflicts), writing the pytest suite, and wiring everything into the Streamlit UI.

The most effective thing was having it do multi-file edits and then actually verify them instead of just handing me a code snippet. It would edit `pawpal_system.py`, `main.py`, `tests/test_pawpal.py`, and `app.py` together, then run `python main.py`, `pytest`, and even a scripted Streamlit test (adding pets/tasks, triggering a conflict, marking a task complete) after each change instead of just assuming the code worked. That's actually what caught a real bug (see 3b) that a code-only review would have missed.

The most helpful prompts weren't "add feature X," they were open-ended review requests. Asking it to review the skeleton for "missing relationships or logic bottlenecks" is what surfaced two real design problems (a duplicated `available_minutes` source of truth, and a `Scheduler` that couldn't handle more than one pet) before they turned into actual bugs later on.

Keeping each phase in its own step (skeleton, then implementation, then algorithms, then tests, then docs/UI) kept the assistant focused on one thing at a time, which made it a lot easier for me to review each change. A schema change didn't get mixed in with the same review as a UI change.

**b. Judgment and verification**

After implementing recurring tasks and conflict detection, I ran `main.py` and noticed the newly-completed "Feeding" task was still showing up in the generated schedule, and it was even conflicting with its own freshly-created next-day occurrence. Both `build_plan()` and `detect_conflicts()` had been written without excluding completed tasks. The code technically did what I'd asked (sort, filter, recur, detect conflicts), but it was behaviorally wrong the moment I actually ran it with a completed task in the mix. I didn't just accept it: I had both methods updated to skip completed tasks and re-ran the demo to confirm the fix, instead of assuming that passing the original requirements meant the feature was actually done.

Separately, during the "simplify one algorithm" step, I considered rewriting `detect_conflicts()` with `itertools.groupby` to make it look more "Pythonic," but decided against it. `groupby` only groups consecutive items, so it would've needed a pre-sort plus turning each group into a list before using it, which ends up slower and no more readable than the dict-based version I already had. I kept the original.

What I learned about being the "lead architect": AI will confidently produce code that satisfies the literal instructions while missing behavioral edge cases (like what happens to a completed recurring task) that only show up once you actually run the thing. My job wasn't to write every line myself, it was to decide what "correct" actually means for this system and then verify that the implementation holds up in every state, not just the happy path from the instructions.

---

## 4. Testing and Verification

**a. What you tested**

The 14-test suite (`tests/test_pawpal.py`) covers task completion and pet task-count basics, chronological sorting (including an empty list), filtering by pet name and completion status, `build_plan`'s priority-then-duration ordering and its skip-when-time-runs-out behavior (including an empty task list), daily and weekly recurrence plus confirming a one-off task doesn't recur, conflict detection for same-time tasks and completed tasks being excluded and the no-conflict case, and `Owner.all_tasks()` aggregating across multiple pets.

These matter because they're basically the promises the UI is making to the owner. If sorting were wrong, "today's tasks" would look out of order. If conflict detection missed a real double-booking, the owner would trust a schedule that's secretly double-booking a pet. If recurrence silently failed, a "daily" task would just stop showing up after the first time you completed it.

**b. Confidence**

I'd put myself at 4 out of 5 stars. The core logic (sorting, filtering, priority planning, recurrence, and exact-time conflict detection) is well covered and passing, and I also verified the actual Streamlit UI by scripting a full interaction: adding two pets, adding two same-time tasks, confirming the conflict warning shows up, marking a daily task complete, and confirming the success message and the new occurrence appear. So it's not just backend logic I checked, it's the real app flow too.

The known gap, which I wrote about in 2b, is that conflict detection only catches exact `HH:MM` matches, not overlapping durations. If I had more time I'd add interval-overlap conflict tests once that logic exists, a test for `Pet.remove_task`, and a test for what happens if two pets get added with the same name (right now `Owner.get_pet` would silently just return the first match it finds).

---

## 5. Reflection

**a. What went well**

I'm most happy with the build, run, and verify loop I kept up the whole time. Every time I added a new method, I'd run `main.py` or the test suite (and eventually a scripted Streamlit interaction) right away instead of just moving on to the next thing. That loop is exactly what caught the completed-recurring-task bug I described in 3b before it ever made it into the UI.

**b. What you would improve**

I'd want to unify the two different notions of "when" that exist in the system right now. `build_plan()` invents its own start times based on priority and duration, while `sort_by_time()`/`detect_conflicts()` respect each task's own declared `time`. Right now they coexist as a deliberate v1 tradeoff (documented in 2b), but a more polished version would make `build_plan` aware of each task's preferred time so the "smart" plan and the owner's actual clock-time expectations don't end up disagreeing with each other. I'd also want to upgrade conflict detection from exact-time-match to real interval overlap.

**c. Key takeaway**

Working with AI on this project made it pretty clear that the hard part of system design isn't generating classes and methods. AI can do that fast and it's usually competent. The hard part is deciding what the system's actual contracts are (what does "complete" mean for a recurring task, what counts as a "conflict") and then actually verifying, by running the code, that the implementation holds up in every state, not just the happy path the instructions described. Being the "architect" meant owning those decisions and doing the verification myself, not just approving whatever happened to compile.
