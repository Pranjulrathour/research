# Chapter 6 — Science and engineering: faster, not automatically better

In 2020 a system called AlphaFold predicted the three-dimensional structure of proteins from their amino-acid sequences with an accuracy that the field had been chasing for fifty years, and within two years its predictions for almost every known protein had been released for anyone to use.[^1] It is the clearest case so far of AI changing what a science can do, and it is worth starting with because of what it did *not* do. It did not run the experiments that confirmed the predictions. It did not decide which proteins mattered. It did not write the papers, review them, or persuade anyone to change a drug programme. It made one step in a long chain enormously faster, and the chain re-formed around the new bottleneck.

That is the pattern this chapter is about. AI accelerates particular steps in research and engineering, often dramatically. Acceleration of a step moves the bottleneck to the next step, and the next step is usually one where the limit is physical, institutional or human: an experiment that takes a week, a review that takes a month, a verification that takes a career. Understanding where the bottleneck moves tells you where the work, and the value, moves with it.

## Where it accelerates

Four places, roughly in order of how settled the evidence is.

**Literature.** Reading, summarising, searching and connecting published work. A researcher can now survey a field in days that used to take months, find the three papers that matter among three thousand, and get a serviceable summary of a technique outside their speciality. This is real and already changing how research is done. It also produces the failure mode that chapter 2 warned about: fluent summaries of papers that do not say what the summary says, and citations to papers that do not exist. The acceleration is in finding and skimming; the verification is still a human reading the actual paper.

**Code.** Writing analysis scripts, simulations, data pipelines and the glue that holds research software together. Much of the time in computational research is spent on code that is not the point of the research, and that code is exactly what current systems write well. The scientist who used to spend a week getting the pipeline to run spends a day, and spends the rest on the question. The risk is code that runs and is wrong, which has always been the risk in research software and is now easier to produce at volume.

**Simulation and search.** Predicting properties of molecules, materials, proteins and designs; proposing candidates for experiments; narrowing a search space of millions to hundreds. This is where AlphaFold sits, along with a growing set of systems in chemistry, materials science and engineering design. The gains are largest where the search space is huge, the evaluation is expensive, and a reasonably accurate predictor can prune most candidates before anyone builds anything.

**Analysis.** Finding structure in large data sets, fitting models, generating hypotheses from patterns. Powerful, and the place where the line between "the system found something" and "the system found something that is there" is thinnest. Every statistical failure that has plagued empirical science (fishing, overfitting, confounds) is available at higher speed.

Each of these is a genuine acceleration. Each moves the bottleneck.

## Where the bottleneck moves

**Experiments.** If a system can propose a thousand candidate molecules in an afternoon, the laboratory that can synthesise and test ten a week is the constraint. Automated laboratories, robotic synthesis and high-throughput screening are the response, and they are expensive, slow to build and far behind the software. For most of the decade, the physical world will be the rate limit on sciences that have to touch it.

**Verification.** A result is not knowledge until someone has checked it, and checking has not got faster. If anything, the volume of plausible-looking results has made it slower, because reviewers and replicators have more to check and less signal about which checks matter. The fields that cope best will be the ones that make verification cheap by design: code and data published with every result, automated reproduction, pre-registered analyses.

**Review and publication.** Peer review was already strained before 2023. Submission volumes have since risen sharply in several fields, a growing share of submissions show signs of machine drafting, and reviewer capacity has not grown. Venues have responded with stricter requirements, including, in some cases, refusing categories of paper that are easy to generate and hard to evaluate. The institution of publication is being renegotiated in real time, and the direction is toward requiring evidence that is harder to fake.

**Judgment.** Which question is worth asking. Which anomaly is a discovery and which is a bug. When a result is good enough to act on. These were always the scarce inputs to research, and acceleration elsewhere makes them scarcer in relative terms. The researcher who spent most of their time on pipeline code now spends most of it on judgment, and judgment is harder to learn and harder to teach.

The honest summary for anyone entering research or engineering: the parts of the job that felt like work are getting easier, and the parts that felt like the job are getting more important.

## The reproducibility dividend

There is a second-order effect that deserves its own section because it changes what counts as credible, and credibility is what this book's reader is trying to build.

When plausible results are cheap to produce, the value of results that can be *checked* rises. A paper with its code, its data, its exact environment and a one-command reproduction is more credible than a paper without them, and the gap between the two kinds of paper widens as the cost of producing the second kind falls toward zero. Journals and conferences are already moving toward requiring artefacts. Hiring committees and recruiters, which have always used publications as a signal, are learning to weight reproducible work over the rest.

This cuts in the reader's favour. A student with one small, fully reproducible, honestly-reported result has something that a hundred fluent summaries cannot buy: evidence of the judgment the bottleneck has moved to. Code plus data plus a limitations section is the new unit of credibility, and it is available to anyone with a laptop and the discipline to use it.

The same logic applies in engineering. A benchmark that others can run is worth more than a performance claim. A design document that records what was measured and what was assumed is worth more than one that records only the decision. The habit of making work checkable is, in a decade of cheap plausibility, the professional habit that matters most.

## Engineering specifically

Engineering is research's practical sibling, and the pattern holds with one difference: the bottleneck in engineering was already judgment and integration rather than production, and the acceleration makes that more visible.

Building software, designing systems, specifying hardware: the production steps get faster. What does not get faster is knowing what to build, knowing whether it works under conditions nobody tested, and keeping it working when the world changes around it. The engineering disciplines that will do well are the ones that already prized those things (reliability engineering, systems design, safety engineering), and the engineers who will do well are the ones who can hold a whole system in their heads and ask what breaks.

There is also a new category of engineering work: building and operating the AI systems themselves. Evaluation, monitoring, guardrails, data pipelines, integration, the unglamorous reliability work that turns a model into a product. It is a new-task channel in chapter 3's sense, it is where much of the hiring is, and it rewards exactly the measurement discipline that this chapter and chapter 2 describe.

## What would make this chapter wrong

If by 2031 automated laboratories and simulation have made the physical bottleneck much less binding, with AI-proposed candidates routinely tested at scale, then this chapter underestimated how fast the experimental side could catch up. Check the rate of AI-originated discoveries that reached clinical or industrial use.

If peer review and verification have been substantially automated, with trusted AI reviewers and automated reproduction, then the verification bottleneck moved faster than argued here. Check whether major venues accept or require automated review, and whether reproduction rates improved.

If, instead, the volume of low-quality machine-assisted research has overwhelmed the field's ability to sort it, the chapter was too optimistic about institutions adapting, and the reproducibility dividend is larger than described because checkable work is rarer.

## What to do this year

Reproduce one published result end to end. Pick a paper in your field with public code and data, run it, and see whether you get the numbers in the paper. Write down everything that was missing, ambiguous or wrong in the published materials. You will learn three things: what the result actually depends on, how rarely published work is fully reproducible, and what your own work must include to be worth more than the average. Then publish your reproduction, with its code, as a short note. It is a first paper, it is honest, and it is the kind that the next decade rewards.

---

[^1]: Jumper, J. et al. (2021), "Highly accurate protein structure prediction with AlphaFold", *Nature* 596; Varadi, M. et al. (2022), "AlphaFold Protein Structure Database", *Nucleic Acids Research* 50(D1).

### Sources for this chapter
- Jumper et al. (2021), *Nature* 596 — AlphaFold; Varadi et al. (2022) — the open database.
- Merchant, A. et al. (2023), "Scaling deep learning for materials discovery", *Nature* 624 — AI-proposed materials and the gap to experimental verification.
- Nosek, B. A. et al. (2015), "Promoting an open research culture", *Science* 348(6242) — the transparency and openness guidelines behind artefact requirements.
- arXiv (2025), "Updated practice for review articles and position papers in the CS category", arXiv blog, 31 October 2025 — a publication institution responding to machine-drafted submissions.
- Baker, M. (2016), "1,500 scientists lift the lid on reproducibility", *Nature* 533 — the pre-AI baseline on reproducibility.
