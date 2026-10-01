## Copyright

Copyright © 2026 Pranjul Rathour. All rights reserved.

No part of this book may be reproduced in any form without written permission from the author, except for brief quotations in reviews or scholarly work.

The measurements in this book were made on the author's hardware with the code published in the companion repository, and are reported with the conditions under which they were taken. They illustrate principles; they are not benchmarks of any product, and your numbers will differ. Nothing here is advice about any specific system, vendor or purchase.

First edition, October 2026.

Published by the author. Kanpur, India.

pranjulrathour41@gmail.com · https://pranjulrathour.scult.in · https://github.com/Pranjulrathour/research

---

*For everyone who has been paged at three in the morning by a system that was "working fine".*

---

## Contents

**Preface** — Why measurement, why now

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

9. Observability: you cannot fix what you cannot see
10. Capacity planning and performance testing
11. Cost is a design constraint
12. Judgment: how to make and document a design decision

**Appendix A** — The benchmark methods and how to re-run them
**Appendix B** — A latency-budget worksheet and an SLO worksheet
**Appendix C** — Reading list
**About the author**

---

## Preface

### Why measurement

System design is usually taught as a vocabulary: learn the names of the patterns, recognise which one the problem calls for, draw the boxes. The vocabulary is necessary and it is not the skill. The skill is judgment: knowing which of several correct designs is right for *these* requirements, what each one gives up, and whether the system you built actually does what the design said it would. Judgment is built from measurement, and most books on the subject contain none.

This book contains measurements. Where it says that one concurrency model's tail latency diverges from another's as load rises, it says so because the two were run, on the same machine, under the same load, and the numbers are in the companion repository with the code that produced them. Where it says that an approximate nearest-neighbour index trades recall for speed along a curve, the curve was measured on public datasets and is reproducible with one command. Where a number comes from someone else's work, it has a name and a year attached. Where the author has only an opinion, the book says so.

The reason is not pedantry. It is that the alternative, asserting performance properties without measuring them, is how systems come to be designed around beliefs that were never true, and how engineers come to be confident about things they have never seen. The habit this book is trying to build is the habit of asking "how do you know?" of every claim, including your own, and of being able to answer.

### Why now

Two things have changed since the classic texts on this subject were written.

The first is that the tools for producing software have become extraordinarily good at producing the parts. Code that implements a known pattern, wires a known service or follows a known recipe can be generated in seconds, and the quality is often fine. What the tools do not do is decide which pattern the requirements call for, notice that the generated part will fall over at ten times the load, or know what to measure to find out. As production gets cheap, the value of the engineer moves to exactly the judgment this book is about, and the ability to prove that judgment with a measurement becomes the thing that distinguishes an engineer from a prompt.

The second is that the systems being built are increasingly systems that *act*: services wrapped around machine-learning models that retrieve, decide and call other systems, with tail latencies that users feel, reliability requirements that the models themselves do not meet, and costs that scale per request in new ways. These systems are not exempt from any principle here; they are the most demanding application of all of them, and several chapters treat them as the running modern example.

### What this book is, and is not

It is a book of principles, each stated plainly, each shown with a number you can reproduce, each with its trade-off named, and each ending with the question an interviewer or an incident review will ask about it and with an exercise you can run in an afternoon. It covers the ground that system-design interviews at the large technology and finance firms actually test, which is also the ground that production incidents actually cover; the two are the same ground, and the book treats them as such.

It is not a catalogue of products. Products are named as examples, with dates, and the principles are chosen to outlast them. It is not an introduction to programming or to any particular language; the companion code is in Python because Python is what the author's readers mostly know, and nothing in the argument depends on it. And it is not exhaustive: twelve chapters cannot cover distributed systems, and the reading list at the end points to the books that come closer.

### How to read it

In order, if you can: Part I builds the measurement habit on latency, where it is easiest to see; Part II applies it to correctness, where it is hardest; Part III turns it into the practices (observability, capacity, cost, decision records) that make a system operable and a design defensible. If you are preparing for an interview next week, read chapter 12 first and then the chapters whose questions you cannot answer. If you have an incident to understand, chapters 7, 9 and 10 are the ones to open.

Every chapter ends with "Run this yourself". The exercises use a small harness published with the book and take an afternoon each. Doing even three of them will change how you read the rest, because you will have seen a tail latency diverge, a cache stampede, a retry storm or a queue grow with your own eyes, and a principle you have watched fail is one you do not forget.

A companion volume, *The AGI Transition: A Field Guide for the Next Decade*, takes the wider view: what the arrival of capable AI means for work, learning and institutions, and why the judgment this book teaches is one of the few things that becomes more valuable as the tools improve. The two were written to be read together and each stands alone.

Kanpur, October 2026

---
