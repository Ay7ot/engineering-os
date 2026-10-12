# Invocation variants

How `improve-animations` is run and what each form does.

| Invocation | Behaviour |
| --- | --- |
| bare | Recon, audit all categories, vet, confirm, plans |
| `quick` or `deep` | Adjust audit effort; composes with a focus |
| a category focus (`performance`, `accessibility`, `easing`) | Recon plus that category only |
| `plan <description>` | Skip the audit; recon just enough to specify, then write one plan |
| `execute <plan>` | Dispatch an executor subagent to implement the plan in an isolated worktree, then review its diff against the `review-animations` bar and render a verdict |
| `reconcile` | Re-check `plans/` against the current code: mark done plans DONE, refresh stale `file:line` references, retire fixed findings |

`execute` is the only variant that changes code, and it does so in a worktree,
never on the source tree this skill was auditing.
