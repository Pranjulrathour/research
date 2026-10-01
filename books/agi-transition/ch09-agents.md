# Chapter 9 — Agents: when software starts acting

For the first two years of the current wave, the dominant interface to AI was a text box. You typed, it answered, you decided what to do with the answer. Whatever the system got wrong, a human stood between the output and the world.

That is changing. The systems now being deployed read your email and draft replies, browse websites and fill forms, write code and run it, call other software and act on the results, and chain dozens of such steps together toward a goal you stated once. The industry calls these *agents*, a word that has been used loosely enough to mean almost anything; this chapter uses it to mean a system that takes actions in the world, with some autonomy, over multiple steps, toward a goal. The defining shift is from *answering* to *acting*, and it changes what matters.

When a system only answers, the question is how good the answer is. When it acts, the questions are how often it fails, how badly a failure hurts, whether failures can be caught before they land, and who is responsible when they are not. Intelligence, in the sense of the benchmark scores chapter 2 discussed, turns out to be the easy part. Reliability is the hard part, and reliability, not capability, is what gates deployment.

## What an agent is, mechanically

Strip away the marketing and an agent is a loop. The model receives a goal and a description of the tools it may use (search, read a file, send a message, call an API, run code). It decides on a step, the step is executed, the result comes back as text, and the model decides the next step. The loop ends when the model declares the goal met, or a budget runs out, or a person stops it.

Three design choices define any particular agent.

**What tools it has.** A system that can only read is a research assistant. A system that can write to files, send messages or spend money is something else, and the difference is not in the model but in the permissions. Chapter 8's security argument follows directly: an agent's potential for harm is bounded by its tools, not by its intelligence.

**How much it does before checking in.** At one extreme the system proposes each step and waits for approval; at the other it runs for hours unattended. Everything useful lives in between, and the right point depends on how reversible the actions are and how costly a mistake is.

**How it knows when it is done, or stuck.** The weakest part of most agents in 2026 is self-assessment: knowing that a step failed, that the goal has drifted, that the same loop has been tried three times. Humans are poor at this too, but humans notice they are confused. Systems often do not, and they report success with the same fluency whether or not they succeeded.

None of this requires a particularly capable model. Agents built on 2023-era models worked, badly. The improvement since has come from models that follow long instructions more reliably, from better tool interfaces, and from the accumulated craft of the people building the loops: when to summarise, when to retry, what to log, how to recover. That craft, not the models, is where most of the engineering work of the next few years sits, and it is learnable.

## The arithmetic of reliability

Here is the fact that governs everything else in this chapter. If each step in a chain succeeds independently with probability *p*, a chain of *n* steps succeeds with probability *p^n*. A system that gets each step right 95 per cent of the time, which sounds good, completes a ten-step task correctly about 60 per cent of the time, and a twenty-step task about 36 per cent of the time. At 99 per cent per step, twenty steps succeed about 82 per cent of the time; at 99.9 per cent, about 98 per cent.

Three things follow.

**Per-step reliability matters far more than per-step brilliance.** A less capable system that is right 99 per cent of the time is worth more, for multi-step work, than a more capable one that is right 95 per cent of the time. This is the opposite of how benchmarks rank systems and it is why benchmark leaders are not always deployment leaders.

**Checkpoints change the arithmetic.** If a person, or a verifier, catches failures at step five and step ten, the chain is three chains of five, and a failure costs five steps of rework instead of twenty. Nearly all of the practical art of building agents is deciding where to put the checkpoints: after irreversible actions, before expensive ones, whenever the system's confidence drops.

**Independence is the generous assumption.** Failures in practice are correlated: a misunderstanding at step two corrupts steps three through twenty. Real completion rates for long unattended tasks are often worse than the arithmetic suggests, which is why, in 2026, the tasks agents do reliably are still mostly short, and the long ones are supervised.

Measurements of this are now public. Evaluation suites built around realistic multi-step tasks (software engineering tasks drawn from real repositories, web tasks on real sites, computer-use tasks on real applications) report completion rates that have risen steeply year on year and remain well short of what a competent person achieves without supervision on the harder tasks.[^1] One useful way of tracking progress, proposed in 2025, is to measure the length of task, in human-time, that a system can complete with a given success rate; by that measure the horizon roughly doubled every several months through the mid-2020s.[^2] If that trend holds, tasks that take a person a day become feasible for agents at a useful reliability within the decade; if it bends, they do not. It is the single most important number to watch in this chapter's domain, and chapter 12 lists it among the things this book might be wrong about.

## When delegation is worth it

A simple model makes the decision clear. Suppose a task takes a person *T* minutes, an agent completes it correctly with probability *p*, checking the agent's work takes *c* minutes, and when the agent fails the cost (rework, damage, cleanup) is *F* minutes-equivalent. Delegation is worth it when

> *c* + (1 − *p*) × *F* < *T*.

The equation is trivial and its implications are not.

**Cheap-to-check tasks are the first to go.** If verifying is much faster than doing (a draft you can skim, code with tests, a calculation you can spot-check), even a mediocre agent pays. Writing first drafts, generating test cases, triaging tickets, summarising documents, producing boilerplate: these were the first tasks delegated at scale, and the reason is the small *c*.

**Expensive-to-fail tasks are the last.** If a failure is costly or irreversible (sending the wrong thing to a customer, deleting data, moving money, giving medical advice), *F* dominates, and no realistic *p* makes unattended delegation sensible. These tasks get agents with a human approving each consequential step, which caps the saving at the difference between doing and approving.

**The middle is where judgment lives.** Tasks where checking is almost as hard as doing (a long analysis you would have to re-derive to verify, a design decision whose quality only shows later) are the hard case, and they are the tasks where "the agent did it" is least informative. The honest response is to delegate the parts that can be checked and keep the parts that cannot.

A 95-per-cent-reliable agent is thus enormously valuable for some tasks and worthless for others, and the difference is not in the agent. It is in *c* and *F*. People who understand their own work well enough to see those two numbers for each task will get more from the tools than people who ask "can the AI do this?", which is the wrong question.

## Oversight, permissions and the shape of trust

The institutions around agents are forming now, and they are forming around a few patterns that will look obvious in hindsight.

**Graduated autonomy.** New agents, like new employees, start with narrow permissions and tight supervision and earn more as they demonstrate reliability on logged work. The engineering version of this is a permission system that is specific (this agent may read these files and send mail to these addresses), revocable, and tied to a record of what the agent has done. Blanket permissions granted at the start of a session are the pattern to avoid, for the security reasons chapter 8 gave and the reliability reasons this chapter gives.

**Human approval for irreversible actions.** Send, pay, delete, publish, deploy, sign. Each gets a specific confirmation, and the confirmation shows the person exactly what will happen. This is slow by design and it is how aviation, surgery and finance already work: checklists and read-backs for the steps that cannot be undone.

**Budgets and kill switches.** Every agent run has a limit (time, money, actions) beyond which it stops and asks, and a way for a person to stop it at any point. The absence of either is a design flaw, not a feature.

**Logs as the unit of accountability.** When something goes wrong, the question is what the agent read, what it decided and what it did, in order. Systems that cannot answer are systems that cannot be improved, insured or defended in a dispute, and the liability questions chapter 7 raised will be settled largely by whether such logs exist.

These patterns are not exotic. They are the controls that any organisation applies to a person who can act on its behalf, applied to software that can. The gap in 2026 is that many agent deployments skipped them, because the people deploying had the mental model of a chatbot (what harm can a text box do?) rather than of an employee with system access. The incidents that followed, from deleted databases to leaked data to runaway spending, were predictable and will keep happening until the mental model catches up.

## What it means for work, and for you

Agents are the mechanism through which the economics of chapter 3 reaches the workplace. Displacement happens task by task as agents become reliable enough on each; augmentation happens as people delegate the cheap-to-check parts and keep the judgment; new tasks appear in building, supervising, evaluating and repairing agents.

That last category deserves attention from anyone planning a career. Someone has to decide what tools an agent gets, write the permission rules, design the checkpoints, build the evaluation suites, read the logs when things go wrong, and fix the loop. In 2026 this is a new discipline with no settled name (it borrows from software engineering, from site reliability engineering, from security, and from the management of people), and it is where a large share of the interesting technical hiring is. It rewards exactly the skills this book has argued are durable: measurement (chapter 2), systems thinking (chapter 6), security habits (chapter 8), and the judgment to see *c* and *F* for a task.

It also rewards something older. The person who delegates well to an agent is the person who could have done the task themselves and knows what good looks like. Delegation without competence is abdication, and it produces work nobody checked. The reason to learn the fundamentals in a world of agents is not that you will do the work by hand; it is that you will be the one who can tell when the agent did it wrong.

## What would make this chapter wrong

If by 2031 agents routinely complete day-long or week-long tasks unattended at reliability comparable to a competent professional, then the "reliability gates deployment" framing will have been a description of the late 2020s rather than of the decade, and the arithmetic section understated how fast per-step reliability could improve. Check the measured task-horizon trend and the completion rates on the hardest realistic suites.

If a major incident (a large financial loss, a safety failure, a data breach) traceable to an unsupervised agent has produced strict regulation of agent autonomy, then the oversight patterns described here arrived by law rather than by craft, faster and more rigidly than this chapter expects.

If the agent paradigm has stalled, with multi-step reliability plateauing and most useful deployment remaining single-step and supervised, then the chapter was too optimistic about the trend, and the delegation equation's *p* stayed lower than the industry hoped.

## What to do this year

Run an agent on a real task with a budget and a kill switch, and write down where it failed. Choose something that matters a little but not a lot: organising a set of files, drafting replies you will review before sending, writing and running tests for a small project. Give it the narrowest permissions that allow the task. Set a limit on time or actions. Watch the log. When it finishes, or stops, write one page: what it did well, where it went wrong, whether you caught the failure before it landed, and what checkpoint would have caught it earlier. Then estimate *c*, *F* and *p* for the task. You will have learned more about the next decade of work than any amount of reading about it, and you will have the beginnings of the discipline described above, which almost nobody has yet.

---

[^1]: Among the public suites: SWE-bench and its verified subset (software tasks from real repositories; Jimenez et al., 2023, and subsequent leaderboards), WebArena (Zhou et al., 2023), OSWorld (Xie et al., 2024) and GAIA (Mialon et al., 2023). Read each suite's own documentation for its definition of "success" before comparing numbers.
[^2]: Kwa, T. et al. (2025), "Measuring AI Ability to Complete Long Tasks", Model Evaluation and Threat Research (METR), March 2025, with later updates; the headline finding was a doubling time of roughly seven months in the length of tasks (measured by human completion time) that systems complete at 50 per cent reliability.

### Sources for this chapter
- Jimenez, C. E. et al. (2023), "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?", *ICLR 2024*.
- Zhou, S. et al. (2023), "WebArena: A Realistic Web Environment for Building Autonomous Agents".
- Xie, T. et al. (2024), "OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments", *NeurIPS 2024*.
- Mialon, G. et al. (2023), "GAIA: a benchmark for General AI Assistants".
- Kwa et al. (2025), METR, "Measuring AI Ability to Complete Long Tasks".
- Yao, S. et al. (2022), "ReAct: Synergizing Reasoning and Acting in Language Models" — the loop pattern most agents descend from.
- OWASP Top 10 for LLM Applications (2025), entries on excessive agency and prompt injection.
