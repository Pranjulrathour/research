# Chapter 8 — Trust, security and the information commons

In early 2024 an employee at the Hong Kong office of a multinational engineering firm joined a video call with what appeared to be the company's chief financial officer and several colleagues, and on their instructions transferred about HK$200 million (roughly US$25 million) to a set of accounts. Every other person on the call was synthetic. The faces and voices had been generated from publicly available footage, and the employee, who had initially suspected a phishing email, was reassured precisely because the people on the call looked and sounded like the people they claimed to be.[^1]

The case is useful because it is not about a gullible person. It is about an assumption that had been safe for the whole of human history and quietly stopped being safe: that a face and a voice you recognise, moving and speaking in real time, belong to the person they belong to. For most of the past decade that assumption has been load-bearing in banking, journalism, politics, family life and ordinary courtesy. This chapter is about what replaces it, and about two other shifts in the same family: the new attack surface created when software starts to act on our behalf, and what happens to shared public knowledge when most new text on the internet is written by machines.

The thread running through all three is the same. When producing a convincing artefact becomes cheap, the artefact stops being evidence, and the weight moves to *provenance*: where did this come from, who signed it, and can that be checked? That is a shift in habits as much as in technology, and the habits are the part you can control.

## Synthetic media and the end of "seeing is believing"

Three facts set the terms.

First, synthetic audio, image and video are now good enough to fool attentive people in ordinary conditions, and the quality is still improving. Audio is the most dangerous because it needs the least data (a few seconds of a voice suffice for a usable clone) and because telephone audio was already low-fidelity, so artefacts hide easily.

Second, the cost has collapsed to roughly zero. A voice clone, a face swap on a live call or a photorealistic image of an event that did not happen can be produced by a person with no technical skill in minutes, on a phone.

Third, detection does not scale. Tools that try to classify media as real or synthetic from the content alone are in an arms race they are structurally positioned to lose, because every improvement in detection is a training signal for the next generator, and because a detector that is wrong one time in twenty is useless for the decisions that matter. Detection remains helpful as one signal among several for a trained investigator; it is not a solution for the public.

What follows from these three facts is that the burden has to move from the receiving end (can I tell this is fake?) to the producing end (can this prove where it came from?). That is what provenance infrastructure tries to do.

### Provenance: C2PA and Content Credentials

The main open standard is the one developed by the Coalition for Content Provenance and Authenticity (C2PA), a body formed in 2021 by a group including Adobe, Microsoft, the BBC, Intel and Arm, whose first specification was published in January 2022.[^2] The mechanism is conceptually simple. When a piece of media is created or edited, the device or software attaches a cryptographically signed manifest recording who made it, with what tool, and what edits were applied; each subsequent edit adds a signed entry. A viewer can inspect the chain ("Content Credentials") and verify the signatures. If the manifest is intact and the signer is trusted, you know the asset's history. If the manifest is missing, you know only that: it is missing.

Adoption moved from standards to products between 2023 and 2026. Cameras began signing images at capture (the first consumer camera with built-in Content Credentials shipped in late 2023, and mainstream phones followed). Major image generators began attaching provenance metadata to their outputs. Several large social platforms began reading the metadata and labelling content accordingly. The EU AI Act's transparency provisions, applying from 2026, require that AI-generated content be marked in a machine-readable way, which pushes the whole ecosystem toward some such standard whether or not it is C2PA.

Alongside signed manifests sits *watermarking*: embedding a signal in the generated content itself, imperceptible to people but detectable by a tool that knows the key. Google DeepMind's SynthID family, introduced from 2023 and partly open-sourced in 2024, is the best-known example. Watermarks survive some edits that strip metadata; they are also removable by a determined adversary and they only mark content from generators that choose to watermark.

Two limits matter more than any technical detail.

Provenance proves the *origin* of signed content. It says nothing about unsigned content, which is most of the internet and all of history. A world with widespread provenance is a world where trustworthy content can prove itself; it is not a world where untrustworthy content is caught. The practical consequence is a norm shift: from "assume real unless shown fake" to "assume unverified unless shown real". That norm is uncomfortable and it is where things are heading.

And provenance is only as good as the signing keys and the organisations behind them. A signed manifest from an unknown signer proves nothing. The trust infrastructure (who is allowed to sign, how keys are revoked, how a viewer knows which signers to trust) is the hard part, and it is being built now, the way certificate authorities were built for the web in the late 1990s, with all of the same failure modes to come.

### The human protocol

Technology sets the floor; habits decide what actually happens. The habits that were already standard in security-conscious organisations are becoming universal, and the family version of them was recommended publicly by law-enforcement agencies in 2024: a shared secret word for emergencies, callback verification on a known number before acting on any urgent request for money or credentials, and a standing rule that urgency itself is a warning sign.[^3] In institutions, the equivalents are out-of-band confirmation for payments above a threshold, signed communication for instructions that move money or data, and the principle that no single channel is sufficient authorisation for an irreversible act.

None of this is new. What is new is that it now applies to everyone, including people who have never thought of themselves as a target, because the cost of targeting them has fallen below the value of what they can be made to do.

## When software acts: the new attack surface

The second shift is subtler and, for anyone who builds software, more immediate.

Until recently, software followed instructions from its developer and from its user, and the two were separable: the developer wrote the code, the user supplied the data, and the data could not change what the code did. Language-model systems blur that line by design. The model receives instructions and data in the same channel, as text, and it cannot reliably tell them apart. Any text the model reads (a web page, an email, a document, a search result) can contain instructions that the model may follow.

This is *prompt injection*, named in 2022, and ranked first in the OWASP Top 10 for Large Language Model Applications from its first edition in 2023 through its subsequent revisions.[^4] The *indirect* form, where the malicious instruction sits in content the system retrieves rather than in what the user typed, was described formally in 2023 and is the one that matters for agents: a system that reads your email to summarise it can be told, by an email, to forward your inbox somewhere; a system that browses the web to answer a question can be told, by a web page, to visit a URL that leaks what it knows.

Three things make this harder than the injection attacks of the past.

There is no known complete defence. SQL injection was solved, in principle, by separating code from data at the interface. Language models have no such interface; the instructions and the data are the same kind of thing. Mitigations exist and are improving (instruction hierarchies, input filtering, output constraints, separate models for untrusted content), and none of them is a guarantee. A system that reads untrusted text has to be designed on the assumption that it will sometimes follow instructions in that text.

The harm scales with what the system can do. A chatbot that can only reply is embarrassing when it is injected. A system that can send email, move money, modify files or call other systems is dangerous. The most useful summary of when the danger is acute is the combination of three properties: access to private data, exposure to untrusted content, and the ability to communicate externally. A system with all three is a system that can be made to exfiltrate what it knows, and the combination should be treated as a design smell in the way that "stores passwords in plain text" is.[^5]

The user often cannot see the attack. The injected instruction may be white text on a white background, a comment in a file, a string in a tool's output. The user asked for a summary and received one; the exfiltration happened in between.

### What this means for building

For anyone who writes software that touches a language model, which will be most people in the field by the end of the decade, the discipline is a security discipline and it is already fairly clear.

*Least privilege, strictly.* An agent gets the narrowest permissions that let it do its job, scoped per task, revocable, and separate from the user's own credentials wherever possible. "It needs to read the inbox" does not imply "it may send mail".

*Treat all retrieved content as hostile.* Text from the web, from documents, from other systems' outputs and from other agents is data, never instruction. Design so that an attacker who controls that text can do no more than corrupt the answer.

*Human confirmation for irreversible actions.* Sending, paying, deleting, publishing, granting access: a person approves each one, and the approval is specific, not a blanket "yes" given at the start. This is slower and it is the price of safety until the systems earn more trust, which chapter 9 discusses.

*Log everything and assume you will need the log.* When an incident happens, and one will, the question is what the system read, what it decided and what it did. If you cannot answer, you cannot fix it.

*Evaluate adversarially.* A system tested only on cooperative inputs is untested. Red-teaming, injection test suites and the habit of asking "what happens if this page is malicious?" are part of the build, not an afterthought.

For a student aiming at a security or an infrastructure role, this is among the most promising areas of the decade: a genuinely new class of vulnerability, no settled solution, enormous deployment, and a shortage of people who understand both the machine-learning side and the security side. Chapter 10 returns to that.

## The information commons after the flood

The third shift is slower and affects everyone who reads.

For about thirty years the public web grew by human effort. People wrote pages, answered questions on forums, maintained encyclopaedias, published code and argued in comment threads, and that accumulation became the training corpus for the systems that now write a growing share of new text. Three consequences are already visible.

**Volume without provenance.** Machine-written text is cheap and indistinguishable from the human kind at a glance, so the share of new public text that is synthetic is rising, with no reliable way to measure it. Search engines, which ranked by signals of human attention and link structure, are coping unevenly; the result is more plausible, generic, lightly-sourced pages competing for the same queries, and a harder time finding the one page written by someone who actually knew.

**The feedback problem.** Systems trained on web text will increasingly be trained on text produced by earlier systems. Research published in 2024 showed that models trained recursively on their own outputs degrade, losing the tails of the distribution first (the rare, specific, surprising content) and converging toward the bland centre.[^6] The result is not automatic (curation, filtering and human data can prevent it), but it means that *human-generated, verified, specific* content becomes more valuable as training data and as reference material, not less, because it is the thing the systems cannot produce for themselves.

**The commons that fed the models is shrinking.** Community question-and-answer sites saw large declines in new questions after 2022, as people asked models instead; the models had been trained on those very sites. Publishers and infrastructure providers began blocking AI crawlers by default in 2025 and experimenting with paid access. The free, open, human-written web that made the current systems possible is being enclosed on one side and diluted on the other. What replaces it as the substrate for public knowledge is an open question, and the answer will involve money, licensing and law as much as technology.

The implication for a reader is the same one that has run through this book since chapter 2. When plausible text is free, the scarce goods are *originality* (something not already on the web), *verification* (something checked against the world) and *accountability* (a named person who stands behind it). Search engines are trying to reward these; readers are learning to look for them; institutions that certify them (journals, newsrooms, professional bodies) are regaining some of the authority they had lost. Original, verified, signed work rises in value exactly because the alternative is now infinite.

For someone building a public reputation, which chapter 10 treats as part of the personal strategy for the decade, this is the whole game. Write what is not already written. Show your checking. Sign your name.

## What would make this chapter wrong

If by 2031 content provenance has become near-universal, with most cameras, phones, platforms and generators signing and displaying credentials and a working trust infrastructure behind them, then the "assume unverified" norm will have arrived faster and more comfortably than this chapter expects, and the warnings about key management and adoption gaps were too cautious. Check the share of major-platform content carrying verifiable credentials.

If prompt injection has been substantially solved, through architectures that genuinely separate instruction from data, then the agent-security section describes a transitional problem. Check whether the OWASP list still ranks it first and whether major incidents have declined despite wider deployment.

If the information commons has been rebuilt on new terms (licensed human content, sustainable compensation for contributors, provenance-ranked search) and public knowledge is demonstrably healthier than in 2026, then the "flood" framing was too pessimistic. Check contribution rates to the large open projects and the measured share of synthetic text in search results.

If, on the other hand, a major democratic election has been visibly swung by synthetic media, or a large institution has been taken down by an injected agent, then this chapter understated the near-term harms, and the habits it recommends were more urgent than it made them sound.

## What to do this year

Adopt provenance and verification habits in your own publishing. Sign what you publish: put your name and a stable identity on your work and keep an authoritative home for it. Where tools allow, attach content credentials to the images and documents you produce. Cite primary sources with dates and check that they exist. Agree a verification protocol with your family and your team for any request involving money, credentials or urgency, and use it even when it feels silly. If you build software that uses a language model, write down, before you ship, what text it reads from untrusted sources and what the worst thing is that text could make it do; if the answer is unacceptable, change the design. You will be ahead of most of the industry.

---

[^1]: Hong Kong Police press briefing, 4 February 2024, as reported by RTHK, CNN and the *South China Morning Post*; the firm was later identified in press reports as Arup.
[^2]: Coalition for Content Provenance and Authenticity, *C2PA Technical Specification*, version 1.0, January 2022, and subsequent 2.x releases, c2pa.org.
[^3]: US Federal Bureau of Investigation, Public Service Announcement I-120324-PSA, "Criminals Use Generative Artificial Intelligence to Facilitate Financial and Romance Fraud", 3 December 2024.
[^4]: OWASP Foundation, *OWASP Top 10 for Large Language Model Applications*, version 1.0 (August 2023) and the 2025 edition; Greshake, K. et al. (2023), "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection", *AISec '23*.
[^5]: Willison, S. (2025), "The lethal trifecta for AI agents: private data, untrusted content, and external communication", simonwillison.net, 16 June 2025.
[^6]: Shumailov, I. et al. (2024), "AI models collapse when trained on recursively generated data", *Nature* 631, 755–759.

### Sources for this chapter
- C2PA Technical Specification (2022–2025); Content Authenticity Initiative documentation.
- Google DeepMind, SynthID (2023); "SynthID-Text" open-source release and *Nature* paper, Dathathri et al. (2024), *Nature* 634.
- Regulation (EU) 2024/1689, Article 50 (transparency obligations for synthetic content).
- OWASP Top 10 for LLM Applications (2023, 2025); Greshake et al. (2023); Willison (2022, 2025) on prompt injection and the lethal trifecta.
- Shumailov et al. (2024), *Nature* 631 — model collapse.
- FBI PSA I-120324-PSA (December 2024) — family verification practices.
- Cloudflare (2025), announcements on default blocking of AI crawlers and pay-per-crawl, 1 July 2025.
- Reporting on the Hong Kong deepfake video-call fraud (February 2024) and the New Hampshire synthetic robocall (January 2024).
