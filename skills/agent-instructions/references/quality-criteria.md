# Quality criteria for agent-instruction files

Score 100 points across six criteria. Score what the file actually says, not
what the repository does; the file exists so an agent can act without reading
everything.

## Commands and workflows (20)

- Build, test, dev, run, lint, and deploy commands are present.
- Commands are copy-pasteable and run from the stated directory.
- Any prerequisite (install step, env var, service) is named next to the
  command.
- Commands still work. Run them; do not assume.

## Architecture clarity (20)

- The directory layout and what each top-level area is for.
- Entry points, main config files, and where data flows.
- Enough that an agent can decide where a change belongs.

## Non-obvious patterns (15)

- Gotchas, quirks, and rules that are not visible from the code.
- Reasons behind surprising choices, when they are needed to avoid a mistake.
- Warnings that would otherwise cost a debugging session.

## Conciseness (15)

- No explanation of the obvious, no generic best practice.
- A line where a paragraph would do.
- No content duplicated from other docs; link instead.

## Currency (15)

- Matches the current codebase: paths exist, commands run, structure is right.
- Nothing describes a layout, tool, or process that has since changed.

## Actionability (15)

- Instructions are commands and concrete rules, not aspirations.
- Each line tells an agent what to do in a situation it will meet.

## Grades

| Grade | Score | Meaning |
|---|---|---|
| A | 90 to 100 | Comprehensive, current, actionable |
| B | 70 to 89 | Good coverage, minor gaps |
| C | 50 to 69 | Basic information, missing key sections |
| D | 30 to 49 | Sparse or outdated |
| F | 0 to 29 | Missing or severely outdated |

## Evidence checks before scoring

Run the documented commands. Check that each cited path exists with `glob`.
Compare the described structure with the real one using `bash` (`git ls-files`,
or a directory listing). A file scores no higher than its evidence allows:
documented but broken commands are worse than absent ones.

## Report format

For each file, give the path and kind, the total score and grade, a per-criterion
table (score and note), a list of specific issues, and a list of recommended
additions. End with the average score and the count of files needing work.
