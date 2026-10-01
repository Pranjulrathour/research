# Chapter 5 — Learning: schools, colleges and the end of the essay as proof

For about two hundred years, education has run on a convenient coincidence: the artefacts that students produce to learn (essays, problem sets, programs, proofs) were also the artefacts that proved they had learned. A teacher could set an essay, and the essay did two jobs at once: writing it taught the student, and reading it told the teacher what the student knew. The coincidence was never perfect, but it was good enough to build systems of assessment, credentialing and admission on top of.

In late 2022 the coincidence ended. A student can now produce a competent essay, a working program or a correct proof without having learned anything, in less time than it takes to read the assignment. The artefact still teaches, if the student makes it. It no longer proves anything, because the teacher cannot tell whether the student did.

This chapter is about what happens to learning when proof and practice come apart, what the technology genuinely offers to learners, and what a curriculum should look like when the tools can do the exercises. It is written for students and for the people who teach them, because both are about to be asked to change, and the ones who understand why will change better.

## Assessment collapse

Call the problem *assessment collapse*: the sudden loss of information in the artefacts that education used to measure learning.

The first responses were predictable and have mostly failed. Detection tools that claim to identify machine-written text have error rates that make them unusable for consequential decisions, and they fail disproportionately on writers whose first language is not English.[^1] Bans on the tools are unenforceable outside a supervised room. Pretending nothing changed produces a grade distribution that measures access to the tools rather than learning.

The responses that work share one feature: they move assessment back toward things that can be observed directly.

**Oral examination.** Asking the student to explain, defend and extend their work in conversation. It is expensive in teacher time, it has been the standard in doctoral education for centuries precisely because it is hard to fake, and it is coming back at every level. A student who can discuss an essay they produced has learned; one who cannot has not, whatever the essay looks like.

**Supervised work.** Writing, problem-solving and coding done in a room where the conditions are known. This measures what the student can do alone, which is one of the things worth measuring, though not the only one.

**Process evidence.** Drafts, version history, notes, the record of how the work came to be. A student who shows their path has shown their learning. This is already standard in software (commit history), in mathematics (the scratch work), and in studio disciplines (the portfolio of attempts), and it generalises.

**Portfolios of verifiable work.** Over a term or a degree, the student accumulates artefacts that other people have used, tested, built on or cited. A program that runs in production, an analysis someone acted on, a result someone else reproduced. These are hard to fake because they involve the world pushing back.

The common thread is that assessment is shifting from *what did you produce* to *what can you do, and how did you do it*. That shift is correct, it is overdue, and it is more work for everyone. It also happens to align assessment with what employers were already asking for, which chapter 10 returns to.

## A worked case: the detector

The first institutional reflex after late 2022 was to buy a detector, and what happened next is the clearest available lesson in why the reflex fails.

In April 2023 the largest provider of plagiarism-checking software to universities switched on an AI-writing detector for its millions of institutional users, reporting a false-positive rate of under one per cent at the document level.[^4] One per cent sounds small. A large university runs tens of thousands of submissions through such a system each term; at one per cent, several hundred students a term would be accused of something they did not do, with no way to prove a negative, in a process where the accusation itself is the punishment. Within months, several universities turned the feature off. One of the first, a large private university in the United States, published its reasoning in August 2023: the vendor could not explain how the detector reached its conclusions, the false-positive rate could not be independently verified, and the institution judged that even the claimed rate would wrongly flag an unacceptable number of honest students.[^5]

The deeper problem surfaced in a study published the same summer. Researchers ran essays by non-native English speakers, written for a standardised English test before any of these tools existed, through seven commercial AI detectors. More than half were flagged as machine-written, and the majority of essays were flagged by at least one detector; the same detectors classified essays by native-speaking American students as human-written almost every time.[^1] The detectors were keying on exactly the features of careful, simpler, more formulaic prose that second-language writers produce and that language models also produce, which meant the students most likely to be falsely accused were the ones with the least standing to contest it.

The case shows why the chapter's argument is structural rather than a matter of waiting for better detectors. A detector is a classifier in an arms race with a generator that improves faster; its errors fall on the innocent, in a setting where a false accusation is a serious harm; and even a perfect detector would answer the wrong question, because the problem is not catching the student who used the tool but knowing what the student learned. The institutions that did well were the ones that stopped asking the artefact to prove learning and started asking the student.

## What the technology actually offers learners

It would be a mistake to treat AI in education only as a threat to assessment. The same capability that makes the essay useless as proof makes something available that education has wanted for a very long time.

In 1984, the educational psychologist Benjamin Bloom published a finding that became known as the two-sigma problem: students taught one-to-one by a skilled tutor performed about two standard deviations better than students taught in a conventional classroom, meaning the average tutored student outperformed about 98 per cent of the conventionally taught ones.[^2] The problem in the name was that one-to-one tutoring was unaffordable at scale, and Bloom challenged the field to find methods that approached its effect in a classroom.

AI tutoring systems are the first technology that plausibly addresses the problem directly: a patient, available, infinitely repeatable explainer that adapts to the individual and never tires of the same question asked a fourth way. Early controlled studies of AI tutoring in real courses have found meaningful gains, in some cases comparable to the gains from well-designed active learning, when the tutor was built to guide rather than to answer.[^3]

Three caveats keep the promise honest.

**Access.** A tutor that requires a good device, a fast connection, fluent English and the habit of asking questions reaches the students who already have the most. Without deliberate design, AI tutoring widens the gap it could close. In India, where chapter 11 goes into detail, this is the central design problem.

**Motivation.** Bloom's tutors did not only explain; they held the student accountable, noticed when attention drifted, and cared. The explaining part of tutoring is now cheap. The caring part is not, and the evidence from online education over the past two decades is that explanation without accountability reaches the already-motivated and loses everyone else.

**The gap between a tutor and a syllabus.** A system that answers questions well is not a curriculum. Someone still has to decide what should be learned, in what order, to what standard, and why. The schools and colleges that do well will be the ones that keep that design job and use the tools to deliver it, rather than the ones that hand the job to the tool.

The realistic version of the promise is not two sigmas for everyone. It is that the explaining part of teaching gets cheap and good, which frees human teachers to do the parts that were always scarce: motivation, judgment, accountability and the design of what is worth learning.

## What a computing degree should look like

Take the degree most readers of this book hold or are pursuing: a computing degree, an MCA or a B.Tech in computer science, in a country that produces more of them than any other.

The traditional curriculum spends much of its time teaching students to produce artefacts that systems now produce on demand: syntax, standard algorithms implemented from memory, boilerplate, routine debugging. Those things still need to be understood. They no longer need to be the thing a graduate is paid to do, and a curriculum that treats them as the destination is training people for the entry-level jobs that chapter 4 showed are narrowing.

Five shifts follow.

**From writing code to specifying, reading and verifying it.** The scarce skill is knowing what should be built, judging whether what was built is right, and finding out why when it is not. Students should spend as much time reviewing code they did not write, with and without machine help, as writing it.

**From the solution to the problem.** Problem-framing, requirements, understanding a domain well enough to know what matters: these are the tasks that precede any code and that the tools do badly. They can be taught, mostly by giving students real, messy problems rather than clean exercises.

**From individual output to systems.** How components fit, fail and recover; how data flows; where latency and cost come from; what breaks at scale. Systems thinking is the layer above any single program, and it is the layer that stays valuable when programs are cheap. (It is also the subject of the companion volume to this book.)

**From trusting output to measuring it.** Every graduate should be able to evaluate a model, a system or a claim: design a test set, read a result, spot a confound, know what a number does and does not show. Chapter 2 made the case that evaluation is a civic skill. For a computing graduate it is a professional one.

**From the exam to the portfolio.** A degree's proof should be a body of verifiable work (systems that run, analyses that hold up, contributions others accepted) rather than a transcript of supervised exams. Colleges that make the portfolio central will produce graduates who clear the narrowed entry rung; colleges that do not will produce graduates with a credential that signals less each year.

None of this requires abandoning fundamentals. Data structures, algorithms, probability, operating systems and networks matter more, not less, when the tools are powerful, because they are what lets a person tell good output from plausible output. What changes is that the fundamentals are taught as a basis for judgment rather than as a set of things to reproduce under exam conditions.

## What students can do without waiting for institutions

Institutions change slowly; chapter 3 explained why. A student does not have to wait.

Use the tools to learn, not to skip learning. The difference is whether you can do the thing afterwards without them. A simple test: after using a system to help with a problem, close it and solve a similar problem alone. If you can, you learned. If you cannot, you were shown.

Build the portfolio now. One verifiable piece of work per term is enough to be ahead of most of a graduating class by the time it matters. Verifiable means someone else used it, ran it, or checked it.

Practise explaining. Oral examination is coming back and it is also what every technical interview and every meeting is. Being able to say clearly what you did, why, and what you would do differently is a skill, and it is one the tools cannot do for you in the room.

Pick a domain. Computing applied to a field you understand (finance, health, agriculture, logistics, law) is worth more than computing alone, because the scarce input is understanding what the field needs. India has many underserved fields and few people who understand both the field and the technology. That gap is a career.

## What would make this chapter wrong

If by 2031 assessment has largely moved to supervised, oral and portfolio forms and the transition went smoothly, the "collapse" framing will look dramatic, and the chapter's value is as a record of why the change happened. Check whether major universities and boards changed their assessment rules between 2024 and 2030, and how.

If AI tutoring has produced large, broad, well-measured learning gains across income levels, the caveats here about access and motivation were too pessimistic, and the chapter should be read as having underestimated what good design could do. Check randomised studies with low-income and non-English-speaking cohorts in particular.

If detection tools have become reliable enough to use for consequential decisions, which currently seems unlikely, part of the assessment-collapse argument weakens. Check their false-positive rates on non-native writers before believing a vendor.

## What to do this year

Build one thing a system cannot do for you, and document how you did it. Choose a problem that requires talking to real people, gathering data that is not online, or making a judgment call that depends on context the tools do not have. Keep the drafts, the dead ends and the notes. At the end you will have a piece of work that proves what the essay no longer can, and a record of process that is worth more than the result.

---

[^1]: Liang, W., Yuksekgonul, M., Mao, Y., Wu, E. & Zou, J. (2023), "GPT detectors are biased against non-native English writers", *Patterns* 4(7).
[^2]: Bloom, B. S. (1984), "The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring", *Educational Researcher* 13(6).
[^3]: Kestin, G., Miller, K., Klales, A., Milbourne, T. & Ponti, G. (2025), "AI tutoring outperforms in-class active learning: an RCT introducing a novel research-based design in an authentic educational setting", *Scientific Reports* 15 — one of the first randomised comparisons in a real university course; read its scope and limitations before generalising.
[^4]: Turnitin (2023), "AI writing detection" product announcement and FAQ, April 2023, stating a document-level false-positive rate below 1 per cent.
[^5]: Vanderbilt University (2023), "Guidance on AI detection and why we're disabling Turnitin's AI detector", Brightspace / Center for Teaching announcement, 16 August 2023.

### Sources for this chapter
- Bloom (1984), *Educational Researcher* 13(6) — the two-sigma problem.
- Liang et al. (2023), *Patterns* 4(7) — detector bias against non-native writers.
- Kestin et al. (2025), *Scientific Reports* 15 — AI tutoring RCT.
- Freeman, S. et al. (2014), "Active learning increases student performance in science, engineering, and mathematics", *PNAS* 111(23) — the active-learning baseline that tutoring studies compare against.
- UNESCO (2023), *Guidance for generative AI in education and research* — the policy response to assessment collapse.
