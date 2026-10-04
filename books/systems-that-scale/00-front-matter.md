## Copyright

Copyright © 2026 Pranjul Rathour. All rights reserved.

No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews or scholarly work.

The measurements in this book were made on the author's own hardware with the code published in the companion repository, and are reported together with the conditions under which they were taken. They illustrate principles; they are not benchmarks of any product, and your numbers will differ. Nothing here is advice about any specific system, vendor or purchase.

First edition, October 2026.

Published by the author. Kanpur, India.

pranjulrathour41@gmail.com · https://pranjulrathour.com · https://github.com/Pranjulrathour/research

GitHub: github.com/Pranjulrathour

LinkedIn: linkedin.com/in/pranjul-rathour

X: x.com/PranjulRathourx

Instagram: instagram.com/pranjulrathour.in

Threads: threads.com/@pranjulrathour.in

Bluesky: bsky.app/profile/pranjulrathour.bsky.social

Facebook: facebook.com/profile.php?id=1377591238763842

Dev.to: dev.to/pranjulrathour

Hashnode: pranjulrathour.hashnode.dev

Blogger: pranjulrathourtechguru.blogspot.com

---

*For everyone who has been paged at three in the morning by a system that was "working fine".*

---

## Contents

**Preface**

**Part I — Latency**

1. Latency is a distribution, not a number
2. Concurrency models and the price of blocking
3. Caching: the fastest request is the one you don't make
4. Data structures at scale

**Part II — Correctness under failure**

5. Consistency, availability and what you actually get
6. Replication, partitioning and the two hard problems
7. Failure is the normal case
8. Queues, streams and asynchrony

**Part III — Operating and deciding**

9. Observability: you can't fix what you can't see
10. Capacity planning and performance testing
11. Cost is a design constraint
12. Judgment: how to make and document a design decision

**Appendix A** — The benchmark methods and how to re-run them
**Appendix B** — A latency-budget worksheet and an SLO worksheet
**Appendix C** — Reading list
**About the author**

---

## Preface

System design is usually taught as a vocabulary. You learn the names of the patterns, learn to recognise which one a problem calls for, and draw the boxes. The vocabulary matters, but it isn't the skill. The skill is judgement: knowing which of several correct designs suits these particular requirements, what each one gives up, and whether the system you built actually does what the design promised. Judgement comes from measurement, and most books on the subject don't contain any.

This one does. When it says that one concurrency model's tail latency pulls away from another's as load rises, that's because I ran both on the same machine under the same load, and the numbers are in the companion repository next to the code that produced them. When it says an approximate nearest-neighbour index trades recall for speed along a curve, that curve was measured on public datasets and can be reproduced with one command. When a number comes from somebody else's work, it carries a name and a year. When all I have is an opinion, I say so.

That isn't pedantry. The alternative, asserting how a system performs without measuring it, is how systems end up designed around beliefs that were never true, and how engineers end up confident about things they've never actually seen. The habit I'm trying to build in this book is asking "how do you know?" of every claim, your own included, and being able to answer.

### Why now

Two things have changed since the classic texts on this subject were written.

The first is that tools for producing software have become extraordinarily good at producing the parts. Code that implements a known pattern, wires up a known service or follows a known recipe can be generated in seconds, often perfectly well. What the tools don't do is decide which pattern the requirements call for, notice that the generated part will fall over at ten times the load, or know what to measure to find out. As producing code gets cheap, the engineer's value shifts to exactly the judgement this book is about, and being able to back that judgement with a measurement becomes what distinguishes an engineer from a prompt.

The second is that more and more of the systems being built act on the world: services wrapped around machine-learning models that retrieve, decide and call other systems, with tail latencies users can feel, reliability requirements the models themselves can't meet, and costs that scale per request in unfamiliar ways. These systems aren't exempt from any principle in this book. They're the most demanding application of all of them, and several chapters use them as the running modern example.

### What it is, and isn't

It's a book of principles. Each one is stated plainly, shown with a number you can reproduce, and paired with the trade-off it involves, and each chapter ends with the question an interviewer or an incident review is likely to ask about it and an exercise you can run in an afternoon. It covers the ground that system-design interviews at large technology and finance firms actually test, which also happens to be the ground production incidents actually cover. They're the same ground, and the book treats them that way.

It isn't a catalogue of products. Products appear as examples, with dates, and the principles were chosen to outlast them. It isn't an introduction to programming or to any particular language; the companion code is in Python because that's what most of my readers know, and nothing in the argument depends on it. And it isn't exhaustive. Twelve chapters can't cover distributed systems, and the reading list at the end points to books that come closer.

### How to read it

In order, if you can. Part I builds the habit of measurement on latency, where it's easiest to see; Part II applies it to correctness, where it's hardest; and Part III turns it into the everyday practices (observability, capacity, cost, decision records) that make a system operable and a design defensible. If you have an interview next week, read chapter 12 first and then whichever chapters ask questions you can't yet answer. If you're trying to understand an incident, open chapters 7, 9 and 10.

Every chapter ends with a section called "Run this yourself". The exercises use a small harness published alongside the book, and each takes an afternoon. Doing even three of them will change how you read the rest, because you'll have watched a tail latency pull away, a cache stampede, a retry storm or a queue grow with your own eyes, and you don't forget a principle you've watched fail.

There's a companion volume, *The AGI Transition: A Field Guide for the Next Decade*, which takes the wider view: what capable AI means for work, learning and institutions, and why the judgement this book teaches is one of the few things that gets more valuable as the tools improve. The two were written to be read together, though each stands on its own.

Pranjul Rathour
Kanpur, October 2026

---
