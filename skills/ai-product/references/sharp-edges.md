# LLM production sharp edges

Each entry is a failure seen in production, with the defence to build in.

## Trusting model output without validation (critical)

Never act on a model response without checking it. Layers:
- Schema validation for structured data.
- Content filters for harmful or disallowed output.
- Fact checking against a knowledge base for anything presented as true.
- Fallback values for missing or malformed fields, plus a visible error when no
  fallback is safe.

## User input placed in prompts unsanitised (critical)

Any user text that reaches a prompt is untrusted input. Defences, in order:
- Sanitise and escape input, and separate instructions from data in the prompt.
- Detect prompt injection attempts and refuse or quarantine them.
- Validate the output before acting on it, so a successful injection still has
  to survive the schema.
- Rate limit per user to bound the damage and the cost.

Prompt injection cannot be fully solved by phrasing alone. Treat it as a
boundary problem: assume the model can be influenced, and keep the dangerous
actions behind validation and authorisation.

## Overfilling the context window (high)

More context is not better. Count tokens with the model's tokenizer before
sending, select the most relevant context, and chunk large documents. For a
frequent pattern, consider fine-tuning or caching instead of re-sending.

## Waiting for the full response (high)

Do not leave the user on a blank screen. Stream tokens, show a progress
indicator, allow cancellation, and handle a stream that dies mid-response.

## Not tracking API cost (high)

Log token usage per call, with the model and the feature. Set a budget and an
alert. Review the most expensive patterns and optimise prompts, context size, or
model tier. Cost per request is a product metric, not only an infrastructure one.

## The app breaking when the API fails (high)

Defence in depth: retry with exponential backoff and jitter, a circuit breaker
to stop hammering, a fallback response, graceful degradation of the feature, and
an error message the user can act on. A model provider outage should degrade one
feature, not the product.

## Unvalidated factual claims (critical)

For anything factual: cross-reference a knowledge base, cite sources where
possible, mark AI-generated content clearly, let the user verify, and track
accuracy over time so regressions show up.

## Calls inside synchronous request handlers (high)

Slow model calls do not belong in a request handler. Move them to background
jobs with a webhook or a poll for completion, stream when real time is needed,
cache repeated queries, and give the user feedback while they wait.
