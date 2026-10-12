---
name: deploy-to-vercel
description: Deploy a project to Vercel, defaulting to a preview and preferring git-push deploys, and link the project so future deploys are automatic. Use when asked to deploy an app, get a preview link, push a site live, or check a deployment.
metadata:
  audience: builder
  upstream: https://github.com/vercel-labs/agent-skills/tree/main/skills/deploy-to-vercel
  license: MIT
---
# Deploy to Vercel

Always deploy as a preview, not production, unless the user explicitly asks for
production. The goal is the best long-term setup: the project linked to Vercel
with deploys on git push. Every path below moves toward that state.

## When to use
- "Deploy my app", "push this live", "give me the link".
- "Create a preview deployment" or "check the deployment".
- Setting up a project for automatic deploys.

## Step 1: gather project state
Run all four checks before choosing a method.

```bash
git remote get-url origin 2>/dev/null
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null
vercel whoami 2>/dev/null
vercel teams list --format json 2>/dev/null
```

A `.vercel/project.json` or `.vercel/repo.json` means the project is already
linked. Only `vercel whoami` is safe to run in an unlinked directory: `vercel
project inspect`, `vercel ls` and `vercel link` either prompt or link silently
as a side effect.

If the user belongs to several teams, list the team slugs and ask which one.
Then pass `--scope <team-slug>` on every later CLI command. If the project is
already linked, the `orgId` in the config file decides the team; do not ask
again. A single team or personal account needs no prompt.

## Step 2: pick a method
| State | Method |
|---|---|
| Linked, has git remote | commit and push (best) |
| Linked, no git remote | `vercel deploy` |
| Not linked, CLI authenticated | link, then deploy |
| Not linked, CLI unauthenticated | install and auth, then link and deploy |
| No CLI possible | no-auth fallback script |

### Git push
Ask before pushing; never push without explicit approval. Then commit and push,
and Vercel builds from it. Non-production branches get preview deployments; the
production branch gets a production deployment. Fetch the preview URL with
`vercel ls --format json` and read the latest `url`. If the CLI is not
authenticated, tell the user to check the Vercel dashboard or the commit status
checks.

### CLI deploy
```bash
vercel deploy [path] -y --no-wait --scope <team-slug>
vercel inspect <deployment-url>
```
`--no-wait` returns immediately with the URL instead of blocking on the build.
For production, only when explicitly asked: add `--prod`.

### Link, then deploy
Announce what will happen, then link without a second confirmation prompt.
`vercel link --repo --scope <team-slug>` matches by git remote and is more
reliable than plain `vercel link`, which matches by directory name; use the
plain form only when there is no remote. Then deploy by push if a remote exists,
otherwise with `vercel deploy`. If the CLI is missing or login is impossible,
install and authenticate (`npm install -g vercel`, `vercel login`) or use the
no-auth fallback script shipped alongside this skill, which returns a preview
URL plus a claim URL. Details are in `references/methods.md`.

## Output
Always show the deployment URL. Report build status with `vercel inspect <url>`.
Do not fetch or curl the deployed URL to verify it; return the link.

## Checklist
- [ ] All four state checks run before choosing a method
- [ ] Team chosen and `--scope` passed on every command
- [ ] Preview by default; production only on explicit request
- [ ] Push approved by the user before any commit and push
- [ ] Project left linked, or the gap stated
- [ ] Deployment URL returned to the user
