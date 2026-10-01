# Chapter 7 — Governance: who decides, and how

Every technology that mattered has been governed eventually. Railways got signalling standards and liability rules after enough collisions; electricity got wiring codes and licensed electricians after enough fires; aviation got an international body, incident reporting and a certification regime that is the reason flying is the safest way to travel. In each case the rules arrived late, were shaped by accidents, and were eventually taken for granted by the people who benefited from them.

AI is being governed now, in public, by a dozen jurisdictions at once, and the process is loud enough that it is easy to mistake the noise for the substance. This chapter is about the substance. The legal instruments will change (several changed while this book was being written) but the questions they answer recur, and if you can see the questions you can read any new rule in a few minutes and tell whether it matters to you.

A warning about dates. This chapter names laws and the dates they took effect, as this book promised to do, because a reader in 2031 deserves to know what was on the table in 2026. Legislation moves; timetables slip; a rule described here as pending may have been delayed, amended or repealed by the time you read this. The dates are the state of play as of October 2026. Check the primary text before relying on anything here.

## Five questions every AI rule answers

Strip away the drafting and almost every AI governance instrument so far is a set of answers to five questions.

**1. Which uses are treated differently?** Most regimes sort AI systems by what they are used for and how much harm a failure could do: a *risk tier*. A spam filter and a system that screens job applicants are both "AI", and no serious regime treats them alike. The design choice is where the lines fall and who draws them.

**2. What must be disclosed, to whom?** Transparency duties come in layers: telling a person they are interacting with a machine; labelling synthetic media; documenting how a system was built and tested; publishing summaries of training data; reporting to a regulator. The design choice is how much of this is public versus confidential, and whether it is required before deployment or only after harm.

**3. Who checks, and what happens when something goes wrong?** Evaluation and incident reporting. Some regimes require testing before release; some require it only for the most capable systems; some require that serious incidents be reported within days. The design choice is whether checking is done by the developer, by a third party, or by the state, and how much of it is binding.

**4. Is there a size threshold?** Several regimes single out the largest models, and the most common proxy for "largest" is the amount of computation used in training, measured in floating-point operations. Compute thresholds are crude (a smaller model trained better can be more capable) and they are used because they are measurable before the model exists, which nothing else is.

**5. Who pays when it fails?** Liability. Whether existing product-liability and negligence law covers AI harms, whether it needs adapting, and where responsibility sits between the developer of a model, the company that deploys it, and the person who used it.

Hold these five in your head and the jurisdiction comparison below becomes a table rather than a maze.

## How the major jurisdictions answered

### The European Union: a comprehensive law with tiers and thresholds

The EU AI Act, Regulation (EU) 2024/1689, is the most complete answer anyone has written. It was published in July 2024, entered into force on 1 August 2024, and applies in stages.[^1]

*Risk tiers.* Four: unacceptable (banned outright, including social scoring by public authorities and most real-time remote biometric identification in public spaces), high-risk (systems used in employment, education, credit, essential services, law enforcement, critical infrastructure and several other listed areas, which must meet requirements for risk management, data governance, documentation, human oversight and accuracy), limited-risk (transparency duties only, such as telling people they are talking to a machine) and minimal-risk (no new obligations). The prohibitions applied from 2 February 2025.

*Disclosure.* Providers of general-purpose AI models must keep technical documentation, publish a summary of training content and comply with copyright law; these duties applied from 2 August 2025, supported by a voluntary code of practice. Deployers of systems that generate synthetic content must label it.

*Checking.* High-risk systems need a conformity assessment before being placed on the market. General-purpose models above the systemic-risk threshold must be evaluated, including adversarial testing, and serious incidents must be reported to the European AI Office.

*Threshold.* A general-purpose model is presumed to carry systemic risk if its training used more than 10^25 floating-point operations, a figure the Commission can revise.

*Liability.* Handled separately. A proposed AI Liability Directive was withdrawn in early 2025; the revised Product Liability Directive (EU) 2024/2853, which explicitly covers software, is due to apply from December 2026.

*Timetable caveat.* Most high-risk obligations were scheduled for 2 August 2026, with some extending to 2027. In late 2025 the Commission proposed, as part of a wider "digital omnibus" simplification package, to push back parts of the high-risk timetable and ease some duties. Whether and how that was adopted is exactly the kind of fact to check in the primary text rather than in this book.

The EU's approach is often summarised as "regulate the use, not the technology", and that is mostly right; the general-purpose model rules and the compute threshold are the exceptions, added late in the negotiation after the 2022–23 wave of large language models made it clear that some models are inputs to thousands of uses at once.

### The United States: no federal statute, a changing executive stance, and the states

The US has passed no comprehensive federal AI law. What it has had is a sequence of executive actions that reversed direction, a standards body doing patient work, and a growing patchwork of state laws.

Executive Order 14110 (October 2023) required developers of the most powerful models (training compute above 10^26 operations) to report safety-test results to the government and directed agencies across the administration to produce guidance. It was rescinded in January 2025 and replaced by an order and, in July 2025, an "AI Action Plan" oriented toward removing perceived barriers to development and toward competitiveness. The federal AI Safety Institute, created within NIST in late 2023, was renamed the Center for AI Standards and Innovation in mid-2025 with a remit emphasising standards and national security.[^2] In December 2025 a further executive order sought to establish a national policy framework and to challenge state laws seen as conflicting with it.

Beneath the executive churn, NIST's AI Risk Management Framework (version 1.0, January 2023) became the de facto reference for how American organisations describe AI risk, voluntary but widely adopted, and it is the document most likely to still be in use in 2031.

The states filled the gap. Colorado passed the first comprehensive state law on high-risk AI in consequential decisions (SB 24-205, signed May 2024), with its effective date pushed from February to June 2026. California vetoed a frontier-model safety bill in 2024 (SB 1047) and then enacted a narrower one in September 2025 (SB 53, the Transparency in Frontier AI Act) requiring large frontier developers, defined by a 10^26 compute threshold and a revenue test, to publish safety frameworks and report critical incidents. Texas enacted its Responsible AI Governance Act in 2025, effective January 2026, focused mainly on government use and on prohibited intents. Dozens of narrower state laws cover deepfakes in elections, synthetic intimate imagery, chatbot disclosure and automated decisions in insurance and employment.

Read through the five questions: the US federal answer to "which uses?" and "who checks?" is largely "the market and existing law", the states are answering "what must be disclosed?" piece by piece, and the compute threshold survives in California even though it was dropped federally. The tension between federal pre-emption and state rules is the thing to watch through 2027.

### China: early, specific, and administrative

China regulated specific AI behaviours earlier than anyone, through administrative measures rather than a single statute. Rules on algorithmic recommendation took effect in March 2022, rules on "deep synthesis" (synthetic media) in January 2023, and the Interim Measures for the Management of Generative AI Services in August 2023, which require providers of public-facing generative services to register, to conduct security assessments, to label generated content and to ensure outputs align with specified values.[^3] Mandatory labelling measures for AI-generated content, with both visible and embedded marks, took effect on 1 September 2025, and amendments to the Cybersecurity Law adding AI provisions took effect at the start of 2026.

Through the five questions: China's tiers are defined by *who is served* (public-facing services face the heaviest duties) rather than by use-case lists; disclosure is strong on labelling and registration; checking is done by the state through filing and assessment; there is no compute threshold; liability runs through the existing civil code and platform-responsibility rules. The regime's distinctive feature is that it is enforceable quickly, because it is administrative, and that content control is a first-class objective alongside safety.

### India: no AI statute, a data law, a mission, and advisories

India has chosen, so far, not to write a dedicated AI law. Its approach has four parts.

*The Digital Personal Data Protection Act, 2023* is the foundation. Passed in August 2023, it governs the processing of personal data, including by AI systems, around consent, purpose limitation and the rights of "data principals". Its implementing rules were notified in November 2025 with a phased timetable running to 2027, so the Act's practical effect on AI developers is arriving during the period this chapter covers.[^4]

*The IndiaAI Mission*, approved in March 2024 with an outlay of about ₹10,372 crore, is an industrial policy: subsidised compute, datasets, foundation-model development, skilling and application funds. It answers none of the five questions directly; it is the state deciding that capacity comes before constraint.

*Advisories and guidelines.* In March 2024 the Ministry of Electronics and Information Technology issued an advisory asking platforms to label under-tested models and to prevent bias and election interference, revised within two weeks after industry pushback; it was an early sign that India would use soft instruments before hard ones. In November 2025 the ministry published national AI Governance Guidelines built around principles rather than new law, establishing coordinating institutions and stating that existing laws would be applied to AI harms first.

*Intermediary rules.* The most concrete step came through amendments to the IT (Intermediary Guidelines) Rules on "synthetically generated information", notified in February 2026, which require platforms to label synthetic content and to act on unlawful synthetic content within tight deadlines. India also hosted the global AI summit series in February 2026, following Bletchley (November 2023), Seoul (May 2024) and Paris (February 2025), and used it to press the case that AI governance should serve development and inclusion, not only risk reduction.

Through the five questions: India has not drawn risk tiers in law; its disclosure duties are concentrated on synthetic media and on personal data; checking is voluntary and institutional rather than mandatory; there is no compute threshold; liability runs through the IT Act, the DPDP Act, consumer law and the ordinary law of negligence. For a developer in India the practical rules in 2026 are DPDP compliance, synthetic-content labelling, and whatever sector regulators (the RBI for finance, the medical-devices regulator for health) require. That is less than the EU demands and more than many Indian builders assume.

### The international layer

Above the jurisdictions sits a thin but real international layer. The G7's Hiroshima Process produced a voluntary code of conduct for advanced AI developers in October 2023. The Council of Europe opened the first binding international treaty on AI and human rights for signature in September 2024. A network of national AI safety institutes formed in November 2024. An *International AI Safety Report*, chaired by Yoshua Bengio and written by a panel drawn from many countries, published its first full edition in January 2025 and a second in early 2026; it is the closest thing the field has to an IPCC-style assessment and it is worth reading in full.[^5] ISO/IEC 42001, published in December 2023, gives organisations a certifiable management-system standard for AI, and it is becoming what ISO 27001 became for information security: the thing procurement departments ask for.

None of this binds a developer directly. All of it shapes what the binding rules will look like.

## What the comparison tells you

Three things stand out when the jurisdictions are laid side by side.

**Convergence on disclosure, divergence on everything else.** Every major regime now requires that synthetic media be labelled and that people be told when they are dealing with a machine. Almost nothing else is shared. Whether to draw risk tiers in law, whether to test before deployment, whether to use compute thresholds, whether to write a new liability regime: the answers differ and are likely to keep differing. Labelling is the floor; expect it everywhere.

**The largest models are governed differently from everything else.** The EU's systemic-risk tier, California's frontier-developer definition and the (rescinded) federal reporting rule all single out a handful of the most capable systems for duties that do not apply to the rest. This is new in technology regulation and it reflects a specific worry: that a few models are inputs to the whole economy and that their failures propagate. If you build *on* such models rather than building them, these rules reach you indirectly, through the documentation and terms your provider must offer.

**Enforcement lags enactment by years.** The EU's prohibitions applied in 2025 and its high-risk rules in 2026 at the earliest; the first serious fines, the first court interpretations and the first clarifying guidance will arrive through 2027 and 2028. India's DPDP rules phase in to 2027. Colorado's law took effect in mid-2026. The decade will be shaped less by the texts than by how they are enforced, and enforcement is where the uncertainty lives.

## What it means for someone building things

If you are a student or an engineer rather than a policy person, the governance layer touches you in four practical ways.

**Documentation is becoming a deliverable.** Model cards, data statements, evaluation reports and risk assessments are moving from good practice to legal requirement in several markets. The engineer who can write a clear account of what a system does, what data it used, how it was tested and where it fails is doing compliance work and engineering work at once. This is the same discipline chapters 2 and 6 argued for; the law is catching up to it.

**Provenance is a feature.** Labelling synthetic content and carrying provenance metadata (chapter 8 covers the C2PA standard) is now required in several jurisdictions and expected in most. Build it in rather than bolting it on.

**Personal data is the live constraint in India.** The DPDP Act, not any AI law, is the rule most likely to affect an Indian AI project in 2026 and 2027: what data you may collect, for what stated purpose, with what consent, and what you must do when someone asks you to delete it. Learn it.

**Sector rules outrank general ones.** A system for a bank is governed by the banking regulator before it is governed by any AI rule; the same for health, insurance, education and securities. If you want to work in finance, the relevant AI governance is the RBI's and SEBI's expectations on model risk, explainability and audit trails, and those expectations are older and more specific than anything in this chapter.

## What would make this chapter wrong

If by 2031 a single international regime has emerged, with aligned definitions, mutual recognition of assessments and a shared incident-reporting system, then the "divergence on everything else" conclusion was too pessimistic and the international layer did more than expected. Check whether the safety-institute network or a treaty body acquired binding powers.

If the compute-threshold approach has been abandoned everywhere, because capability stopped tracking training compute closely enough to be useful, then the section on thresholds describes a dead end. Check whether the EU revised or dropped its 10^25 figure and whether California's 10^26 test survived.

If the US has enacted a comprehensive federal AI statute, or if federal pre-emption has swept away the state laws, then the US section is a snapshot of a transition rather than a description of a settled pattern.

If India has enacted a dedicated AI law with risk tiers and mandatory assessment, then India's "capacity before constraint" period was shorter than this chapter expected.

## What to do this year

Read one law's actual text, not a summary. Pick the one that governs where you live or where you want to work: the EU AI Act's Articles 5 and 6 and Annex III if you are aiming at Europe; the DPDP Act and its 2025 rules if you are building in India; Colorado's SB 24-205 or California's SB 53 if you are aiming at the US. Read it with the five questions beside you and write down, for each, what the law actually says. Then write one page on what it would require of a system you have built or want to build. You will find that the text is more specific, more limited and more readable than the commentary, and you will have a skill that almost nobody in a technical interview has.

---

[^1]: Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 (Artificial Intelligence Act), *Official Journal of the European Union*, 12 July 2024. Entry into force 1 August 2024; staged application per Article 113.
[^2]: Executive Order 14110, "Safe, Secure, and Trustworthy Development and Use of Artificial Intelligence", 30 October 2023, rescinded 20 January 2025; Executive Order 14179, "Removing Barriers to American Leadership in Artificial Intelligence", 23 January 2025; "America's AI Action Plan", July 2025; US Department of Commerce announcement of the Center for AI Standards and Innovation, June 2025.
[^3]: Cyberspace Administration of China, *Interim Measures for the Management of Generative Artificial Intelligence Services*, effective 15 August 2023; *Measures for Labeling AI-Generated Synthetic Content*, effective 1 September 2025.
[^4]: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023), assented 11 August 2023; Digital Personal Data Protection Rules, 2025, notified November 2025.
[^5]: Bengio, Y. et al. (2025), *International AI Safety Report*, January 2025, and second edition, February 2026.

### Sources for this chapter
- Regulation (EU) 2024/1689 (AI Act), OJ L, 12 July 2024 — text, Annex III, Article 113 timetable; Directive (EU) 2024/2853 on liability for defective products.
- US: EO 14110 (2023); EO 14179 (2025); *America's AI Action Plan* (July 2025); NIST *AI Risk Management Framework 1.0* (January 2023); Colorado SB 24-205 (2024); California SB 53 (2025); Texas HB 149 (2025).
- China: CAC Interim Measures on Generative AI (2023); Deep Synthesis Provisions (2023); Algorithmic Recommendation Provisions (2022); Labeling Measures (2025).
- India: DPDP Act 2023 and DPDP Rules 2025; IndiaAI Mission cabinet approval, 7 March 2024; MeitY advisory of 1 March 2024 and revision of 15 March 2024; MeitY *India AI Governance Guidelines*, November 2025; IT (Intermediary Guidelines and Digital Media Ethics Code) Amendment Rules on synthetically generated information, February 2026.
- International: Bletchley Declaration (November 2023); Seoul (May 2024), Paris (February 2025) and New Delhi (February 2026) summits; Council of Europe Framework Convention on AI (opened for signature 5 September 2024); G7 Hiroshima Process Code of Conduct (October 2023); ISO/IEC 42001:2023; *International AI Safety Report* (2025, 2026).
