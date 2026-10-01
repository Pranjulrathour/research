# Appendix A — A one-page capability-reading checklist

Use this whenever you meet a claim that an AI system "can do" something: a press release, a benchmark result, a demo, a colleague's enthusiasm. Ten questions. If you cannot answer one, you do not yet know what the claim means.

1. **Which tasks, exactly?** Named, specific tasks, or a category? "Can code" is not a claim; "resolves 60% of a particular set of real repository issues under these conditions" is.

2. **At what reliability?** Pass rate, error rate, or distribution of outcomes. A system that is right 70% of the time is a different product from one that is right 99% of the time, and the claim should say which.

3. **Measured how?** Benchmark, human evaluation, deployment data, or demonstration. Demonstrations are selected; benchmarks can be trained on; human evaluation depends on who the humans were.

4. **Against what baseline?** Previous system, average human, expert human, or nothing. "Better than the previous version" and "better than an expert" are claims of a different order.

5. **Could the test have been in the training data?** If the benchmark is public and older than the model, assume partial contamination unless the evaluators say how they checked.

6. **Who ran the evaluation?** The developer, an independent group, or a regulator. Developer-run results are not worthless; they are a lower bound on scrutiny.

7. **What was the system allowed?** Tools, internet access, multiple attempts, a human in the loop, unlimited compute. A result with five attempts and a verifier is not a result with one attempt and none.

8. **What is the cost per task?** Time and money. A capability that costs a hundred times what a person costs is not yet an economic capability.

9. **What was left out?** Tasks the system fails at, conditions under which it was not tested, failure modes the report mentions in a footnote. The limitations section is the most informative part of any honest report.

10. **What would change if the claim is true?** For your work, your field, your plans. If the answer is "nothing", the claim is interesting but not actionable. If the answer is "a lot", go back to question 1 and check harder.

---

# Appendix B — The task-decomposition worksheet

From chapter 3. Do this for your own job, or for the job you are preparing for. It takes an hour and most people have never done it.

**Step 1. List the tasks.** Not the job title; the ten to twenty distinct activities that fill your working time. Be concrete: "write status reports", "debug production failures", "explain a design to a non-technical stakeholder", "clean data from a new source", "decide which of three vendor proposals to accept".

**Step 2. Estimate time share.** Roughly what fraction of your time each task takes. It will not add to 100 and that is fine.

**Step 3. Mark each task on three dimensions.**

| | Question to ask | Mark |
|---|---|---|
| **Exposure** | Can a current system produce an acceptable version of this output, given a clear specification? | High / Medium / Low |
| **Verification cost** | How hard is it to check whether the output is right? (chapter 9's *c*) | Cheap / Moderate / Expensive |
| **Failure cost** | What happens if the output is wrong and nobody catches it? (chapter 9's *F*) | Low / Medium / Severe |

**Step 4. Sort.** Three groups emerge.

- *High exposure, cheap verification, low failure cost* → these tasks will be delegated to tools, soon, and your time on them will fall. Do not build a career on them.
- *High exposure, expensive verification or severe failure cost* → these will be done with tools under supervision; the supervisor's judgment is the job. Learn to be the supervisor.
- *Low exposure* → framing, relationships, judgment under ambiguity, physical or institutional presence, novel problems. These are where your time will move. Get measurably better at them.

**Step 5. Find the new tasks.** What work would exist in your role if the first group took a tenth of the time it does now? Evaluation, integration, oversight, more of the third group, something nobody is doing yet. Name two.

**Step 6. Write the one-page plan** from chapter 10 using what you found.

Repeat yearly. The marks move.

---

# Appendix C — A reading list that will still be worth reading in 2031

Primary sources only; no commentary, no product documentation. Roughly in the order the book draws on them.

**On what "general" means and how to measure it**
- Morris, M. R. et al. (2024), "Levels of AGI for Operationalizing Progress on the Path to AGI", Google DeepMind / *ICML 2024*.
- Raji, I. D. et al. (2021), "AI and the Everything in the Whole Wide World Benchmark", *NeurIPS Datasets and Benchmarks*.
- Mitchell, M. et al. (2019), "Model Cards for Model Reporting", *FAT\* 2019*.
- Bengio, Y. et al. (2025, 2026), *International AI Safety Report*.

**On the economics**
- Acemoglu, D. & Restrepo, P. (2019), "Automation and New Tasks: How Technology Displaces and Reinstates Labor", *Journal of Economic Perspectives* 33(2).
- Autor, D. (2015), "Why Are There Still So Many Jobs?", *Journal of Economic Perspectives* 29(3); and (2024), "Applying AI to Rebuild Middle Class Jobs", NBER WP 32140.
- Eloundou, T., Manning, S., Mishkin, P. & Rock, D. (2023), "GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models".
- Brynjolfsson, E., Rock, D. & Syverson, C. (2021), "The Productivity J-Curve", *AEJ: Macroeconomics* 13(1).
- Brynjolfsson, E., Li, D. & Raymond, L. (2025), "Generative AI at Work", *Quarterly Journal of Economics* 140(2).
- David, P. A. (1990), "The Dynamo and the Computer", *American Economic Review* 80(2).

**On earlier transitions (the stories in this book)**
- Allen, R. C. (2009), "Engels' pause", *Explorations in Economic History* 46(4).
- Feigenbaum, J. & Gross, D. P. (2020, revised), "Automation and the Fate of Young Workers", NBER WP 28061.
- Levinson, M. (2006), *The Box: How the Shipping Container Made the World Smaller and the World Economy Bigger*.
- Eisenstein, E. L. (1979), *The Printing Press as an Agent of Change*; Buringh, E. & van Zanden, J. L. (2009), "Charting the 'Rise of the West'", *Journal of Economic History* 69(2).
- Olmstead, A. L. & Rhode, P. W. (2001), "Reshaping the Landscape: The Impact and Diffusion of the Tractor in American Agriculture", *Journal of Economic History* 61(3).
- Armstrong, S. & Sotala, K. (2012), "How We're Predicting AI, or Failing To".

**On learning**
- Bloom, B. S. (1984), "The 2 Sigma Problem", *Educational Researcher* 13(6).
- Freeman, S. et al. (2014), "Active learning increases student performance in science, engineering, and mathematics", *PNAS* 111(23).

**On science and reproducibility**
- Nosek, B. A. et al. (2015), "Promoting an open research culture", *Science* 348(6242).
- Jumper, J. et al. (2021), "Highly accurate protein structure prediction with AlphaFold", *Nature* 596.

**On governance**
- Regulation (EU) 2024/1689 (the AI Act): read Articles 3, 5, 6, 50 and Annex III.
- NIST (2023), *AI Risk Management Framework 1.0*.
- Digital Personal Data Protection Act, 2023 (India), and the 2025 Rules.

**On trust and security**
- C2PA, *Technical Specification* (current version).
- OWASP, *Top 10 for Large Language Model Applications* (current edition).
- Greshake, K. et al. (2023), "Not what you've signed up for", *AISec '23*.
- Shumailov, I. et al. (2024), "AI models collapse when trained on recursively generated data", *Nature* 631.

**On agents**
- Yao, S. et al. (2022), "ReAct: Synergizing Reasoning and Acting in Language Models".
- Kwa, T. et al. (2025), "Measuring AI Ability to Complete Long Tasks", METR.

**On judgment and being wrong well**
- Tetlock, P. E. & Gardner, D. (2015), *Superforecasting*.
- Kahneman, D. (2011), *Thinking, Fast and Slow*, especially Part III on overconfidence.

**On India**
- NASSCOM, *Strategic Review* (annual).
- ASER Centre, *Annual Status of Education Report* (annual).
- Reserve Bank of India and NPCI publications on digital public infrastructure.

---

# About the author

**Pranjul Rathour** is a generative-AI engineer from Kanpur, India. He builds production systems around large language models (retrieval, evaluation, agents and the reliability engineering that holds them together) and has won first prize at three hackathons for applied AI work. He has mentored more than two hundred students in India and abroad on careers in software and AI, which is where the questions this book tries to answer came from.

He writes about AI, engineering and careers at pranjulrathour.scult.in and publishes the code and data behind his research at github.com/Pranjulrathour. *Systems That Scale*, the companion to this volume, covers the engineering side of the same argument.

He can be reached at pranjulrathour41@gmail.com.
