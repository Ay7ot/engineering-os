---
name: security-review
description: Review code, configs, and dependencies for security weaknesses. Use before merge when changes touch auth, payments, data, webhooks, secrets, or infrastructure, and for general security review.
metadata:
  audience: security, reviewer
---
# Security Review

## When to use
- Before merge when the change touches authentication, authorization, payments, PII, webhooks, secrets, or infrastructure.
- General security review of a codebase or feature.

## Review checklist
- **Authentication** — mechanism, session/cookie flags (HttpOnly, Secure, SameSite), token storage/handling, MFA, brute-force protection.
- **Authorization** — access control on every action, tenant isolation, privilege separation, ownership checks (IDOR).
- **Input validation** — injection (SQL, command, template, header), XSS, path traversal, SSRF, unsafe deserialization, file uploads, prototype pollution, regex DoS.
- **Secrets** — hardcoded secrets, secrets in logs/config/repo, overly permissive env exposure.
- **Webhooks** — signature verification, replay protection, idempotency.
- **Race conditions** — TOCTOU, double-spend, non-atomic state changes.
- **Sensitive data exposure** — PII/keys/tokens in logs, responses, error messages, stack traces.
- **Logging** — what is logged, what is redacted, log injection.
- **Permissions** — least privilege on services, DB, IAM, filesystem.
- **Dependencies** — known vulnerabilities (npm audit, pip-audit, etc.), outdated/abandoned packages, supply-chain risks.
- **Infrastructure** — network exposure, TLS, headers, CORS, misconfiguration.

## Output format
For each finding: **Severity** (critical / high / medium / low / info), **Location** (path:line), **Issue**, **Impact**, **Exploitation likelihood**, **Remediation**. End with **Verdict**: SAFE / ISSUES FOUND + severity counts.

## Rules
- Distinguish verified findings from hypotheses; provide evidence.
- Focus on real attack surface, not cosmetics.
- Report only — never fix during review.
- Flag anything hitting the human approval gate (security-sensitive changes).

## Example finding
- Severity: high
- Location: src/routes/payments.ts:44
- Issue: `org_id` taken from request body, not authenticated session; charge created for arbitrary org.
- Impact: cross-tenant IDOR — any authenticated user can create charges in another org.
- Exploitation likelihood: trivial with a modified request.
- Remediation: derive `org_id` from the authenticated session and verify membership server-side.