# Chapter 11 — India's decade

This book has been written from India and it has used India as an example throughout: the entry-level paradox in chapter 4, the curriculum in chapter 5, the governance choices in chapter 7. This chapter puts the pieces together and asks the question directly: what does the transition this book describes mean for the country with the largest young population on Earth, the second-largest pool of software engineers, and a services economy built in large part on doing, for the rest of the world, the kinds of work the tools are learning to do?

The honest answer has two halves that are both true. India is unusually exposed, because a large share of its export earnings and its graduate employment comes from exactly the task categories chapter 3 marked as most automatable. And India is unusually well placed, because it has built, over fifteen years, a digital public infrastructure that most countries lack, it has a domestic market of a scale that justifies building for it, and it has the people. Which half dominates is not decided by the technology. It is decided by choices made in the next five years, by firms, by institutions and by individuals, and this chapter is about what those choices are.

## The exposure

Start with the numbers that matter.

India's IT and business-process services industry employed about 5.4 million people directly in 2024 and earned the country roughly US$190–200 billion a year in export revenue, making it the largest single component of services exports and one of the largest employers of graduates.[^1] The industry's historical model is the one chapter 4 described: hire large numbers of fresh graduates, train them for a few months, bill them to overseas clients for work that is well specified and repeatable (application maintenance, testing, support, data processing, routine development), and promote the ones who learn to manage and design.

Every step of that model is exposed. The work that is billed is the work chapter 3's exposure studies rank highest. The training ground for juniors is the task set that is being automated first. And the clients are the same firms that are deploying the tools internally and asking why they are paying for human hours to do what their own systems can now do. The large Indian services firms saw this early; their headcount growth decoupled from revenue growth from around 2023, their fresh-graduate hiring fell sharply in 2023 and 2024 before partially recovering, and their public strategy shifted toward "AI-led" services, meaning fewer people billed for more value each.[^2] That shift is rational and it means that the industry which absorbed a large share of India's engineering graduates for twenty-five years will absorb fewer of them, at a higher bar, for the rest of the decade.

The second exposure is in the newer layer: the global capability centres, the in-house India operations of multinational firms, which grew rapidly through the 2020s to more than 1,700 centres employing around two million people by 2025.[^3] GCCs do higher-value work than the services firms on average (engineering, analytics, product development, finance operations) and they are less exposed for that reason. They are also where the multinational employers that this book's readers aspire to actually hire in India, and they are hiring for exactly the profile chapter 10 described: people who can work above the narrowed entry rung from the start.

The third exposure is the one nobody counts: the millions of graduates each year, in computing and in other fields, whose first job was going to be some form of information work and for whom the entry rung is narrowing in every sector at once.

### A worked case: the headcount numbers

The industry's own figures make the shift visible. For two decades the three largest Indian IT-services firms added employees every year, often tens of thousands each, and their campus intake was the single largest entry point into professional work for Indian engineering graduates. In the financial year ending March 2024, all three reported a net *decline* in headcount, together shedding on the order of 60,000 employees while revenue continued to grow, and fresher hiring at the large firms fell to a fraction of its 2022 level.[^7] Revenue per employee, which had been flat for years, began to rise. Headcount recovered modestly in the following year, but campus offers did not return to their earlier scale, and in mid-2025 the largest of the three announced a reduction of around 2 per cent of its workforce, concentrated in middle and senior grades, which it attributed to skill mismatch in a changing market.[^8]

Read through chapter 3's channels, the numbers say three things. Revenue growing while headcount falls is the productivity channel operating: the same output with fewer people, or more output with the same people. Fresher intake falling faster than total headcount is the entry-level paradox of chapter 4 in its purest form. And the industry's public strategy, "AI-led" services with fewer, more senior people billed for outcomes rather than hours, is the value migration this section describes, undertaken deliberately by the firms themselves. None of this means the industry is shrinking; it means the industry's relationship to the graduate pipeline has changed, and the change is visible in the firms' own accounts before it is visible in any labour statistic.

## The platform

Now the other half.

Between 2009 and 2024 India built a set of shared digital systems that almost no other country has: a universal digital identity (Aadhaar, with more than 1.3 billion enrolments), a real-time interoperable payments system (UPI, processing on the order of 18–20 billion transactions a month by 2025), a consent-based data-sharing framework (the Account Aggregator system, DigiLocker), and open protocol initiatives for commerce (ONDC) and other sectors.[^4] Together these are usually called India's digital public infrastructure, and their significance for the AI transition is specific.

AI systems create value when they can act on real processes with real data. In most countries, the processes are fragmented across incompatible private systems and the data is locked in silos, so an AI product has to be integrated anew with every bank, every merchant, every agency. In India, a large share of the economy's basic transactions run on shared rails with open interfaces. A system that can speak UPI can transact with hundreds of millions of people; a system that can use the Account Aggregator framework can, with consent, reason over a person's financial history; a system that can work with the identity layer can verify who it is talking to. The cost of deploying an AI application into the real economy is lower in India than almost anywhere, because the plumbing is already shared.

This is why the scenario in which India is "the world's AI back office" (doing data labelling, model evaluation, support and integration for products built elsewhere) is not the only one available. The alternative is building AI products *for* the Indian economy, on the rails that already exist, for a market of 1.4 billion people most of whom are underserved by every kind of formal service, from credit to health to legal advice to education. The rails make that possible. They do not make it inevitable.

## Language: barrier and moat

India has 22 scheduled languages and hundreds of others in daily use, and the current generation of AI systems was trained overwhelmingly on English. In 2023 the gap was stark: the models were dramatically worse in Hindi than in English and nearly useless in most other Indian languages, both because of training data scarcity and because tokenisers built for English made Indian-language text several times more expensive to process.[^5]

The gap has narrowed. Indian-language capability in the frontier models improved substantially through 2024–2026; dedicated Indian-language models and datasets were built by academic groups, by companies and under the IndiaAI Mission; speech systems in Indian languages, which matter more than text for most of the population, improved fastest of all. By 2026 the question was no longer whether the systems could function in Indian languages but how well, for which languages, at what cost, and whether anyone was building the applications.

Here the language diversity cuts both ways. It is a barrier: everything is harder, more expensive and later in a market with twenty-two languages than in one with one. It is also a moat: a product that works well in Bhojpuri or Marathi or Kannada, for the specific needs of people who speak those languages, is not something a firm in California will build first, or well. The firms and individuals who do that work have a market that global products will reach slowly, and a defensible position when they do. Chapter 10's advice to go deep in a domain applies with special force here: the domain can be a language and the communities who speak it.

## Education at the only scale that matters

India has about 250 million school students and more than 40 million in higher education, taught by a system that is chronically short of good teachers and uneven in quality to a degree that national averages conceal.[^6] Chapter 5 argued that AI tutoring is the first technology that plausibly addresses Bloom's two-sigma problem, and if that promise is real anywhere it matters most here, where the alternative for most students is not a human tutor but no tutor at all.

What the technology can plausibly do, in Indian conditions, is three things. Explain, in a student's own language, patiently and repeatedly, the material a crowded classroom could not. Give teachers tools for preparation, assessment and feedback that multiply their limited time. And make high-quality material available in languages and places it never reached.

What it cannot do is the three things chapter 5 identified. It cannot supply the motivation and accountability that a present adult provides, and the evidence from two decades of educational technology in low-resource settings is that technology without that adult reaches the already-motivated. It cannot fix access: a tutor that needs a smartphone, data and a quiet place reaches the students who have them, and widens the gap for those who do not, unless access is designed for deliberately (shared devices, offline modes, voice-first interfaces, integration with the schools and the teachers who exist). And it cannot decide what should be taught; that remains a human, institutional job, and India's institutions are slow.

The realistic goal is not two sigmas for every student. It is a measurable improvement for the students in the middle of the distribution who have a device and a teacher but not enough of either, and the design problem is making the tools work through the teachers rather than around them. That is a problem for Indian builders, because nobody else will solve it for Indian classrooms.

## Governance: capacity before constraint

Chapter 7 described India's choice: no dedicated AI law, a data-protection act phasing in, a large industrial mission, and soft instruments (advisories, guidelines, intermediary rules on synthetic content) ahead of hard ones. The strategic reading is that India has decided to build capacity first and regulate once it knows what it is regulating.

That is a defensible choice and it has a cost. The benefit is that builders in India in 2026 face fewer constraints than their European counterparts and can move faster. The cost is that the harms arrive before the rules: synthetic media in elections, fraud by voice clone, biased automated decisions in lending or hiring, and the data practices of firms that treat the absence of a specific AI law as the absence of any law. The DPDP Act, as its rules phase in through 2027, is the instrument that will bite first, and the practical governance task for an Indian builder is to treat personal data seriously before being forced to.

## What this means for a graduate in 2030

Pull the threads together and a picture emerges for someone finishing an MCA or a B.Tech in 2028 or 2030.

The services-firm entry rung that absorbed previous cohorts will be smaller and higher. The GCC rung, which is where the multinational employers hire in India, will be larger and will require, from the first day, the judgment-and-systems profile that chapter 10 described. The domestic product sector, building on the rails for Indian users in Indian languages, will be the fastest-growing and the most uncertain. And the entry path in every case will reward verifiable work over credentials, for the reasons chapter 5 gave.

Three implications follow for a student reading this now.

**Build for India, not only for a résumé.** A system that solves a real problem for real Indian users (a clinic, a school, a farmer cooperative, a small business, a language community) is a better piece of verifiable work than a tutorial project aimed at nowhere, and it puts you in the part of the market that global products reach last.

**Learn the rails.** UPI, Aadhaar-based verification, the Account Aggregator framework, DigiLocker, ONDC: these are the integration points for any AI product that touches the Indian economy, and almost no graduate knows them. It is a small investment with a large differentiating return.

**Treat the GCC and quant-finance rung as reachable.** The multinational firms hiring in India for engineering, analytics and quantitative roles want people who can measure, reason about systems and verify their own work. Chapter 10's plan builds exactly that profile, and chapter 6's reproducible-work habit is the proof those employers can check.

## What would make this chapter wrong

If by 2031 India's services exports have continued to grow strongly with stable employment, because the industry moved up the value chain faster than its juniors were displaced, then the exposure section was too pessimistic. Check industry employment and export figures and the fresh-graduate hiring numbers of the large firms.

If the digital public infrastructure has not translated into a domestic AI product sector of consequence, and India's role in the global AI economy in 2031 is mainly talent, data work and integration, then the platform section overestimated how much the rails would matter and the back-office scenario won. Check the revenue and user base of Indian-built AI products serving Indian users.

If Indian-language AI has reached parity with English across the major languages at low cost, the language-as-moat argument weakens because the barrier that protected local builders fell. Check the cost and quality of major-model performance across the scheduled languages.

If AI tutoring has produced large, well-measured gains in Indian government schools at scale, the education section was too cautious, and the design problem was easier than it looked.

## What to do this year

Build something for an Indian language or an Indian institution. Pick a problem you have seen with your own eyes: a form that a relative could not fill, a school that needs a timetable, a shop that cannot track stock, a community whose language no tool serves well. Build the smallest thing that helps, in the language its users speak, on whatever rails apply. Put it in front of five real users and keep what you learn. It will be a piece of verifiable work in chapter 10's sense, it will teach you more about the gap between capability and deployment than any course, and it will be the kind of work that the next decade in India rewards, because it is the work almost nobody else is doing.

---

[^1]: NASSCOM, *Strategic Review 2024* and *2025*: industry revenue, export share and direct employment figures. The industry's own figures; treat them as upper bounds on employment.
[^2]: Quarterly results and annual reports of the large listed Indian IT-services firms, FY2023–FY2026, for headcount and fresher-hiring figures; coverage in *The Economic Times*, *Mint* and *Business Standard* through 2024–2026.
[^3]: NASSCOM–Zinnov, *GCC Landscape* reports (2023, 2024, 2025) for centre counts and employment.
[^4]: Unique Identification Authority of India, enrolment dashboard (2025); National Payments Corporation of India, UPI monthly statistics (2025); Reserve Bank of India and Sahamati on the Account Aggregator framework; Open Network for Digital Commerce documentation.
[^5]: Ahuja, K. et al. (2023), "MEGA: Multilingual Evaluation of Generative AI", *EMNLP 2023*, and Petrov, A. et al. (2023), "Language Model Tokenizers Introduce Unfairness Between Languages", *NeurIPS 2023*, for the capability and tokenisation gaps; AI4Bharat (IIT Madras) publications for Indian-language benchmarks and models.
[^6]: Ministry of Education, *UDISE+ 2023–24* for school enrolment; *All India Survey on Higher Education 2021–22* for higher-education enrolment; ASER Centre, *Annual Status of Education Report 2024* for learning outcomes.
[^7]: Annual reports and fourth-quarter FY2024 results of Tata Consultancy Services, Infosys and Wipro (April 2024), each reporting a year-on-year net decline in employees; coverage of the combined figure and of campus-hiring trends in *The Economic Times* and *Mint*, April–May 2024.
[^8]: Tata Consultancy Services, statement and press coverage, 27 July 2025, on a planned workforce reduction of about 2 per cent during FY2026.

### Sources for this chapter
- NASSCOM Strategic Reviews (2024, 2025); NASSCOM–Zinnov GCC reports.
- NPCI UPI statistics; UIDAI dashboard; RBI/Sahamati Account Aggregator data; ONDC documentation.
- IndiaAI Mission (Cabinet approval, 7 March 2024); MeitY *India AI Governance Guidelines* (November 2025); DPDP Act 2023 and Rules 2025.
- Ahuja et al. (2023); Petrov et al. (2023); AI4Bharat IndicLLMSuite and related papers (2024).
- UDISE+ 2023–24; AISHE 2021–22; ASER 2024.
- Chapters 3, 4, 5, 7 and 10 of this book.
