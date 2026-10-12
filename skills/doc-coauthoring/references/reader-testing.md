# Reader testing

Testing a document on a reader who has none of the writing session's context.

## Why

Authors cannot see their own blind spots: terms defined only in their head, steps skipped as obvious, decisions that make sense only if you were there.

## Predict reader questions

Write 5 to 10 questions a real reader would ask while trying to find or use the document. Base them on the reader's job, not the author's:

- Where do I start?
- What do I do when X fails?
- Which of these options applies to me?
- Who approves this?
- What does term X mean here?

## Run the test

- If a fresh agent is available: spawn a `task` per question, giving it only the document text and that question. It must answer from the document alone.
- Otherwise: ask the user to open a new session, paste the document, and ask the same questions.

Ask the reader to report, per answer:

- what it found ambiguous or unclear;
- what knowledge or context the document assumes the reader already has;
- any internal contradictions or inconsistencies.

## Interpret

For each question, record whether the answer was correct, partial or wrong, and quote the sentence that caused the problem. A partial answer usually means a missing definition or a skipped step, not a bad reader.

## Fix and re-run

Edit the sections that failed, then re-test only the questions that were wrong. Stop when answers are consistently correct and no new ambiguity appears.

## Exit condition

The document passes when a context-free reader answers the questions correctly and no new gaps or ambiguities surface.
