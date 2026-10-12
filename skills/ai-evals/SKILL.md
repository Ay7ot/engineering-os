---
name: ai-evals
description: Design and run evals for AI features: error analysis, explicit rubrics, binary pass/fail scoring, and validated judges. Use when building evals for an LLM product, measuring output quality, or designing test cases and scoring rubrics.
metadata:
  audience: builder, tester
  upstream: https://github.com/RefoundAI/lenny-skills/tree/main/skills/ai-evals
  license: MIT
---
# AI Evals

## When to use
- An AI or LLM feature needs systematic quality measurement.
- Test cases, rubrics or scoring criteria must be designed.
- You need to know whether a model change made output better or worse.

For ordinary software tests, use `testing`.

## Start by clarifying
- What feature or model is being evaluated, and what does "good" look like?
- What are the most common failure modes seen so far?
- How will you know if the model got better or worse?
- Are you measuring what users actually care about?
- Have you manually reviewed enough outputs to understand the failure patterns?

## Core principles
- **The eval is the PRD.** If the model is the product, the eval defines what
  success looks like. It is a specification, not an optional quality check.
- **A core product skill, not only ML.** Product builders are expected to run it.
- **A workflow, not a one-off test.** Error analysis, open coding (writing down
  what is wrong on each trace), clustering failure patterns, then rubrics.

## Method
1. `read` real traces and record the actual failure on each one (open coding).
2. Cluster the failures into named patterns and count how often each occurs.
3. For the top clusters, write a rubric with specific, measurable criteria.
4. Turn each rubric into binary pass/fail test cases with concrete inputs.
5. Score the outputs, then either fix the product or add cases for a pattern you
   missed.
6. Repeat: the case set grows with each failure you find.

## Common mistakes
- **Skipping manual review.** You cannot write good evals without first seeing
  failure patterns in real traces.
- **Vague criteria.** "The output should be good" is not an eval; be specific and
  measurable.
- **Unvalidated LLM judges.** If a model acts as judge, validate the judge against
  human experts on a labelled sample first.
- **Likert scales.** Force pass or fail decisions; 1 to 5 scales produce
  meaningless averages.

## Checklist
- [ ] Real traces reviewed manually before criteria were written
- [ ] Failures clustered and counted
- [ ] Rubrics specific and measurable; cases are binary pass/fail
- [ ] Any LLM judge validated against human labels
- [ ] Evals trace back to user-visible requirements, not only technical metrics
