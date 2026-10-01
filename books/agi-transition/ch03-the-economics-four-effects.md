# Chapter 3 — The economics: four effects, not one

Ask most people what AI will do to jobs and you will hear a single verb: replace. Ask most economists and you will hear four. The gap between those answers is the subject of this chapter, and closing it is the difference between planning for the next decade and panicking about it.

The one-verb story is not stupid. Some tasks that people are paid for today will be done by machines tomorrow, and the people who did them will not be paid for them. That is real, it is already happening, and chapter 4 takes it seriously. But a technology that can do a task also changes the value of the tasks around it, creates tasks that did not exist, and changes how much of the output people want. Those three effects are quieter than the first, they take longer to show up, and historically they have been larger. A framework that only has the first verb will get the decade wrong.

## The task framework

Start with a shift of unit. Economists who study automation stopped talking about jobs and started talking about tasks, because jobs are bundles of tasks and the bundles change. A bank teller in 1980 counted cash, verified identities, answered questions and sold products. The cash counting was automated by the ATM; the job did not disappear, it was rebundled toward the other three, and the number of tellers in the United States rose for two decades after ATMs spread, because cheaper branches meant more branches.[^1] Only in the 2010s, when online banking took the other tasks too, did teller employment fall.

That story contains the whole framework. Daron Acemoglu and Pascual Restrepo formalised it in a series of papers from 2018 onward: automation acts on tasks, and its effect on labour runs through four channels.[^2]

**Displacement.** A machine does a task a person used to do. Labour demand for that task falls. This is the one-verb story and it is the first-order effect of any automation technology.

**Productivity (augmentation).** The task is now cheaper or better, so the output is cheaper or better, so more of it is demanded, and so the people who do the *other* tasks in producing it are more valuable. The spreadsheet displaced the bookkeeper's arithmetic and made the analyst who could ask better questions of the numbers worth far more.

**New tasks.** The technology creates kinds of work that did not exist. Nobody was a web developer in 1990, a data scientist in 2005, or a prompt engineer in 2020. David Autor's work on "new work" estimates that most of the occupational titles that exist today were created after 1940, and that new-task creation has been the dominant source of employment growth across the twentieth century.[^3]

**Demand.** When the output gets cheaper, people buy more of it and spend the savings elsewhere, which creates work in other sectors. Cheaper lighting did not reduce the hours people spent in light; it multiplied them.

The net effect on any group of workers is the sum of the four, and the sum has a sign only after you have estimated each. The history of general-purpose technologies, from steam to electricity to computing, is one in which the first channel showed up fastest and loudest, and the other three determined the outcome.

## Exposure is not displacement

In 2023 a group of researchers published an estimate that about 80 per cent of the US workforce had at least 10 per cent of their tasks "exposed" to large language models, and about 19 per cent had half or more of their tasks exposed.[^4] The International Labour Organization and the International Monetary Fund followed with their own exposure studies, which found, among other things, that exposure is highest in high-income countries and in clerical work, and that in many jobs exposure is more likely to mean augmentation than replacement.[^5]

Those numbers were widely reported as "80 per cent of jobs at risk". They do not say that. *Exposure* in these studies means that a task could, in principle, be done at least twice as fast with the technology's help, with no loss of quality. That is a measurement of the first and second channels together, before the third and fourth have acted, and before anyone has checked whether the firm actually adopts the tool, whether the quality really holds, or whether the saved time is cut from headcount or redeployed. Exposure is the input to the four-channel calculation, not its output.

The exposure studies are genuinely useful. They tell you *where* the pressure will be felt first: clerical and administrative work, routine writing, customer support, parts of software development, parts of law and accounting. If your job is mostly those tasks, chapter 4 is about you. But the distance from exposure to displacement runs through adoption, reliability, regulation, retraining and the price of the output, and every one of those takes years.

## Where to look: wages, not headlines

If displacement is loud and the other three channels are quiet, how do you tell which is winning?

Watch wages and hours, by occupation and by task, over years. Headlines report layoffs, which are visible events with a date; they do not report the hires that happen because a firm's product got cheaper, which are diffuse and have no press release. The first channel generates news; the net effect generates statistics.

Three signals are worth tracking through the decade.

*Relative wages of exposed versus unexposed occupations.* If displacement dominates, exposed occupations lose ground. If augmentation dominates, they gain, because the people left in them are more productive. The early evidence from the 2023-2026 period is mixed and occupation-specific, which is exactly what the framework predicts for the first years.

*Entry-level hiring in exposed professions.* This is where displacement shows first, for reasons chapter 4 explains, and it is the signal most relevant to anyone currently a student.

*Output prices and volumes in exposed sectors.* If translation gets ten times cheaper, is ten times more translated? For lighting the answer was yes; for some services it may be no, because demand saturates. The demand channel's strength is sector-specific and it is the hardest of the four to see without looking.

Make a habit of distrusting any single number about "jobs" that is not accompanied by a time horizon, an occupation and a wage.

## Why history keeps showing all four at once

The ATM example is not an exception. Every general-purpose technology has run the same pattern, and the pattern has a shape worth knowing because you will live inside it.

Electrification took roughly forty years from the first power stations to measurable productivity gains in manufacturing, because factories had been built around a single central steam shaft and gained little from swapping it for a single central electric motor. The gains came when factories were redesigned around small motors at each workstation, which required new buildings, new workflows and a generation of managers who had grown up with the new possibility.[^6] The technology was ready decades before the institutions were.

Computing shows the same lag. Robert Solow's quip in 1987 that "you can see the computer age everywhere but in the productivity statistics" was accurate for another decade, until organisations had rebuilt processes around the machines rather than bolting machines onto old processes.[^7] Economists call the pattern the productivity J-curve: early investment in a new general-purpose technology shows up as cost without output, because the complementary investments (training, reorganisation, new business models) are intangible and take time, and then the curve turns.[^8]

AI will probably follow the shape, and probably faster than electricity, because it is software and spreads at the speed of a download rather than a construction project. But "faster than forty years" is not "instant", and the complementary investments are the same ones: redesigned workflows, retrained people, new institutions for trust and verification. The displacement channel acts at the speed of the download. The other three act at the speed of the redesign. The gap between those two speeds is the transition, and it is the subject of the rest of this book.

## A worked case: two field experiments

The channels are abstract until you watch them operate on real workers, and two of the first careful field studies of generative AI at work show the second channel, augmentation, in enough detail to see who gains and why.

The first followed 5,179 customer-support agents at a software company over about a year, as an AI assistant that suggested replies and surfaced documentation was rolled out to them in stages.[^9] The staggered rollout allowed the researchers to compare agents with and without the tool at the same time. Productivity, measured as issues resolved per hour, rose by about 14 per cent on average. The average concealed the finding that matters: the least experienced and lowest-performing agents improved by about 34 per cent, while the most experienced and highest-performing agents improved little or not at all. The assistant had, in effect, been trained on what the best agents did and was transferring it to the rest. Customer satisfaction rose, requests to speak to a manager fell, and new agents reached the productivity of experienced ones in a fraction of the time.

Read through the four channels: no agent was displaced during the study; the task was augmented; the output (resolved issues) got cheaper; and the gains went disproportionately to the people at the bottom of the skill distribution, which compressed the gap between novice and expert. That last effect is the one with the largest implications for chapter 4, because the thing the tool was doing (transferring the experts' tacit knowledge to juniors quickly) is the thing that apprenticeship used to do slowly, and it changes the value of experience in both directions: the experienced agent's edge shrank, and the novice's path to competence shortened.

The second study ran a controlled experiment with 758 consultants at a global consulting firm, giving some of them access to a frontier language model for a set of realistic tasks.[^10] On tasks within the system's capabilities (brainstorming, drafting, analysis of a kind the model handled well), consultants with the tool completed about 12 per cent more tasks, about 25 per cent faster, with output rated about 40 per cent higher in quality, and again the gains were largest for the consultants who had scored lowest beforehand. On a task deliberately chosen to sit just outside the system's capabilities (one that required integrating quantitative data with qualitative interview evidence in a way the model handled badly), consultants with the tool were about 19 percentage points *less* likely to reach the correct answer than those without it. The researchers called the boundary the "jagged frontier": the tools are strong and weak in a pattern that does not match human intuition about what is hard, and a worker who trusts them across the frontier does worse than one who has none.

Together the two studies say what the framework predicts and add a warning. Augmentation is real and large, it compresses skill differences, and it arrives before displacement. And its value depends entirely on the worker knowing where the frontier is, which is the verification skill that chapter 2 described and chapter 10 returns to. The tool makes the novice better. It makes the novice who cannot tell good output from plausible output worse. Both are true, and the difference between them is the skill the decade rewards.

## What this means for a person

The framework is not only for economists. It is a tool for deciding what to do with your own working life, and the exercise at the end of the chapter is the practical version. Three implications first.

If your current tasks are heavily exposed, the first channel is coming for them, and the question is which of your other tasks become more valuable as a result. The teller who moved toward selling and advising kept a job that the teller who insisted on counting cash did not.

If you can position yourself in the new-task channel, you are where the growth is. New tasks appear around a technology's edges: integrating it, verifying it, teaching it, governing it, fixing what it breaks, and doing the newly valuable things it makes possible. These are not glamorous at first and they are rarely called by their eventual names.

If you understand the demand channel in your own sector, you can see whether cheaper output means more work or less. Legal documents and medical images are things people will want more of when they are cheaper. Some outputs are not, and work in those sectors shrinks even as the technology improves.

None of this is reassurance. Displacement is real and it falls hardest on people with the least room to move. But a plan built on the one-verb story will put you in the wrong place; a plan built on four verbs has a chance of putting you in the right one.

## What would make this chapter wrong

The framework in this chapter assumes that new tasks continue to be created at a rate comparable to the past, and that the new tasks are ones people can do. If AI systems become able to perform new tasks as fast as they are created, the third channel closes, and with it most of the historical reassurance. This is the scenario in which "this time is different" is true, and it is not ruled out. A reader in 2031 should check whether the occupations that have grown fastest since 2026 are ones that AI systems also do.

The chapter also assumes the demand channel operates: that cheaper output is bought in greater quantity. If the sectors most exposed are ones where demand saturates quickly, the fourth channel is weak, and displacement is less offset than the framework suggests.

If, on the other hand, adoption has been much slower than exposure studies implied, because of reliability, regulation or cost, then the chapter's warnings about the first channel will look overstated, and the lesson is about the stubbornness of institutions rather than the speed of technology.

## What to do this year

Decompose your own job, or the job you are training for, into tasks. Write down ten to fifteen of them; be specific. For each one, mark it *exposed* (a current system could do it at least twice as fast with acceptable quality), *augmented* (a system makes you faster at it but cannot do it alone), or *new* (a task that exists because of the technology). Then ask two questions: which of the augmented and new tasks are you weakest at, and which do you most enjoy. The answer to the first tells you what to learn this year. The answer to the second tells you where you will be able to keep learning when the list changes, which it will.

---

[^1]: Bessen, J. (2015), *Learning by Doing: The Real Connection between Innovation, Wages, and Wealth*, Yale University Press, ch. 6, on bank tellers and ATMs.
[^2]: Acemoglu, D. & Restrepo, P. (2018), "The Race between Man and Machine: Implications of Technology for Growth, Factor Shares, and Employment", *American Economic Review* 108(6); and (2019), "Automation and New Tasks: How Technology Displaces and Reinstates Labor", *Journal of Economic Perspectives* 33(2).
[^3]: Autor, D., Chin, C., Salomons, A. & Seegmiller, B. (2024), "New Frontiers: The Origins and Content of New Work, 1940–2018", *Quarterly Journal of Economics* 139(3).
[^4]: Eloundou, T., Manning, S., Mishkin, P. & Rock, D. (2023), "GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models", arXiv:2303.10130.
[^5]: Gmyrek, P., Berg, J. & Bescond, D. (2023), *Generative AI and Jobs: A Global Analysis of Potential Effects on Job Quantity and Quality*, ILO Working Paper 96; Cazzaniga, M. et al. (2024), *Gen-AI: Artificial Intelligence and the Future of Work*, IMF Staff Discussion Note SDN/2024/001.
[^6]: David, P. A. (1990), "The Dynamo and the Computer: An Historical Perspective on the Modern Productivity Paradox", *American Economic Review* 80(2).
[^7]: Solow, R. (1987), "We'd Better Watch Out", *New York Times Book Review*, 12 July 1987.
[^8]: Brynjolfsson, E., Rock, D. & Syverson, C. (2021), "The Productivity J-Curve: How Intangibles Complement General Purpose Technologies", *American Economic Journal: Macroeconomics* 13(1).
[^9]: Brynjolfsson, E., Li, D. & Raymond, L. (2025), "Generative AI at Work", *Quarterly Journal of Economics* 140(2), 889–942; first circulated as NBER Working Paper 31161 (2023).
[^10]: Dell'Acqua, F. et al. (2023), "Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects of AI on Knowledge Worker Productivity and Quality", Harvard Business School Working Paper 24-013.

### Sources for this chapter
- Acemoglu & Restrepo (2018, 2019) — the task framework and its four channels.
- Autor, Chin, Salomons & Seegmiller (2024), *QJE* 139(3) — new work since 1940.
- Bessen (2015), *Learning by Doing* — the ATM and bank-teller case.
- Eloundou et al. (2023); Gmyrek, Berg & Bescond (2023), ILO WP 96; Cazzaniga et al. (2024), IMF SDN/2024/001 — exposure estimates and their interpretation.
- Brynjolfsson, Li & Raymond (2025), *QJE* 140(2); Dell'Acqua et al. (2023), HBS WP 24-013 — the two field experiments in the worked case.
- David (1990), *AER* 80(2); Solow (1987); Brynjolfsson, Rock & Syverson (2021), *AEJ: Macro* 13(1) — diffusion lags and the productivity J-curve.
