# Deploy methods in detail

## The `.vercel` directory

A linked project has one of these:
- `.vercel/project.json`: created by `vercel link`, holds `projectId` and
  `orgId`.
- `.vercel/repo.json`: created by `vercel link --repo`, holds `orgId`,
  `remoteName` and a `projects` array mapping directories to project IDs.

Either file means linked. Check for both.

## Retrieving the preview URL after a push

```bash
sleep 5
vercel ls --format json
```

The JSON has a `deployments` array; the latest entry's `url` is the preview
URL. If the CLI is not authenticated, check the Vercel dashboard or the commit
status checks on the git host.

## No-auth deploy script

```bash
bash "<skill-dir>/resources/deploy.sh" [path]
```

`path` is a directory or a `.tgz` (defaults to the current directory). The
script auto-detects the framework from `package.json`, packages the project
excluding `node_modules`, `.git` and `.env`, uploads it, and waits for the
build. It returns JSON or plain text with `previewUrl` and `claimUrl`.

Report both:

```text
Deployment successful.
Preview URL: https://my-app-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...
```

## Sandboxed environments

- Try the CLI first when shell access and network egress are available.
- If auth is blocked or login cannot complete, go straight to the no-auth
  script.
- If the deploy fails on network errors (timeouts, DNS failures, connection
  resets), rerun only the deploy command with escalated network permissions,
  and ask the user first. Never escalate the `command -v vercel` check.
- If an egress allowlist blocks the call, tell the user which domain to allow
  (`*.vercel.com`) and try again.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `vercel deploy` says no credentials | run `vercel login`, or use the no-auth script |
| `vercel link` matched the wrong project | use `vercel link --repo` so it matches by git remote |
| Interactive prompt in an unlinked directory | stop; only `vercel whoami` is safe there |
| Build still running | poll `vercel inspect <url>`, do not re-deploy |
| Wrong team | check the `orgId` in `.vercel`, then pass `--scope` |

## Why prefer the linked state

A linked project with a git remote deploys on every push, gives a preview URL
per branch, and needs no further agent involvement. Each method above exists to
move a project toward that state rather than to perform one-off uploads.
