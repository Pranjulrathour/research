# Chapter 7 — Governance: who decides, and how

Every technology that mattered was governed in the end. Railways got signalling standards and liability rules after enough collisions. Electricity got wiring codes and licensed electricians after enough house fires. Aviation got an international body, incident reporting and a certification regime, which is a large part of why flying is now the safest way to travel. In each case the rules arrived late, were shaped by accidents, and came to be taken for granted by the people who benefited from them.

AI is being governed right now, in public, by a dozen jurisdictions at once, and the process is noisy enough that it's easy to mistake the noise for the substance. This chapter is about the substance. The legal instruments will keep changing (several changed while I was writing this), but the questions they answer keep coming back, and once you can see the questions you can read any new rule in a few minutes and tell whether it matters to you.

A word about dates. I name laws and the dates they took effect, as I promised at the start, because a reader in 2031 deserves to know what was on the table in 2026. But legislation moves and timetables slip, and something I describe as pending may have been delayed, amended or repealed by the time you read it. What follows is the state of play in October 2026. Check the primary text before you rely on any of it.

## Five questions underneath every rule

Strip away the legal drafting and nearly every AI governance instrument so far turns out to be a set of answers to the same five questions.

The first is which uses get treated differently. Most regimes sort AI systems by what they're used for and how much damage a failure could do, which is usually called a risk tier. A spam filter and a system that screens job applicants are both "AI", and no serious regime treats them the same way. The design choice is where the lines fall and who gets to draw them.

The second is what has to be disclosed, and to whom. Transparency duties come in layers: telling someone they're talking to a machine, labelling synthetic media, documenting how a system was built and tested, publishing a summary of the training data, reporting to a regulator. The choices here are how much is public versus confidential, and whether disclosure is required before deployment or only after something goes wrong.

The third is who checks, and what happens when things go wrong. This covers evaluation and incident reporting. Some regimes require testing before release, some only for the most capable systems, and some require serious incidents to be reported within days. The real decision is whether the checking is done by the developer, a third party or the state, and how much of it is binding.

The fourth is whether there's a size threshold. Several regimes single out the very largest models, and the usual proxy for "largest" is how much computation went into training, measured in floating-point operations. Compute thresholds are crude, since a smaller model trained more cleverly can be more capable, and they're used anyway because they're the one thing you can measure before the model exists.

The fifth is who pays when it fails. That's liability: whether existing product-liability and negligence law covers AI harms, whether it needs adapting, and how responsibility is split between whoever built the model, whoever deployed it and whoever used it.

Keep those five in mind and the comparison below turns from a maze into a table.

![The five questions, answered by four jurisdictions as of October 2026. A filled dot means a binding rule in force or enacted; a half dot means partial, sectoral, state-level or voluntary; an empty dot means no specific AI rule. Simplified; see the text for detail.](figures/fig07_five_questions.png)

## How the major jurisdictions have answered

### The European Union: one big law, with tiers and a threshold

The EU AI Act, Regulation (EU) 2024/1689, is the most complete answer anyone has written. It was published in July 2024, entered into force on 1 August 2024, and applies in stages.[^1]

Its risk tiers come in four kinds. Some uses are banned outright, including social scoring by public authorities and most real-time remote biometric identification in public spaces; those prohibitions applied from 2 February 2025. Then come high-risk systems, used in employment, education, credit, essential services, law enforcement, critical infrastructure and several other listed areas, which must meet requirements for risk management, data governance, documentation, human oversight and accuracy. Below them are limited-risk systems, which only carry transparency duties such as telling people they're dealing with a machine, and minimal-risk systems, which carry no new obligations at all.

On disclosure, providers of general-purpose AI models have to keep technical documentation, publish a summary of their training content and comply with copyright law. Those duties have applied since 2 August 2025, backed by a voluntary code of practice. Anyone deploying a system that generates synthetic content has to label it.

On checking, high-risk systems need a conformity assessment before they can be put on the market. General-purpose models above the systemic-risk threshold have to be evaluated, including through adversarial testing, and serious incidents have to be reported to the European AI Office.

The threshold itself: a general-purpose model is presumed to carry systemic risk if its training used more than 10^25 floating-point operations, a number the Commission can revise.

Liability sits in a separate instrument. A proposed AI Liability Directive was withdrawn in early 2025. The revised Product Liability Directive, (EU) 2024/2853, which explicitly covers software, is due to apply from December 2026.

One caveat on timing. Most of the high-risk obligations were scheduled to apply from 2 August 2026, some not until 2027. In late 2025 the Commission proposed, as part of a broader "digital omnibus" simplification package, to push back parts of that timetable and soften some duties. Whether and how that proposal was adopted is precisely the kind of thing to check in the primary text rather than in this book.

People often summarise the EU approach as "regulate the use, not the technology", and that's mostly fair. The general-purpose model rules and the compute threshold are the exceptions. They were added late in the negotiations, after the 2022–23 wave of large language models made it obvious that a few models were becoming inputs to thousands of different uses at once.

### The United States: no federal statute, a shifting executive, and the states

The US has no comprehensive federal AI law. What it has had is a run of executive actions that changed direction, a standards body doing patient, unglamorous work, and a growing patchwork of state laws.

Executive Order 14110, issued in October 2023, required developers of the most powerful models (those trained with more than 10^26 operations) to report safety-test results to the government, and told agencies across the administration to write guidance. It was rescinded in January 2025 and replaced by an order and then, in July 2025, an "AI Action Plan" aimed at removing what the administration saw as barriers to development and at competitiveness. The federal AI Safety Institute, set up inside NIST in late 2023, was renamed the Center for AI Standards and Innovation in mid-2025, with a remit that leaned towards standards and national security.[^2] In December 2025 another executive order set out to establish a national policy framework and to challenge state laws seen as conflicting with it.

Underneath all that churn, NIST's AI Risk Management Framework (version 1.0, January 2023) quietly became the standard reference for how American organisations describe AI risk. It's voluntary but widely used, and I'd bet it's the document most likely to still be in use in 2031.

The states filled the gap. Colorado passed the first comprehensive state law on high-risk AI used in consequential decisions (SB 24-205, signed in May 2024), though its effective date slipped from February to June 2026. California vetoed a frontier-model safety bill in 2024 (SB 1047) and then passed a narrower one in September 2025, SB 53, the Transparency in Frontier AI Act, which requires large frontier developers (defined by a 10^26 compute threshold plus a revenue test) to publish safety frameworks and report critical incidents. Texas enacted its Responsible AI Governance Act in 2025, effective January 2026, which is mostly about government use and certain prohibited purposes. Dozens of narrower state laws deal with election deepfakes, synthetic intimate images, chatbot disclosure and automated decisions in insurance and hiring.

Run that through the five questions and you get this: at the federal level, the answer to "which uses?" and "who checks?" is largely the market plus existing law; the states are answering "what must be disclosed?" one piece at a time; and the compute threshold survives in California even though it was dropped federally. The thing to watch through 2027 is the fight between federal pre-emption and the state rules.

### China: early, specific and administrative

China regulated specific AI behaviours earlier than anyone, and did it through administrative measures rather than one big statute. Rules on recommendation algorithms took effect in March 2022, rules on "deep synthesis" (synthetic media) in January 2023, and the Interim Measures for the Management of Generative AI Services in August 2023.[^3] Those measures require providers of public-facing generative services to register, carry out security assessments, label generated content and make sure outputs conform to specified values. Mandatory labelling of AI-generated content, with both visible marks and embedded ones, took effect on 1 September 2025, and amendments adding AI provisions to the Cybersecurity Law came into force at the start of 2026.

Through the five questions, China's tiers are defined by who is being served (public-facing services carry the heaviest duties) rather than by lists of uses. Disclosure is strong on labelling and registration. The state does the checking, through filing and assessment. There's no compute threshold. Liability runs through the existing civil code and the rules on platform responsibility. What's distinctive is speed, since administrative rules can be enforced quickly, and the fact that controlling content is a primary goal alongside safety.

### India: no AI statute, a data law, a mission and some advisories

So far India has chosen not to write a dedicated AI law. Its approach has four pieces.

The foundation is the Digital Personal Data Protection Act, 2023. Passed in August 2023, it governs how personal data is processed, including by AI systems, and is built around consent, purpose limitation and the rights of "data principals". Its implementing rules were notified in November 2025 with a phased timetable that runs into 2027, so its real effect on AI developers is arriving during exactly the period this chapter covers.[^4]

The IndiaAI Mission, approved in March 2024 with an outlay of about ₹10,372 crore, is industrial policy: subsidised compute, datasets, foundation-model development, skilling and funds for applications. It doesn't answer any of the five questions directly. It's the state deciding that capacity comes before constraint.

Then there are advisories and guidelines. In March 2024 the Ministry of Electronics and Information Technology issued an advisory asking platforms to label under-tested models and to guard against bias and election interference, and revised it within two weeks after industry objected. That was an early sign that India would reach for soft instruments before hard ones. In November 2025 the ministry published national AI governance guidelines built around principles rather than new legislation, which set up coordinating bodies and said existing laws would be applied to AI harms first.

The most concrete step came through amendments to the IT (Intermediary Guidelines) Rules on "synthetically generated information", notified in February 2026, which require platforms to label synthetic content and to deal with unlawful synthetic content within tight deadlines. India also hosted the global AI summit in February 2026, after Bletchley (November 2023), Seoul (May 2024) and Paris (February 2025), and used it to argue that AI governance should serve development and inclusion and not just risk reduction.

Through the five questions: India hasn't drawn risk tiers in law. Its disclosure duties are concentrated on synthetic media and personal data. Checking is voluntary and institutional, not mandatory. There's no compute threshold. Liability runs through the IT Act, the DPDP Act, consumer law and the ordinary law of negligence. For someone building in India in 2026, the practical rules are DPDP compliance, labelling synthetic content, and whatever the sector regulators require (the RBI in finance, the medical-devices regulator in health). That's less than the EU demands, and more than a lot of Indian builders seem to assume.

### The international layer

Above the national regimes sits a thin but real international layer. The G7's Hiroshima Process produced a voluntary code of conduct for advanced AI developers in October 2023. The Council of Europe opened the first binding international treaty on AI and human rights for signature in September 2024. A network of national AI safety institutes formed in November 2024. An *International AI Safety Report*, chaired by Yoshua Bengio and written by a panel drawn from many countries, published its first full edition in January 2025 and a second in early 2026; it's the nearest thing the field has to an IPCC-style assessment and is worth reading properly.[^5] And ISO/IEC 42001, published in December 2023, gives organisations a certifiable management-system standard for AI. I expect it to become what ISO 27001 became for information security, which is the thing procurement departments ask for.

None of this binds a developer directly. All of it shapes what the binding rules end up looking like.

## What the comparison shows

Lay the jurisdictions side by side and a few things stand out.

They agree on disclosure and on very little else. Every major regime now requires synthetic media to be labelled and people to be told when they're dealing with a machine. Beyond that, almost nothing is shared. Whether to draw risk tiers in law, whether to require testing before deployment, whether to use compute thresholds, whether to write a new liability regime: the answers differ and will probably keep differing. Labelling is the floor, and you should expect it everywhere.

The largest models are governed differently from everything else. The EU's systemic-risk tier, California's frontier-developer definition and the now-rescinded federal reporting rule all single out a handful of the most capable systems for duties that don't apply to anything else. That's new in technology regulation, and it reflects a specific worry: that a few models have become inputs to the whole economy, so their failures spread. If you build on top of such models rather than building them, these rules still reach you, indirectly, through the documentation and terms your provider is obliged to give you.

Enforcement trails enactment by years. The EU's bans applied in 2025 and its high-risk rules from 2026 at the earliest, so the first serious fines, court rulings and clarifying guidance will come through 2027 and 2028. India's data-protection rules phase in until 2027. Colorado's law only took effect in mid-2026. This decade will be shaped less by the texts than by how they're enforced, and enforcement is where most of the uncertainty is.

## What it means if you build things

If you're a student or an engineer rather than a policy person, governance reaches you in four practical ways.

Documentation is becoming part of the deliverable. Model cards, data statements, evaluation reports and risk assessments are turning from good practice into legal requirements in several markets. An engineer who can write a clear account of what a system does, what data it used, how it was tested and where it fails is doing compliance work and engineering work at the same time. It's the same discipline chapters 2 and 6 argued for, and the law is now catching up with it.

Provenance is a feature. Labelling synthetic content and carrying provenance metadata (chapter 8 covers the C2PA standard) is already required in several jurisdictions and expected in most. Build it in from the start instead of bolting it on.

In India, personal data is the constraint that actually bites. The DPDP Act, not any AI-specific law, is what's most likely to affect an Indian AI project in 2026 and 2027: what data you can collect, for which stated purpose, with what consent, and what you have to do when someone asks you to delete it. It's worth learning properly.

And sector rules come before general ones. A system built for a bank answers to the banking regulator before it answers to any AI rule, and the same goes for health, insurance, education and securities. If you want to work in finance, the AI governance that matters to you is the RBI's and SEBI's expectations on model risk, explainability and audit trails, which are older and more specific than anything else in this chapter.

## What would make this chapter wrong

If by 2031 a single international regime has emerged, with shared definitions, mutual recognition of assessments and common incident reporting, then my conclusion about divergence was too gloomy and the international layer achieved more than I expected. Check whether the safety-institute network or a treaty body ever acquired binding powers.

If compute thresholds have been abandoned everywhere because capability stopped tracking training compute closely enough to be useful, then the threshold sections describe a dead end. Check whether the EU revised or dropped its 10^25 figure and whether California's 10^26 test survived.

If the US has passed a comprehensive federal AI statute, or federal pre-emption has swept away the state laws, then my US section is a snapshot of a transition rather than a description of anything settled.

And if India has enacted a dedicated AI law with risk tiers and mandatory assessments, its "capacity before constraint" phase was shorter than I expected.

## What to do this year

Read one law's actual text, not a summary of it. Choose the one that applies where you live or want to work: Articles 5 and 6 and Annex III of the EU AI Act if you're aiming at Europe, the DPDP Act and its 2025 rules if you're building in India, Colorado's SB 24-205 or California's SB 53 if you're aiming at the US. Keep the five questions next to you and write down what the law actually says on each one. Then write a page on what it would require of a system you have built or want to build. You'll find the text more specific, more limited and more readable than the commentary about it, and you'll have a skill almost nobody brings to a technical interview.

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
