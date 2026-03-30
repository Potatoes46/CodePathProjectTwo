# PawPal+ Project Reflection

## 1. System Design

The user should be able to generate a schedule, add tasks, and add pets and their owners as associated value types.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
My initial UML design includes the four classes of "task", "pet", "owner", and "scheduler". Task is just a single care activity like a walk or feeding and holds info like duration, priority, and preferred time. Pet stores a specific animal's profile and its list of tasks and can sort them by priority when needed. Owner holds the human's info and most importantly how much time they have available in the day. Scheduler is the main class that takes an Owner and Pet and figures out which tasks fit in the available time and explains the resulting plan. The relationships are pretty straightforward where Owner has one or more Pets, Pet has zero or more Tasks, and Scheduler reads from both Owner and Pet to build the schedule without either of them knowing it exists.
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, my design definitely changed during implementation. One change I made was 
One change I made was adding the frequency and due_date fields to the Task class so that recurring tasks like daily walks or weekly grooming sessions could automatically reschedule themselves after being completed. Before that change, marking a task complete just set a flag and that was it, which meant you would have to manually re-add the same task every day. By having mark_complete() return a brand new Task with an updated due_date calculated using timedelta, the system handles the repetition for you which felt like a much more realistic way to model pet care.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The scheduler currently considers three main constraints which are time availability, priority, and preferred time of day. Time is the hardest constraint since tasks simply cannot be scheduled if they exceed the owner's available minutes for the day. Priority acts as the tiebreaker for ordering, with high priority tasks always getting picked first. Preferred time is the softest constraint and is more of a labeling preference than something that strictly blocks scheduling. Priority ended up mattering most because in a pet care context missing a high priority task like feeding is a bigger deal than missing a low priority one like grooming, so it made sense to let that drive the selection order.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
The Scheduler class does a solid job of keeping all the scheduling logic in one place, which makes it easy to find and change without touching Pet or Owner. That said, there are some real tradeoffs worth noting. The greedy approach in build_schedule() is simple and fast but it can produce a suboptimal schedule since it just picks tasks in priority order without ever backtracking to see if a different combination would actually fit more work into the time window. The conflict detection in detect_conflicts() also runs in O(n²) time since it compares every pair of tasks, which is totally fine for a pet care app with a handful of tasks but would slow down noticeably if the task list ever got large. Another tradeoff is that Scheduler is built around a single pet at a time, so doing cross-pet conflict detection requires manually passing in the other pet's tasks as an argument rather than the scheduler just knowing about all pets from the start. Overall the design prioritizes simplicity and readability over raw power, which is probably the right call for a project at this scale.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
AI tools were super helpful throughout this project in a few different ways. At the start I used Claude to help brainstorm the class structure and generate the initial UML diagram, which saved a lot of time that would have gone into figuring out how the classes should relate to each other. From there I would paste my current file and ask for specific additions like the conflict detection logic, the recurring task system, or the docstrings, and Claude would return a modified version I could copy straight into my IDE. The most helpful prompts were ones where I gave the full file as context and described exactly what I wanted added and why, since vague prompts tended to produce more generic answers. I also used it to generate test cases and write README descriptions which was honestly really useful for the more writing-heavy parts of the project that are easy to put off.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
One moment where I didn't just accept the AI suggestion as-is was when the conflict detection logic was first generated. The method looked correct on the surface but I actually stepped through the overlap condition manually on paper with a couple of example tasks to make sure the math was right before trusting it. Specifically I wanted to verify that the condition start_a < end_b and start_b < end_a actually caught all overlap cases and didn't miss edge cases like two tasks that share an exact start time or one that ends exactly when another begins. I also added a dedicated test in the test file with a known overlapping pair and a known non-overlapping task to confirm the method returned exactly one warning rather than just assuming it worked. That combination of manual tracing and writing a real test gave me way more confidence in the logic than just reading the generated code and moving on.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
Looking at the test file, five behaviors were tested across the system. The first two were basic sanity checks where one test verified that calling mark_complete() actually flips the task's completed flag to true, and another confirmed that calling add_task() on a pet correctly grows its task list. These felt important to test first since basically everything else in the system depends on those two operations working correctly. The third test checked that sort_by_time() returns tasks in chronological order even when they were added out of order, which mattered because the whole point of that method is to clean up an unsorted schedule for display. The fourth test was probably the most important one since it verified that completing a daily recurring task automatically creates a new task with a due date exactly one day ahead, which is the core of the recurrence feature and would be really hard to catch just by reading the code. The last test confirmed that detect_conflicts() correctly identifies overlapping tasks and returns exactly one warning for one overlap, which was important to verify since a conflict detector that misses conflicts or throws false positives would make the whole warning system useless.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
Honestly the confidence level is somewhere around a 3 out of 5 right now. The parts that are implemented and tested like sorting, conflict detection, recurring tasks, and filtering all behave correctly based on the tests written. The bigger issue is that build_schedule(), explain_plan(), filter_by_priority(), and fits_in_window() are still stubs, so the core scheduling loop has not actually been verified at all yet which is a pretty significant gap. If there was more time the edge cases worth testing next would be things like what happens when the available minutes is zero or less, whether the scheduler handles a task whose duration is longer than the entire time budget, what sort_by_time() does when no tasks have a start time set, whether conflict detection behaves correctly when two tasks share an exact start time versus one ending exactly when another begins, and how the recurrence logic handles a task with no due date set. Those boundary conditions are usually where bugs hide and right now none of them are covered.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The part of the project that is most satisfying is probably the recurring task system. It felt like the most complete and well thought out feature since it touches multiple classes working together, where Task.mark_complete() handles the date math using timedelta and returns a fresh task instance, and then Pet.mark_task_complete() catches that return value and automatically appends it to the pet's task list without the caller having to do anything extra. It also has a dedicated test that actually verifies the next due date is exactly one day ahead rather than just checking that a new task exists, which makes it one of the more trustworthy parts of the codebase. Compared to some of the other methods that are still stubs, the recurrence feature feels genuinely finished and does something non-trivial in a clean way that matches how the system was designed from the start.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If there was another iteration the biggest thing to fix would be filling in the remaining stubs since build_schedule(), explain_plan(), filter_by_priority(), and fits_in_window() all still have ... in them which means the core scheduling loop has never actually run. Beyond that the greedy priority based approach in build_schedule() would be worth reconsidering since it can miss better combinations of tasks that would fit more work into the available time window, and a smarter algorithm like dynamic programming or even just trying multiple orderings would produce more optimal schedules. Another thing worth redesigning is how Scheduler only handles one pet at a time, since right now cross-pet conflict detection requires manually passing the other pet's task list in as an argument rather than the scheduler just being aware of all pets from the start. It would also be nice to add input validation on things like the HH:MM format for start times and the priority string values since right now the system just trusts that the inputs are correct which would cause confusing crashes in a real app.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important thing learned from this project is that AI is really good at generating structure and boilerplate but it still needs a human to verify that the logic actually makes sense for the specific problem. For example Claude could generate a conflict detection algorithm or a recurring task system pretty quickly, but without manually tracing through the overlap condition or writing a test to confirm the due date math, there would be no real way to know if it was correct or just looked correct. That gap between code that looks reasonable and code that actually works is something AI cannot close on its own, which made it clear that the most effective way to use it on this project was as a fast starting point rather than a final answer. The prompting process also taught a lot about how to communicate technical requirements clearly since vague prompts produced generic results and the more specific the file context and the description of what was needed, the more useful the output was.