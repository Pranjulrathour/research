# Chapter 1 — What "general" means, and why the word matters

In the spring of 2023, a system that had been trained to predict the next word in a sentence passed a simulated bar exam, wrote working code in a dozen languages, explained jokes, and failed to count the letters in a short word. All four of those things were true at once, and all four were widely reported, and the reports almost never appeared together. People who saw the bar exam concluded that general intelligence had arrived. People who saw the letter-counting concluded the whole thing was a party trick. Both groups were reasoning from one data point about a question that needs a map.

This chapter is about the map. Before you can think clearly about what the next decade of artificial intelligence will do to work, learning, institutions and your own plans, you need a way to say *what a system can do* that is more precise than "it is smart" and more useful than a benchmark score. You need to be able to say which tasks, at what reliability, with how much autonomy, and compared with whom. Once you can say that, most of the loudest arguments about AI turn out to be arguments between people describing different parts of the same animal.

## The word is doing too much work

"Artificial general intelligence" is a phrase that carries at least four different meanings, and the people using it rarely say which one they mean.

The first meaning is **breadth**: a system that can do many kinds of task rather than one. A chess engine is narrow. A system that can draft an email, debug a program and summarise a court judgment is broader, whatever its quality on each.

The second is **human parity**: a system that performs a task as well as a typical person, or as well as an expert. This is a statement about level, not about breadth, and it is always relative to a reference population that should be named and usually is not.

The third is **autonomy**: a system that can carry out a long task, choose its own intermediate steps, recover from errors and finish without a person checking each move. A model that writes an excellent paragraph when asked is not autonomous. A system that is given a goal on Monday and reports results on Friday is, whether or not its paragraphs are excellent.

The fourth meaning is **economic**: a system that can do most economically valuable work. This is the definition in several AI companies' charters, and it is the one that matters most for the subject of this book, because it is a claim about labour markets rather than about cognition. It is also the hardest to measure, since "most economically valuable work" is not a benchmark anyone can run.

When someone says a system "is" or "is not" AGI, ask which of the four they mean. Most disagreements dissolve at that point. A system can be broad and shallow, or narrow and superhuman, or capable but not autonomous. Describing it along each axis separately is the beginning of thinking clearly.

## A map, not a prophecy: levels of capability

In late 2023 a group of researchers at Google DeepMind published a framework that does the separation for you. Their paper, *Levels of AGI*, proposes classifying systems on two axes: **performance** (how well, compared with people) and **generality** (how broadly), with autonomy treated as a third, separate dimension that is a matter of deployment choice rather than capability alone.[^1]

The performance axis runs from "emerging" (equal to or somewhat better than an unskilled person) through "competent" (at least the median skilled adult), "expert" (the 90th percentile), "virtuoso" (the 99th) to "superhuman" (better than everyone). The generality axis has two values: narrow (a clearly scoped task or set of tasks) and general (a wide range of non-physical tasks, including the ability to learn new ones). A calculator is narrow and superhuman. A 2023 chatbot was, by the authors' own assessment, general but only emerging: broad, and roughly at the level of an unskilled person across that breadth, with pockets of much higher performance.

Two features of the framework are worth more than the labels themselves.

The first is that **performance and generality are measured separately**. This is what the bar-exam-versus-letter-counting argument was missing. A system can sit high on one axis and low on the other, and most of the interesting systems of this decade will. When you read a capability claim, locate it on both axes before you react to it.

The second is that **autonomy is a choice, not a level**. The same model can be deployed as a tool (it acts only when asked), a consultant (it proposes, a person decides), a collaborator (it and a person share the work), an expert (it does the work, a person reviews), or an agent (it acts, a person is informed). Which of these a system is allowed to be depends on reliability, on the stakes, and on who bears the consequences of a mistake. A model's level sets an upper bound on how much autonomy makes sense; it does not determine it. This matters for the rest of the book because almost every economic and institutional effect of AI runs through the autonomy that organisations actually grant, not through the raw capability that exists in a lab.

The framework will not survive the decade unchanged. The authors say so. The levels may compress or split; the generality axis may acquire gradations; physical tasks may need their own treatment. Use it as a map that will be redrawn, which is what every useful map is.

## The right question

"Is it AGI yet?" asks for a yes or a no about a system that is, at any moment, a scatter of points across a plane. It cannot be answered honestly, and the attempts to answer it produce heat rather than light.

The question that can be answered is: **which tasks, at what level, with what reliability, under what autonomy?**

Each clause does work.

*Which tasks.* Not "coding" but "writing a function from a clear specification in a popular language", which is a very different task from "finding the one wrong assumption in a large, old codebase". Not "medicine" but "summarising a discharge note" versus "choosing between two treatments for a patient with three conditions". The finer the task description, the more useful the capability claim, and the less it will be misread.

*At what level.* Compared with whom? A system that drafts legal clauses as well as a second-year associate is a different fact from one that drafts them as well as a partner, and both are different from one that does it as well as a careful layperson with a template. The reference population changes what the capability is worth and to whom it is a threat.

*With what reliability.* A system that is right 95 per cent of the time is a brilliant assistant and a catastrophic autopilot. The same number means opposite things depending on who catches the other five per cent. Reliability also has a shape: are the failures random, or clustered on particular inputs, or on inputs that look exactly like the successes? A system that fails loudly can be managed. A system that fails fluently cannot be managed by anyone who is not already an expert.

*Under what autonomy.* Does a person check every output, or sample them, or only hear about problems? The economic value and the risk of a system both scale with autonomy, and autonomy is granted by institutions, slowly, as reliability is demonstrated. This is why capability arrives in labs years before it arrives in your workplace, and why the gap between the two is one of the main subjects of this book.

Train yourself to translate every claim you hear into this form. "AI can now do X" becomes "a system did task X at level L with reliability R when operated as a tool by an expert who checked the output". Sometimes that translation leaves the claim intact. Often it does not.

## Three confusions that recur

Three particular mistakes come up so often that they deserve names.

**Benchmark performance is not job performance.** A benchmark is a fixed set of questions with known answers, usually chosen because they are gradable. Jobs are open-ended, context-dependent and graded by consequences. A system that scores well on a benchmark has demonstrated something real, but the something is "can produce gradable answers to questions of this type under these conditions", not "can do the job that people who answer such questions have". The gap is widest for tasks where most of the work is figuring out what the question is. Chapter 2 is about the measurement problem in detail; for now, hold onto the distinction.

**Fluency is not competence.** Language models produce text that reads as confident and well-organised whether or not it is correct. Human readers have spent their whole lives in an environment where fluent, well-structured prose was a reliable signal of a careful mind, and that signal has now been decoupled from the thing it used to indicate. This is not a technical footnote; it is the single largest reason that people over-trust these systems, and the reason that verification skills, discussed throughout this book, are becoming more valuable rather than less.

**Demos are not deployments.** A demonstration is a chosen task, on chosen inputs, with the operator ready to retry. A deployment is whatever users actually do, on whatever they actually bring, with nobody standing by. The distance between the two is where most of the engineering work in this field actually lives, and it is why the companies that ship reliable systems often look slower than the companies that ship impressive videos.

When you hear a capability claim, check which of these three confusions it might be riding on. Usually at least one.

## Why the word matters anyway

If "AGI" is this ambiguous, why not drop it?

Because the word is a coordination device. Companies set their missions by it. Governments write policy around thresholds that invoke it. Investment, hiring, regulation and public mood all move on what people believe about how close it is. A term that moves that much money and that much policy cannot simply be abandoned; it has to be used carefully.

It also matters because the thing the word gestures at, however imprecisely, is real: the direction of travel is toward systems that are broader, more reliable and more autonomous than they were, and the economic and institutional consequences of that direction do not wait for anyone to agree on a definition. You can refuse to say "AGI" and still have to decide what your college should teach, what your firm should automate and what you should learn next year. The map in this chapter is for making those decisions, not for winning arguments about the word.

## What would make this chapter wrong

A reader in 2031 should check the following.

If a single system has reached expert-level performance across the full breadth of non-physical tasks *and* is routinely operated at high autonomy in consequential settings, then the careful separation of axes in this chapter will look like pedantry, because the points on the plane will have collapsed into a corner. That is possible. The chapter's framework still describes how we got there, but its emphasis on gradations would be dated.

Conversely, if progress on the generality axis has stalled while narrow systems have kept improving, then the chapter under-weights how much of the decade's change came from many narrow, superhuman tools rather than from general ones, and the chapters on work and learning should be read with that correction.

If the levels framework itself has been superseded by a better-validated taxonomy, use that one. The argument of the chapter is that you need *a* map with separate axes; it is not an argument for this particular drawing.

## What to do this year

Learn to read an evaluation. Pick one widely reported capability claim and find its source: the benchmark or study behind the headline. Write down, in one line each, which tasks it tested, against which reference population, with what reliability, and how the system was operated. Then write down what the headline implied about each of those. The gap you find is the skill this chapter is trying to give you, and you will use it every month for the next ten years.

---

[^1]: Morris, M. R., Sohl-Dickstein, J., Fiedel, N., Warkentin, T., Dafoe, A., Faust, A., Farabet, C. & Legg, S. (2023, revised 2024). *Levels of AGI for Operationalizing Progress on the Path to AGI.* Google DeepMind. arXiv:2311.02462.

### Sources for this chapter
- Morris et al., *Levels of AGI* (2023/2024), arXiv:2311.02462 — the two-axis framework and the autonomy levels.
- OpenAI, *OpenAI Charter* (2018) — the "highly autonomous systems that outperform humans at most economically valuable work" definition, cited here as an example of the economic meaning of the term.
- OpenAI, *GPT-4 Technical Report* (2023), arXiv:2303.08774 — source of the simulated bar-exam result referenced in the opening.
