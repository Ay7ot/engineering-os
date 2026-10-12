---
name: ai-product
description: Ship LLM features to production: validated structured output, streaming, prompt versioning, cost and failure handling. Use when building or reviewing an AI feature, or debugging unreliable model output. For output quality, use `ai-evals`; for where AI belongs, see `ai-product-strategy`.
metadata:
  audience: builder, reviewer
  upstream: https://github.com/sickn33/antigravity-awesome-skills
  license: MIT
---
# AI Product

## When to use
- Building or reviewing an LLM feature that will face real users.
- Model output is unreliable, slow, or expensive in production.
- Adding streaming, retries, fallbacks, or cost controls around a model call.

For measuring whether output is good, use `ai-evals`. For deciding whether AI
belongs in the product at all, use `ai-product-strategy`.

## Patterns
- **Structured output with validation.** Use tool or function calling, or JSON
  mode, with a schema, then validate every response against that schema before
  use. Never parse free text and trust the result.
- **Streaming with progress.** Stream tokens so the user sees progress and
  perceived latency drops. Allow cancellation and handle an interrupted stream.
- **Prompts as code.** Version prompts in the repository, review changes like
  code, and keep a regression suite of inputs and expected properties.
- **Graceful degradation.** Retry with exponential backoff, add a circuit
  breaker, keep a fallback path, and show a clear error state.

## Anti-patterns
- **Demo-ware.** A demo hides edge cases; real inputs break it and the trust
  around it.
- **Context window stuffing.** More context is slower and more expensive and it
  dilutes the signal. Select relevant context and count tokens first.
- **Unstructured output parsing.** Free-text parsing breaks randomly and invites
  injection.

## Sharp edges
Each of these is a common production failure. Detail and defences:
`references/sharp-edges.md`.
- Trusting model output without validation (critical): schema checks, content
  filters, fact checks, fallback values.
- User input placed in prompts unsanitised (critical): sanitise and escape,
  detect injection, validate output, rate limit per user.
- Overfilling the context window (high): count tokens, prioritise, chunk,
  consider fine-tuning for frequent patterns.
- Waiting for the full response before showing anything (high): stream, show
  progress, allow cancel.
- Not tracking API cost (high): log tokens per call, set budgets and alerts,
  optimise the expensive patterns.
- The app breaking when the API fails (high): retries, circuit breakers,
  fallbacks, user-friendly errors.
- Unvalidated factual claims (critical): ground in a knowledge base, cite
  sources, label generated content, track accuracy.
- Model calls inside synchronous request handlers (high): background jobs,
  webhooks, streaming, caching.

## Checklist
- [ ] Structured output validated against a schema before use
- [ ] Prompts versioned and covered by a regression suite
- [ ] Streaming or progress for slow calls; cancellation works
- [ ] Token cost logged per request, with a budget and an alert
- [ ] Injection defences and per-user rate limits in place
- [ ] API failure path: retry, circuit breaker, fallback, clear error
- [ ] Factual claims grounded, cited, or labelled; accuracy tracked
- [ ] Long calls moved out of synchronous request handlers
