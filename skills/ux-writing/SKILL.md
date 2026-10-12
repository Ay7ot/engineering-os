---
name: ux-writing
description: Write interface microcopy for buttons, errors, empty states, loading, success, tooltips and onboarding. Use when writing or reviewing product UI text; not for marketing page copy (`copywriting`) or long-form docs (`documentation`).
metadata:
  audience: builder, lead
  upstream: https://github.com/slb2248/ai-ux-skills/tree/main/skills/ux-writing
  license: MIT
---
# UX Writing

## When to use
- Writing or reviewing button labels, error messages, empty states, success messages, loading text, tooltips or onboarding copy.
- The wording reads generic ("Submit", "Error 404", "Success!").
- A user-facing string should say what to do next, not only what happened.

Not for marketing pages, headlines or CTAs (`copywriting`), and not for README, spec or API prose (`documentation`).

## Principles
- Clarity over cleverness: plain, familiar words, no jargon.
- Concise: one idea per sentence, front-load the important part.
- Helpful: say what to do, not just what happened.
- Specific: name the exact object, value or next step.

## Button labels
- Do: action verbs ("Save", "Send", "Create"); specific ("Add to Cart", not "Submit"); match intent ("Sign up free").
- Do not: generic ("OK", "Submit", "Continue"), vague ("Click here", "Go"), negative framing ("Don't cancel").
- Common swaps: Submit to Send Message; OK to Got it; Continue to Next: Payment; Cancel to Keep Editing; Yes/No to Delete / Keep.

## Error messages
Formula: what happened + why + how to fix it.
- "Page not found. Try searching or go back to the homepage."
- "Enter a valid email address, for example name@example.com."
- "We couldn't save your changes. Check your connection and try again."
- Be specific, avoid blame ("You entered..."), suggest the fix, use plain language rather than an error code.

## Empty states
Cover three things: what this space is for, why it is empty, how to fill it.
- "No results for 'xyz'. Try different keywords or check your spelling."
- "No messages yet. When someone contacts you, you'll see it here."
- "Your projects will appear here. Create your first project to get started."

## Loading and progress
- Under 2 seconds: a spinner alone, no text.
- 2 to 10 seconds: "Loading your dashboard...", "Saving changes..."
- Over 10 seconds: "Processing your video. This usually takes 1-2 minutes." Show a percentage when you can.

## Success messages
- Be specific: "Your profile has been updated." not "Success!".
- Confirm the action and its object: "Message sent to name@example.com", "Order #12345 confirmed. Shipping in 2-3 days."
- Suggest the next step: "Password changed. You can now sign in with your new password."

## Tooltips and hints
- Use for unfamiliar controls, context for an action, or a keyboard shortcut.
- Under 150 characters, one concept each, never critical information: tooltips are hidden by default.

## Onboarding
- Welcome: acknowledge the milestone, set expectations, point at the first action. "Welcome to Acme! Let's set up your workspace in 3 quick steps."
- Progressive disclosure: do not explain everything at once; introduce features when relevant; prefer inline hints over a tutorial.

## Voice and tone
- Voice is constant: friendly but professional, clear, direct.
- Tone shifts by context: success warm, error calm and helpful, warning serious, onboarding encouraging, settings neutral.
- Keep one term per concept everywhere ("sign in" or "log in", never both).

Worked swaps and before/after rewrites: references/microcopy-examples.md.

## Checklist
- [ ] Buttons use a specific action verb, not "Submit" or "OK"
- [ ] Errors state what happened, why, and the fix
- [ ] Empty states say what the space is for and how to fill it
- [ ] Loading text matches the wait length
- [ ] Success messages name the object and the next step
- [ ] Tone matches the situation; voice stays consistent
- [ ] No blame, jargon or raw error codes
- [ ] One term per concept across the interface
