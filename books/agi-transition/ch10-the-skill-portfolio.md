# Chapter 10 — The personal skill portfolio for 2026–2036

Everything in this book so far has been about the world. This chapter is about you, and it is the one most readers will have skipped ahead to, so it is written to stand alone. Where it leans on earlier chapters it says so.

The question people actually ask is "what should I learn so that I am not replaced?" It is the wrong question, in the same way that "is it AGI yet?" was the wrong question in chapter 1, and for the same reason: it asks for a binary answer about a thing that is a distribution. Nobody is replaced; tasks are. Nobody is safe; some skills compound with the tools and some are substituted by them. The useful question is "which of my skills get *more* valuable as the tools improve, and how do I prove I have them?"

This chapter gives a framework for that question, a one-page plan, and the uncomfortable list of what to stop doing.

## The wrong frame: "AI skills"

In 2024 and 2025 the labour market filled with demands for "AI skills", and courses to sell them. Most of what was sold was knowledge of specific products: how to write prompts for a particular model, how to use a particular tool, how to wire a particular API. There is nothing wrong with learning those things, and they are the wrong thing to build a career on, for three reasons.

They depreciate on the product's schedule, not yours. Everything specific to a tool from 2024 is already partly obsolete; everything specific to a tool from 2026 will be partly obsolete by 2028. Chapter 3 explained why: the capability frontier moves, and the interfaces move with it.

They are the skills the tools themselves make cheap. "Prompting" was a skill when models were brittle; as models got better at understanding ordinary instructions, the premium fell. The same will happen to every skill that consists of working around a system's current limitations.

They do not differentiate you. If a skill can be learned from a two-hour course, everyone competing with you has learned it, and it carries no signal.

The right frame is *skills that compound with AI*: things that become more valuable as the tools get better, because the tools amplify them rather than substitute for them. There are, as far as anyone can tell in 2026, three layers of these.

## Three layers that compound

### Layer one: judgment

Judgment is the set of skills that decide *what* to do and *whether it was done right*, and it includes three things that recur throughout this book.

**Problem framing.** Turning a vague situation into a well-posed question. What are we actually trying to achieve? What would count as success? What are the constraints nobody mentioned? The tools are superb at answering well-posed questions and poor at posing them, and a person who can frame a problem clearly multiplies the value of everything downstream. This is the oldest skill in engineering and consulting, and it is now the scarcest.

**Verification.** Knowing whether an output is correct, and knowing *how you know*. Chapter 2 made the case that reading an evaluation is a civic skill; for a professional, being able to check work (yours, a colleague's, a machine's) is the skill that turns cheap output into reliable output. It depends on fundamentals: you cannot verify code without understanding what it should do, or a statistical claim without understanding what the number means, or a system design without knowing where systems break. Verification is why the fundamentals matter more in a world of fluent tools, not less.

**Taste.** The harder-to-name ability to tell good from merely acceptable: a design that will age well, an analysis that asks the right question, writing that says one thing clearly. Taste is built by exposure to excellent work and by making a great deal of work yourself and seeing what holds up. It cannot be downloaded and it is what distinguishes the person whose output people seek from the person whose output is interchangeable with a machine's.

### Layer two: systems

Systems thinking is understanding how parts fit together, where the bottlenecks are, how failures propagate, and what breaks at scale. Chapter 6 argued that this is where engineering value has migrated as production gets cheaper; chapter 9 showed that the discipline of building and supervising agents is largely a systems discipline.

For a technical reader this means the unglamorous core of computer science and engineering: how data moves, what latency and throughput mean and where they come from, how to reason about consistency and failure, how to measure before and after a change, how components hide and expose faults. It is the subject of this book's companion volume and of the second half of any good computer-science degree. The point here is strategic: a person who can hold a whole system in their head is amplified by tools that can build any individual part, because the scarce step becomes deciding what the parts should be and whether they work together.

For a non-technical reader the same layer exists in a different vocabulary: how an organisation actually works, where its information flows, who decides what, what fails when the volume triples. The person who understands the system is the one who can direct the tools at the right problem.

### Layer three: domain depth

The third layer is knowing a field deeply: finance, health, law, agriculture, logistics, energy, education, public administration, a scientific discipline. General-purpose tools are, by construction, shallow in every domain; the value is created where someone who understands a field well enough to know what matters directs the tools at it.

This is the layer most undervalued by computing students, who tend to treat the domain as a detail and the technology as the point. For the next decade it is the other way round. Chapter 5 said it for students and chapter 11 says it for India: the gap between what the tools can do and what any particular field needs is where careers are, and it is filled by people who understand both sides. Pick a domain early, learn it seriously (its vocabulary, its data, its regulations, its failure modes, its people), and your technical skills become ten times more valuable because they are pointed at something.

The three layers reinforce one another. Judgment without systems knowledge is opinion; systems knowledge without a domain is abstraction; a domain without judgment is expertise that cannot adapt. A portfolio has all three, in proportions that depend on who you are.

## What to stop learning

This is the part people dislike, and it is the part that saves the most time.

**Stop learning to do by hand what you will never do by hand.** Memorising syntax, standard algorithm implementations, boilerplate patterns, formulaic writing. You must *understand* these things, well enough to verify them (layer one). You do not need to be fast at producing them, because you will not be the one producing them. The difference between understanding and fluent production is the difference between an hour of study and a hundred hours of drill, and the hundred hours are now better spent elsewhere.

**Stop collecting tool certifications as if they were skills.** One or two, for the tools you use daily, as evidence of competence. Beyond that they signal that you confused the tool for the work.

**Stop optimising for the entry-level task.** Chapter 4 showed that the tasks which used to train juniors are the first automated. Preparing exhaustively to do those tasks prepares you for a rung that is narrowing. Prepare instead to be useful *above* that rung earlier than previous generations had to be, which means layers one and two from the start.

**Stop treating breadth as a goal.** Knowing a little about many frameworks, languages and tools was a reasonable strategy when each had to be learned to be used. Now the tools will learn the tool for you. Depth in a few things you can verify and a domain you understand beats a long list of things you have touched.

## Proving it: the portfolio of verifiable work

A skill nobody can see is a skill the market cannot price. The second half of a personal strategy is proof, and chapter 5 named the form proof now takes: a portfolio of *verifiable* work, meaning work that other people have used, tested, built on, cited or checked, as opposed to work that merely exists.

The distinction matters because existence is now free. A repository of generated code, a blog of generated articles, a certificate from a generated course: none of these demonstrates anything, and recruiters know it. What demonstrates something is contact with the world.

**Work that runs.** A system that people other than you actually use, with the problems that implies: real data, real failures, real users who complain. Even a small one.

**Work that is checked.** An analysis with its code and data published, that someone else could reproduce (chapter 6). A result that holds up when a sceptic looks at it. A measurement rather than a claim.

**Work that others accepted.** A contribution to a project you do not control, reviewed by people who did not have to accept it. A talk at an event whose organisers chose you. A paper or a note that passed someone's screening.

**Work that explains.** Writing that teaches something true to people who did not know it, under your name, in a place where they can find it. Explanation is a test of understanding that generated text fails in a way that is visible to anyone who knows the subject, and it is the fastest way to be found by the people who are looking for someone who understands.

One piece of verifiable work per quarter, sustained for the years of a degree or an early career, puts a person ahead of almost everyone, because almost nobody does it. The compounding is real: each piece makes the next easier, the body of work becomes a reputation, and the reputation becomes the thing that chapter 8 said rises in value when everything else is free: a signed, verified, accountable identity.

## The one-page plan

Write this on one page. Revisit it every quarter.

1. **Domain.** The field I am going deep in, and why. One or two sentences. If you cannot write them, that is the first task.

2. **Judgment skills I am building this year.** Pick two from framing, verification, taste, and name the practice: what you will do weekly that builds them. Verification is the one to start with if unsure; it is the most learnable and the most immediately valuable.

3. **Systems knowledge I am building this year.** The specific fundamentals (for a technical reader: the two or three topics from the core curriculum you understand least well; for others: the two or three mechanisms of your organisation or field you cannot yet explain).

4. **What I am stopping.** Name it. The drill you will stop, the certification you will not pursue, the breadth you will trade for depth.

5. **This quarter's verifiable work.** One piece. What it is, who will use or check it, where it will live under your name, and the date.

6. **How I use the tools.** A rule for yourself about delegation (chapter 9's *c*, *F* and *p*): what you delegate freely, what you delegate and check, what you do yourself because doing it is how you learn.

7. **What would change this plan.** One or two developments that would make you revise it (a capability jump in your domain, a change in how your target employers hire) and how you will notice them.

The plan is deliberately short because long plans are not followed. It is deliberately specific because vague plans cannot be checked, and the whole argument of this book is that checkable beats plausible.

## A note on the entry-level reader

If you are a student or in your first job, the chapter above may read as advice for someone further along, so here is the version for you.

You are entering a market in which the easiest tasks are being automated and the hardest ones still need people, and in which the traditional path (do the easy tasks for a few years, learn by doing them, graduate to the hard ones) is narrowing. That is a real disadvantage and it is not your fault.

It is also an opening. The firms that have cut their junior hiring have not stopped needing people who can do the harder work; they have stopped believing that a degree alone proves someone can. A student who arrives with a verifiable portfolio (one system that runs, one analysis that reproduces, one contribution that was accepted, one explanation that taught somebody) is not competing with the narrowed entry rung. They are competing for the rung above it, and there are far fewer such candidates than there are places.

The fundamentals, the domain, the quarterly piece of real work and the habit of verifying before trusting: these are not the safe path. They are the only path that was ever reliable, made visible by a technology that removed the alternatives.

## What would make this chapter wrong

If by 2031 the tools have become so capable that judgment, systems thinking and domain depth are themselves substituted at scale, the three-layer framework will have described a shrinking island rather than durable ground. Check whether experienced professionals in judgment-heavy roles (senior engineers, physicians, lawyers, analysts) are seeing wage and employment declines comparable to those of entry-level roles.

If the credential has reasserted itself, with employers reverting to degree and brand as the main filters because portfolios became too easy to fake, then the verifiable-work argument underestimated how quickly proof could be counterfeited. Check what the large employers' hiring processes actually weight.

If "AI skills" in the narrow, product-specific sense have turned out to carry a durable premium, then the first section was too dismissive. Check wage data for roles defined by tool proficiency rather than domain or judgment.

## What to do this year

Publish one piece of verifiable work per quarter, starting this quarter. Four pieces, under your name, each of which someone else can run, reproduce, check or learn from. Keep them small enough to finish. Write the one-page plan above before you start the first, and revise it after the fourth. At the end of the year you will have a portfolio that most people with twice your experience do not have, and a clear view of which of your skills the tools amplified and which they replaced, which is the only career information that matters for the decade ahead.

---

### Sources for this chapter
- Autor, D. (2024), "Applying AI to Rebuild Middle Class Jobs", NBER Working Paper 32140 — the argument that AI can extend expertise to more workers, and its conditions.
- Brynjolfsson, E., Li, D. & Raymond, L. (2025), "Generative AI at Work", *Quarterly Journal of Economics* 140(2) — who gains most from assistance (less-experienced workers) and why that matters for the entry rung.
- Dell'Acqua, F. et al. (2023), "Navigating the Jagged Technological Frontier", Harvard Business School Working Paper 24-013 — the uneven capability frontier and the risk of over-trusting output.
- Chapters 2, 4, 5, 6, 8 and 9 of this book for the evidence behind each layer.
- Ericsson, K. A. & Pool, R. (2016), *Peak* — on deliberate practice, for the distinction between understanding and fluent production.
