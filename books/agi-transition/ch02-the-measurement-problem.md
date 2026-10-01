# Chapter 2 — The measurement problem

Every claim about what AI can do rests on a measurement, and most of the measurements are worse than they look. This is not because the people making them are careless. It is because measuring the capability of a system that has read most of the internet is genuinely hard, in ways that the field is still working out, and because the incentives around the measurements push toward numbers that go up.

If chapter 1 gave you a map with axes, this chapter is about the instruments that place a system on the map, how they break, and how to read them anyway. The skill is not academic. Over the next decade you will be asked to judge capability claims as a student choosing what to learn, as an employee deciding what to trust, as a manager deciding what to buy, and as a citizen deciding what to allow. Nobody will hand you a clean number. You will have to read the dirty ones.

## What a benchmark is

A benchmark is a fixed collection of tasks with a scoring rule. A set of multiple-choice questions across academic subjects with the answer key. A set of programming problems with hidden test cases. A set of maths word problems with numeric answers. The system is run on the tasks, the scoring rule is applied, and a number comes out.

Benchmarks exist because they make progress comparable. Two systems scored on the same tasks under the same rules can be ranked, and the same system scored a year apart shows a trajectory. Almost everything useful that is known about the rate of progress in this field comes from benchmarks, and the chapters that follow lean on that knowledge. So the point of this chapter is not that benchmarks are bad. It is that a benchmark score is the answer to a narrow question, and the narrow question is usually not the one in the headline.

The narrow question is: *how often does this system produce a gradable answer that matches the key, on this fixed set of tasks, under these conditions?* Every word of that matters.

## Four ways the instrument breaks

**Saturation.** A benchmark is informative while systems score in its middle range. Once the best systems score near the ceiling, differences between them stop meaning anything, and improvements on the benchmark stop tracking improvements on the underlying skill. Benchmarks that took years to climb in the 2010s were climbed in months in the 2020s; several of the most cited were effectively saturated within two or three years of release. A saturated benchmark is a thermometer whose scale ends at the temperature of the room.

**Contamination.** Modern systems are trained on enormous text collections scraped from the public internet. Benchmark questions and their answers are on the public internet. So some fraction of any public benchmark has usually been seen, in some form, during training, and a high score may partly reflect recall rather than reasoning. Researchers try to detect and quantify this, and the honest technical reports now include contamination analyses. But the clean solution, questions nobody has published, is in tension with the point of a benchmark, which is that everyone can run it. Held-out, periodically refreshed and private evaluations are the response, and they are the ones to weight most heavily when you see them.

**Goodhart's law.** When a measure becomes a target, it stops being a good measure. Once a benchmark is the number that drives funding, hiring and press, developers optimise for it, directly or through choices about training data and tuning. The optimisation is not necessarily dishonest; it is what any organisation does with a metric it is judged on. The effect is the same: the number rises faster than the thing it was supposed to indicate.

**Mismatch with use.** A multiple-choice question tests whether the system can pick the right option when the options are given. Real tasks rarely come with options. A programming benchmark tests whether a short function passes hidden tests when the specification is clear. Real programming is mostly discovering what the specification should have been. The better a benchmark is at being gradable, the further it tends to sit from how the skill is actually used.

None of these makes a benchmark result false. Each makes it mean less than its headline. When you read "system X scores Y per cent on benchmark Z", the four questions to ask are: is Z saturated, could Z be in the training data, is Z the number everyone is optimising for, and how far is Z from the task I actually care about.

## What survives

Some kinds of evaluation resist these failures better than others, and they are the ones to look for.

**Held-out and refreshed.** Evaluations whose questions are new, kept private, and replaced over time cannot be memorised and are harder to target. They are more expensive to run and harder to compare across years, which is why they are rarer. When a lab or an independent evaluator reports results on a private held-out set, that number deserves more weight than a public benchmark score of the same size.

**Task-based.** Evaluations that ask a system to complete a realistic task from start to finish, with the messiness intact (ambiguous instructions, a real environment, a result that has to actually work), measure something closer to usefulness. They are harder to score, so they are usually scored by people or by checking an outcome rather than an answer. The emerging practice of measuring agents by the length and complexity of tasks they can complete reliably is an example.

**Reliability, not just accuracy.** A single accuracy number hides the distribution of failures. Evaluations that report consistency across repeated runs, calibration (does the system's confidence track its correctness), and performance on the hardest subset tell you how the system will behave when it matters. A system that is right 90 per cent of the time and knows which 10 per cent it is unsure about is a different tool from one that is right 90 per cent of the time and equally confident throughout.

**Measured by people who did not build it.** Independent evaluation is the oldest quality signal in science and it applies here. Results reproduced by a third party, on their own hardware, with the published method, are worth more than results reported by the developer, even an honest one, because the third party did not make the hundred small choices that nudge a number upward.

When you see one of these, lean in. When you see a single public benchmark score and nothing else, lean back.

## Reading a model card and a technical report

Most major systems now ship with two documents: a short *model card* that summarises what the system is, what it was trained on, how it was evaluated and what it should not be used for; and a longer *technical report* with the details. Learning to read them is the practical form of the skill this chapter is about. Three things to look for.

**What is disclosed, what is estimated, what is missing.** Training data: described, listed or not mentioned? Compute used: stated, estimated by outsiders or withheld? Evaluation: on which benchmarks, with what prompting, how many attempts, with contamination checked or not? A report that states its omissions is more trustworthy than one that fills every box, because the first author knows what they do not know.

**The conditions.** Scores often depend on how the system was prompted (with examples or without), how many attempts it was allowed, and whether it could use tools. The same system can move ten or twenty points on a benchmark depending on these settings. A score without its conditions is not a score.

**The limitations section.** Every honest report has one. Read it first. It tells you where the system fails, which is the information you need to decide whether it fits a task, and it tells you how candid the authors are, which is the information you need to decide how much to trust the rest.

Independent datasets now track what the reports disclose about compute, energy and data over time, and the trend in disclosure is itself a measurement worth watching: when it falls, the field is becoming harder to evaluate from outside.

## A worked case: two benchmarks, re-examined

Two of the most-cited benchmarks of the early 2020s were re-examined by independent researchers in 2024, and the two re-examinations illustrate two of the four failure modes above with unusual clarity.

The first was a large multiple-choice test of academic knowledge across 57 subjects, from elementary mathematics to professional law, which had become the single most-quoted number in model announcements: a system's score on it was treated, loosely, as its general knowledge. A team re-annotated a sample of 3,000 of its questions by hand and found that about 6.5 per cent contained errors: wrong answer keys, questions with no correct option or more than one, questions that were unanswerable as written. In the worst subject, virology, more than half the sampled questions had a problem.[^1] A benchmark with a 6.5 per cent error floor cannot distinguish systems within about six points of each other near the top, which by 2024 was where every leading system sat. The instrument had saturated, and part of the saturation was the instrument's own noise.

The second was a widely used set of grade-school arithmetic word problems, the standard test of simple mathematical reasoning. Because it was public and old, its questions and answers were almost certainly present in the training data of every system scored on it. A team wrote a fresh set of 1,250 problems of matched difficulty and style, kept it private, and scored the same systems on both. Several families of models scored markedly lower on the fresh set, by up to about eight percentage points, which is direct evidence of contamination: they had partly memorised the public set rather than learned the skill. The strongest systems showed little gap, which is the encouraging half of the result and the reason the method matters: it separated the systems that had learned arithmetic from the ones that had learned the test.[^2]

Neither study said the benchmarks were useless. Both said what this chapter says: a score is the answer to a narrow question, and the only way to know how narrow is to look at the questions and to test the system on ones it has not seen. The teams that did the looking did more for the field's understanding of capability that year than any new state-of-the-art result, and the method they used (re-annotate a sample; write a private twin) is available to anyone with a weekend and a will to check.

## Evaluation as a civic skill

For most of the history of technology, the people who had to judge a tool were the people who used it, and they could judge it by using it. A spreadsheet either calculated correctly or it did not, and anyone could check.

AI systems break that arrangement in two ways. Their outputs are fluent whether or not they are correct, so using them does not reveal their quality unless you already know the answer. And their behaviour is distributional, meaning they are right most of the time and wrong in ways that are hard to predict, so a handful of trials tells you little.

The consequence is that evaluation, which used to be a specialist's job, is becoming everyone's. A journalist reporting a capability claim, a manager deciding to automate a workflow, a teacher deciding whether a tool can be used for homework, a voter weighing a policy that invokes "AI capabilities": each of them needs the reading skills in this chapter, and each will be misled without them. The gap between what the systems can do and what people believe they can do, in both directions, is itself one of the risks of the transition, and it is closed by better measurement and better readers of measurement, not by better systems.

## What would make this chapter wrong

If by 2031 the field has converged on a small number of independent, held-out, task-based evaluations that are widely trusted and that track real-world usefulness well, then the warnings here will read as describing a solved problem. The chapter's advice about reading conditions and limitations would still hold, but its urgency would not.

If instead evaluation has become mostly private, with capability measured by the developers alone and little independent reproduction, then the chapter under-states the problem, and the reader should treat every public capability claim with more scepticism than the text suggests.

If a system has become capable enough to grade open-ended work as reliably as expert humans, then much of the difficulty of task-based evaluation disappears, since the expensive step was always the grading. That would change the economics of measurement more than anything else in this chapter.

## What to do this year

Run one public benchmark yourself. Pick a small, well-documented one, download the questions, run an openly available model on it with the published prompting, and score the results. Then do three things: find questions the model got wrong and see whether you can tell why; search for a few of the questions online and see how many appear verbatim; and change the prompt format and see how much the score moves. In an afternoon you will understand saturation, contamination and conditions better than a year of reading about them, and you will never again take a single number at face value.

---

[^1]: Gema, A. P. et al. (2024), "Are We Done with MMLU?", arXiv:2406.04127; the re-annotated subset is published as MMLU-Redux.
[^2]: Zhang, H. et al. (2024), "A Careful Examination of Large Language Model Performance on Grade School Arithmetic", arXiv:2405.00332; the private twin set is GSM1k.

### Sources for this chapter
- Gema et al. (2024) — MMLU-Redux; Zhang et al. (2024) — GSM1k.
- Goodhart, C. (1975), on measures that become targets; Strathern, M. (1997), "'Improving ratings': audit in the British University system", *European Review*, for the popular formulation.
- Mitchell, M. et al. (2019), "Model Cards for Model Reporting", *FAT\* '19* — the origin of the model-card practice.
- OpenAI (2023), *GPT-4 Technical Report*, arXiv:2303.08774 — includes a contamination analysis, cited as an example of disclosed methodology.
- Kiela, D. et al. (2021), "Dynabench: Rethinking Benchmarking in NLP", *NAACL* — on benchmark saturation and dynamic, held-out evaluation.
- Epoch AI, *Notable AI Models* dataset and documentation (accessed 2026) — on tracking disclosure of compute and training details over time.
- Stanford HAI, *AI Index Report* (2025, 2026) — on benchmark saturation trends and the move toward new evaluations.
