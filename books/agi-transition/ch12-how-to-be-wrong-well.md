# Chapter 12 — How to be wrong well

Every chapter in this book has ended with a section on what would make it wrong. This chapter is that section for the book as a whole, and it is also the book's actual conclusion, because the central claim of a field guide to a transition is not any particular prediction. It is that the person who comes through the next decade stronger will be the one who updates fastest and most honestly, and that updating is a skill with a method.

The method has three parts: knowing the base rates, keeping a record, and listing your own likely errors in advance. The chapter takes them in turn and then closes with the ten habits the rest of the book has been building toward.

## Base rates: what previous general-purpose technologies did

The most reliable guide to how a transformative technology diffuses is how the previous ones did, and the record is consistent enough to be useful.

**Electricity.** The dynamo was commercially practical by the early 1880s. Factory productivity did not visibly respond until the 1920s, roughly forty years later, because the gains came not from replacing steam engines with electric motors in the same factory layout, but from redesigning the factory around small motors at each machine, which required a generation of engineers who had grown up with the new technology and a stock of old factories to wear out.[^1] The lesson is that the technology is the fast part; the reorganisation of work around it is the slow part, and the reorganisation is where the value is.

**Computing.** Business computing was widespread by the 1970s. Through the 1980s, measured productivity growth in the countries that invested most heavily in it was unimpressive, which prompted the economist Robert Solow's remark in 1987 that the computer age was visible everywhere except in the productivity statistics.[^2] The acceleration came in the second half of the 1990s, two decades after the investment began, and it came alongside large intangible investments (new processes, training, organisational redesign) that the statistics had not counted. Economists later formalised this as the *productivity J-curve*: a general-purpose technology first depresses measured productivity, because firms are investing in intangibles that do not show up as output, and then raises it, often sharply.[^3]

**The internet.** Commercially open from the early 1990s; the first boom and bust by 2001; the business models that actually dominated (search advertising, platforms, cloud computing, the smartphone ecosystem) mostly emerged or matured between 2004 and 2012. The firms that led in 1999 were, with a few exceptions, not the firms that led in 2015. The lesson is that the early winners of a transition are not reliably the eventual winners, and that the most important applications are usually not the ones imagined at the start.

Three regularities hold across all three.

*Diffusion takes decades, not years.* Measured from commercial availability to broad economic impact, the lag has been twenty to forty years. AI may be faster, because it diffuses through software rather than physical capital and because it is being adopted by firms that have already digitised. It is unlikely to be instantaneous, because the binding constraints (chapter 3's institutional lag, chapter 6's bottleneck movement, chapter 9's reliability gate) are the same ones that slowed the earlier technologies.

*Returns are uneven.* Some sectors, firms and workers gain enormously and early; others gain late or lose. Averages conceal this. The useful question is never "will AI raise productivity?" but "whose, when, and who bears the adjustment?"

*Institutions lag and then catch up roughly.* Education, law, professional norms and labour markets adapt slowly and imperfectly, and their adaptation, not the technology, determines who bears the cost.

The base rates do not say that this time is the same. They say that anyone claiming this time is different has the burden of proof, and that the proof should come in the form of measurements, not demonstrations.

## A worked case: three forecasts, ten years on

The method's value is easiest to see on forecasts old enough to grade. Three from the mid-2010s, each made by serious people, each widely repeated, each gradable now.

**"47 per cent of US jobs are at high risk."** In 2013 two Oxford researchers estimated that about 47 per cent of US employment was in occupations at high risk of computerisation over "a decade or two".[^4] The number travelled around the world and is still quoted. Graded in 2026: US unemployment through the period was at or near historic lows, and no occupation-level collapse on anything like that scale occurred. The study was careful about what it measured (technical feasibility of automating an occupation's tasks, judged by experts) and the reporting was not: feasibility was read as displacement, occupations were read as jobs, and the time horizon dropped out of the headline. A 2016 analysis by the OECD that re-did the exercise at the level of tasks rather than occupations put the share of jobs at high risk at about 9 per cent, because most occupations contain tasks that are hard to automate alongside ones that are easy.[^5] Both numbers were defensible answers to different questions. The lesson is chapter 3's: exposure is not displacement, and a forecast that does not name its channel will be graded against the wrong one.

**"Stop training radiologists."** In 2016 one of the field's most distinguished researchers said that it was "quite obvious" that deep learning would outperform radiologists within five years and that training new ones should stop.[^6] Graded in 2026: image-recognition systems did reach and exceed radiologist-level performance on many specific, well-defined detection tasks, exactly as predicted; and radiologist employment, salaries and training places *rose*, with shortages reported in several countries. The capability forecast was largely right. The labour forecast was wrong, because the job was not the task: a radiologist's work includes integrating findings across modalities, handling the unusual case, communicating with clinicians, taking responsibility for the diagnosis, and the regulatory and liability structure that decides who may sign a report. The systems became tools used by radiologists, which raised their productivity and, through chapter 3's demand channel, the volume of imaging. The forecaster later said the timeline was wrong but the direction right; the more useful correction is that "outperform at the task" and "replace in the job" are different claims, and the distance between them is institutional, not technical.

**"Full self-driving next year."** From 2016 onward, a leading electric-vehicle company's chief executive predicted, roughly annually, that fully autonomous driving was about a year away.[^7] Graded in 2026: driver-assistance systems improved enormously; limited robotaxi services operated in a handful of cities under specific conditions; and general-purpose autonomy, in any weather on any road without a human responsible, had not arrived. The pattern of the forecast is itself instructive: a capability that was genuinely improving, a demonstration that genuinely worked in chosen conditions (chapter 1's "demos are not deployments"), and a reliability bar for unsupervised operation (chapter 9's arithmetic) that was far higher than the demonstrations suggested and that moved as the systems revealed new failure modes.

The three cases share a shape. In each, the technical trajectory was called roughly right and the consequence was called wrong, because the consequence ran through institutions (how jobs are bundled, who holds liability, what reliability is required before autonomy is granted) that the forecaster did not model. That is the base-rate lesson of this chapter applied to the recent past, and it is why this book has spent more pages on institutions than on capabilities. It is also a demonstration of the journal: each forecast, written down with the belief it rested on and a date, would have taught its author something precise about *which* belief failed. Repeated without the record, the same error is being made about the current wave by people who remember the earlier forecasts only as "the experts were wrong", which is the least useful possible lesson.

## The decision journal

The second part of the method is a record. The idea is old (it is standard practice among serious investors and forecasters) and it is simple enough that almost nobody does it.

Whenever you make a decision that depends on a belief about how this transition will go (what to study, what job to take, what to build, what to stop doing), write down four things: the decision, the belief it rests on, what evidence would change the belief, and a date to check. Then, on the date, check, and write down what actually happened and whether the belief was right.

Three things make the journal valuable.

It separates the quality of a decision from the quality of its outcome. A good decision can turn out badly and a bad one well; over many entries the record shows which beliefs are reliable and which are not, which no single outcome can.

It defeats hindsight. Memory rewrites itself to make past beliefs look more accurate than they were. A dated record does not. The experience of reading your own confident entry from two years ago and seeing how wrong it was is unpleasant and it is the single most effective training in calibration available.

It forces the question "what would change my mind?" at the moment of deciding, which is when it is most useful and least asked. Chapter 2's measurement discipline, chapter 9's checkpoints and this book's "what would make this wrong" sections are all versions of the same move: name the evidence before you see it.

The journal should be short. One paragraph per decision; one paragraph per check. A year of it will be more useful than any forecast anyone publishes, because it will be about your beliefs and your decisions, calibrated against your world.

## What this book expects to get wrong

Here, plainly, are the places this book is most likely to be wrong, in rough order of consequence.

**The speed of capability progress.** The book assumes continued but uneven improvement, with reliability lagging raw capability and agents constrained by the arithmetic of chapter 9. If the task-horizon trend that chapter 9 described continues to double every several months through 2030, systems will complete week-long professional tasks unattended within the decade, and large parts of chapters 4, 6, 9 and 10 will have been too conservative about what gets automated and how fast. If the trend bends, as trends usually do, the book will look about right. The evidence to watch is the measured horizon on realistic tasks, not demonstrations.

**The entry-level paradox.** The book argues that the narrowing of junior roles is real and durable and that the response is to be useful above the entry rung earlier. If firms instead redesign apprenticeship successfully, or if demand effects create more junior roles than automation removes, the paradox will have been a 2023–2027 adjustment rather than a feature of the decade. Watch hiring rates and wages for the youngest cohorts in exposed occupations, by year.

**India's trajectory.** Chapter 11 presents two halves and declines to predict which dominates. If the book is wrong about India it will most likely be wrong in the pessimistic direction: underestimating how fast the services industry adapts and how much the domestic product sector grows. The evidence is export figures, employment figures and the revenue of Indian-built AI products.

**Governance.** Chapter 7 expects continued divergence between jurisdictions and slow enforcement. A major incident could produce fast, convergent, strict regulation; a long quiet period could produce the opposite. The book does not know which, and says so.

**The information commons.** Chapter 8 expects the share of synthetic content to rise and the value of verified human work to rise with it. It could be wrong about the second half: the market might not reward verification as much as the argument requires, and provenance infrastructure might fail to reach the scale needed. Watch whether platforms, search engines and employers actually pay for provenance.

**The whole frame.** The book treats the transition as one that institutions and individuals can navigate with judgment, measurement and good habits. There are scenarios, at both tails, in which that frame is inadequate: a capability discontinuity that makes human judgment irrelevant across most of the economy, or a stall that makes the whole discussion premature. The book has argued that both tails are less likely than the broad middle and has given its reasons, in chapters 1, 3 and 9. Those reasons could be wrong.

A reader in 2031 who finds that this list missed the thing that actually mattered should treat that as the book's most important lesson rather than its failure: the things that matter most are often the things nobody put on the list, which is why the method (base rates, a record, named errors) matters more than any list.

## Ten habits

What follows is not a summary. It is the set of habits the preceding chapters have each, in their own way, recommended, collected so that they can be checked against.

1. **Ask which level, on which tasks, at what reliability.** Never "is it intelligent?" or "can it do my job?" (chapter 1).

2. **Read the evaluation before the claim.** Know what was measured, on what, by whom, and what was left out. Run one yourself (chapter 2).

3. **Think in tasks, not jobs, and watch wages, not headlines.** Decompose your own work; track what actually changes (chapters 3 and 4).

4. **Build proof that cannot be generated.** Work that runs, is checked, is accepted by others, or teaches. One piece per quarter (chapters 5 and 10).

5. **Make your work reproducible.** Code, data, method, limitations, every time. It is the unit of credibility now (chapter 6).

6. **Read the primary text.** The law, the paper, the specification, not the summary. It is almost always shorter and clearer than the commentary (chapter 7).

7. **Default to verification.** Sign what you publish; verify what you receive; agree protocols for anything that involves money, credentials or urgency (chapter 8).

8. **Delegate by *c*, *F* and *p*.** Delegate freely what is cheap to check, supervise what is costly to fail, and keep what you must do to stay able to judge (chapter 9).

9. **Compound, don't collect.** Judgment, systems, domain depth. Stop drilling what you will never do by hand (chapter 10).

10. **Keep the journal.** Write down the belief, the evidence that would change it, and the date. Check. Update (this chapter).

None of these habits depends on a product that could vanish, a prediction that could fail or a job that could disappear. That is the point. The decade ahead will be shaped by capabilities that nobody can forecast precisely and by institutional responses that nobody controls. What an individual controls is how they reason about evidence, how they prove what they can do, and how they update when they are wrong. Those were always the things that mattered. The transition has made them visible.

## What would make this chapter wrong

If the next decade turns out to resemble none of the previous general-purpose technologies in its diffusion pattern, with impact arriving in years rather than decades and spread evenly rather than unevenly, then the base-rate section misled by analogy and the discontinuity scenario the book discounted was the right one.

If keeping a decision journal and listing one's own errors turns out not to improve anyone's decisions, which is testable, then the method this chapter recommends is a comfort rather than a tool. The evidence from forecasting research so far says otherwise, and that evidence could be wrong.

## What to do this year

Start the journal today, with one entry: the most consequential decision you are making this year that depends on how this transition goes. Write the belief it rests on, the evidence that would change your mind, and a date twelve months from now. Then read chapter 1 again and check whether you still agree with it. Being wrong well is a practice, and the first entry is the hardest.

---

[^1]: David, P. A. (1990), "The Dynamo and the Computer: An Historical Perspective on the Modern Productivity Paradox", *American Economic Review* 80(2), 355–361.
[^2]: Solow, R. M. (1987), "We'd better watch out", review of Cohen & Zysman, *Manufacturing Matters*, *New York Times Book Review*, 12 July 1987, p. 36.
[^3]: Brynjolfsson, E., Rock, D. & Syverson, C. (2021), "The Productivity J-Curve: How Intangibles Complement General Purpose Technologies", *American Economic Journal: Macroeconomics* 13(1), 333–372.
[^4]: Frey, C. B. & Osborne, M. A. (2013), "The Future of Employment: How Susceptible Are Jobs to Computerisation?", Oxford Martin School working paper; published 2017 in *Technological Forecasting and Social Change* 114, 254–280.
[^5]: Arntz, M., Gregory, T. & Zierahn, U. (2016), "The Risk of Automation for Jobs in OECD Countries: A Comparative Analysis", OECD Social, Employment and Migration Working Papers No. 189.
[^6]: Geoffrey Hinton, remarks at the Machine Learning and Market for Intelligence conference, Toronto, October 2016, widely reported; see also Hinton's later comments revising the timeline (2023–2024).
[^7]: Public statements by Tesla's chief executive on the timeline for full self-driving capability, 2016–2024, as compiled in contemporaneous press coverage; graded against the deployment status of unsupervised autonomy in 2026.

### Sources for this chapter
- David (1990), *AER* 80(2) — electricity's forty-year lag.
- Solow (1987) — the productivity paradox remark.
- Brynjolfsson, Rock & Syverson (2021), *AEJ: Macro* 13(1) — the J-curve.
- Bresnahan, T. & Trajtenberg, M. (1995), "General purpose technologies: 'Engines of growth'?", *Journal of Econometrics* 65(1) — the GPT framework.
- Tetlock, P. E. & Gardner, D. (2015), *Superforecasting* — the evidence that recording and scoring beliefs improves calibration.
- Kwa et al. (2025), METR — the task-horizon measurement named as the number to watch.
