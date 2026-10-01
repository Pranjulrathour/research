# Chapter 12 — Judgment: how to make and document a design decision

Eleven chapters of principles, measurements and trade-offs reduce, in practice, to a sequence of decisions made by a person under uncertainty with incomplete information and a deadline. This chapter is about that person's method: how to turn a vague request into requirements, how to choose among designs that are each correct for some requirements and wrong for others, how to write the decision down so that it can be understood and revisited, and how the whole discipline compresses into the forty-five minutes of a system-design interview, which is not a different skill but the same one with a clock.

## The principle

**A design is an argument from requirements to trade-offs. State the requirements as numbers, enumerate the options honestly, choose with reasons, write down what you gave up and what would change your mind, and measure after you build.**

## Requirements before architecture

The most common design failure is not a wrong choice between two architectures. It is choosing an architecture before knowing what it has to do. Every chapter in this book has turned on a quantity that must be known before the design can be judged, and the first job is to extract those quantities from the people who want the system, who usually have not thought about them in those terms.

The questions, in the order they usually matter:

**What does it do, for whom, and what must never happen?** The functional core, stated in a few sentences, plus the invariants: no double charge, no lost order, no data shown to the wrong user. The invariants are what chapters 5 and 6 are about, and they decide more of the design than the features do.

**How much, how fast, how often?** Request rate at peak and average, data volume now and in two years, read-to-write ratio, the size of a typical and a large payload. Chapter 10's Little's law needs these numbers; without them, "it scales" means nothing.

**How fast must it feel?** The latency budget (chapter 1), as a percentile and a target: p99 under 300 ms for the interactive path. Then the decomposition: how much of the budget is left after the network and the client, and how is the remainder divided among the stages.

**How available, and what does unavailability cost?** The SLO (chapter 9), as a number with a window, and the business cost of being below it, which decides how much redundancy is worth paying for (chapter 7, chapter 11).

**What may be stale, and for how long?** The consistency requirement (chapter 5), per kind of data. The balance cannot be stale; the recommendation can be a day old. Most systems have both kinds and treat them the same, at the cost of the wrong one.

**What is the budget?** Money per month and engineering time to build and run it (chapter 11). A design that exceeds either is not a design.

**What is already there?** Existing systems, teams, skills, contracts, the data's current home. The best design that the organisation cannot build or run is worse than the second-best that it can.

The answers will be approximate and some will be refused ("we don't know how many users"). Approximate is fine: an order of magnitude is enough to choose between a single database and a partitioned one. Refused is fine too, if the refusal is written down and the design states the assumption it made instead, so that the assumption can be checked when the number becomes known.

## Choosing: enumerate, then decide

With requirements in hand, the choice among architectures is usually not hard. The work is in making sure the right options are on the table and that the choice is made for stated reasons.

**Enumerate at least two.** The design that came to mind first is a candidate, not a decision. For each major component (storage, communication, caching, deployment) name the serious alternatives and say in one line what each is good at. This is the step that most design documents skip and that most incident reviews wish had not been skipped.

**Match each option to the requirements.** For each alternative, which requirements does it meet easily, which with effort, which not at all? A relational database meets the invariants easily and the write volume with effort; a document store the reverse; the requirements decide.

**Prefer the simplest design that meets the requirements.** Not the most elegant, the most scalable or the most interesting. Every component added is a thing to operate, a place to fail, and a cost in money and attention. The question to ask of each component is "what requirement forces this?", and if none does, remove it. Systems grow components easily and lose them with great difficulty.

**Identify the decision that is hardest to reverse, and spend the time there.** Partition keys (chapter 6), the choice of primary data store, the public API, the consistency model for the core data: these are expensive to change later and deserve the analysis. The choice of web framework or message queue is reversible and deserves a sentence. Allocating design attention in proportion to reversibility is a habit that separates experienced engineers from careful ones.

**Decide, and name the trade-off.** Every design gives something up. A design document that claims no downside is either wrong or incomplete. The sentence "we chose X, which gives us A and B, at the cost of C, which we accept because D" is the core of every good design decision, and if it cannot be written, the decision is not yet understood.

## Writing it down: the architecture decision record

The artefact that holds a design decision is short and has a standard shape, usually called an *architecture decision record* (ADR).[^1] One page, or less, per significant decision, kept with the code, never edited after the fact (a new decision supersedes an old one, and both remain).

- **Title and date.** What was decided, when.
- **Context.** The requirements and constraints that bear on this decision, with the numbers. What forced a choice.
- **Options considered.** Each in a line or two, with what it would have been good at.
- **Decision.** What was chosen.
- **Consequences.** What this makes easy, what it makes hard, what it costs, what it commits the team to. The trade-off sentence lives here.
- **What would change our mind.** The condition under which this decision should be revisited: a traffic level, a cost threshold, a requirement that changes. This line is the one most often omitted and the one most valuable two years later.

The ADR does three jobs. It forces the author to have the reasons, because they must be written. It lets a newcomer understand why the system is the way it is without archaeology. And it turns "why did we do this?" from an argument about memory into a reading of the record. A codebase with a dozen ADRs is easier to join, change and defend than one with a hundred pages of architecture documentation that nobody updated.

## Measure after you build

A design is a prediction: these requirements, met this way, at this cost. The last step of the method is to check the prediction. Did the p99 land inside the budget? Is the constraining resource the one the design expected? Is the cost per unit what the ADR estimated? Is the consistency anomaly the design accepted actually rare, or does it happen to every user?

This closes the loop that the book has been describing from its first page. Chapter 1 said latency is measured, not asserted; chapter 10 said capacity is a number with a date; chapter 11 said cost is a metric. The design decision is the hypothesis and the running system is the experiment, and an engineer who checks the result, writes it next to the prediction and updates the next design accordingly is doing engineering in the full sense. One who does not is guessing with confidence.

## The interview as the job, compressed

The system-design interview, which the readers of this book will sit many times, is often treated as a performance with its own rules. It is better treated as the method above, run in forty-five minutes, with the interviewer standing in for the stakeholders, the time limit standing in for the deadline, and the whiteboard standing in for the ADR.

The sequence that works is the one this chapter has given.

**Spend the first ten minutes on requirements.** Ask the questions from the first section, out loud, and write the answers (or the assumptions you make when the interviewer declines to answer) where both of you can see them. Candidates who draw boxes in the first two minutes are drawing a solution to an unknown problem; interviewers notice.

**Do the arithmetic.** Request rate, data volume, in-flight requests from Little's law, storage growth, bandwidth. Rough is fine; the point is to show that the numbers drive the design, and the numbers usually reveal which component is the hard one (the database, the fan-out, the hot key).

**Draw the simplest design that meets the requirements.** Name each component and the requirement that forces it. Then say what you did not add and why.

**Go deep where it is hard.** The interviewer will push on one part; it is the one with the hardest trade-off, and it is where the chapters of this book live: the consistency of the core data, the partition key, the cache invalidation, the failure of a dependency, the queue that grows. Say the trade-off sentence. Say what breaks at ten times the load and what you would change.

**Say what you would measure.** The SLO, the dashboards, the alert, the cost per unit. This is the step most candidates omit and the one that most clearly distinguishes someone who has operated a system from someone who has read about one.

**Manage the clock.** Forty-five minutes divides into roughly ten for requirements, five for arithmetic, ten for the design, fifteen for depth and five for operations and wrap-up. A candidate who runs out of time in the design has spent too long on requirements or drawn too much; the fix is the "simplest design" rule.

None of this is a trick. It is what a senior engineer does in a design review, with the same questions, the same arithmetic and the same trade-off sentences, and an interviewer who has done the job recognises it. The companies this book's readers are aiming at are not looking for a candidate who knows the "correct" architecture for a URL shortener. They are looking for the method, because the method transfers to problems that have no textbook answer, which is all of the real ones.

## Twelve questions to ask of any design

A closing checklist, one question per chapter, to be asked of any system you are designing, reviewing, joining or interviewing about.

1. **What is the latency budget, as a percentile, and where does the time go?** (Latency is a distribution.)
2. **What blocks what, and what happens when the queue is full?** (Concurrency and backpressure.)
3. **What may be stale, for how long, and how does each copy learn of a change?** (Caching.)
4. **Which data structure constrains this, and what does it cost in memory and time at ten times the size?** (Data structures at scale.)
5. **Which consistency guarantee does each kind of data actually get, and is it the one it needs?** (Consistency.)
6. **Who may write, what happens when they disagree, and is every operation safe to repeat?** (Replication, partitioning, idempotency.)
7. **For each dependency: what happens when it fails, when it is slow, and when it returns garbage?** (Failure as the normal case.)
8. **What is asynchronous, why, and who watches the queue depth?** (Queues and streams.)
9. **What is the SLO, how is it measured, and what happens when the budget is spent?** (Observability.)
10. **What is the constraining resource, where is its knee, and when will we reach it?** (Capacity.)
11. **What does this cost per unit of useful work, and where does the money leak?** (Cost.)
12. **What did we give up, and what would change our mind?** (Judgment.)

A design that has an answer to all twelve is a design someone understood. A design that has an answer to none is a drawing. Most are in between, and the questions show where the thinking stopped, which is exactly where the incident will begin.

## Run this yourself

Take a system you know (one you built, one you work on, or one you can read the code of) and write its ADRs retrospectively: five to eight decisions, one page each, in the format above, including the trade-off sentence and the "what would change our mind" line. For each, note whether the decision was made for the reasons you have written or for reasons nobody recorded. Then ask the twelve questions of the system and write down the ones it cannot answer. You will have produced the best onboarding document the system has ever had, a list of its latent incidents, and a demonstration of the only skill this book has really been about: making the trade-off visible, and then measuring whether you were right.

---

[^1]: Nygard, M. (2011), "Documenting Architecture Decisions", cognitect.com, November 2011 — the original proposal of the ADR format.

### Sources for this chapter
- Nygard (2011) — architecture decision records.
- Brooks, F. P. (1975; anniversary ed. 1995), *The Mythical Man-Month*, Addison-Wesley — on conceptual integrity and the cost of complexity.
- Lampson, B. W. (1983), "Hints for Computer System Design", *SOSP 1983* — the classic list; most of this book's principles have an ancestor in it.
- Hamilton, J. (2007), "On Designing and Deploying Internet-Scale Services", *LISA 2007* — operational design rules from a practitioner, still current.
- Kleppmann (2017), *Designing Data-Intensive Applications*, chapter 12 — "The Future of Data Systems", on choosing by requirements.
- Alex Xu (2020, 2022), *System Design Interview*, volumes 1 and 2 — for the interview format; read for structure, and bring this book's trade-offs to its examples.
