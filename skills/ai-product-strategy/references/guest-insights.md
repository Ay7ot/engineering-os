# AI product strategy: insights from practitioners

Distilled from interviews with product leaders and AI practitioners. Use these
when a team is deciding where AI belongs.

## Start with the problem, not the AI

"One slippery slope is to keep thinking about solution complexity and forget the
problem you are trying to solve. Start with minimal-impact use cases to gain a
grip on current capabilities." Ship a small, real use case first and let
measured capability widen the scope.

## Define the human-AI boundary

"When working on algorithmic products, your job is figuring out what the
algorithm is responsible for, what people are responsible for, and the
framework for making decisions." The boundary is the product decision; the
model choice is downstream of it.

## LLMs are cheap glue, dear inference

"LLMs are distilled intuition. They make writing good-enough software
significantly cheaper, but they increase marginal inference costs." The cost
structure changes: cheap to build, ongoing to run. Plan for the second.

## Build for the slope, not the snapshot

"Build for the slope instead of the snapshot of where you are." Capability and
price move fast, so avoid architecture that only works with one model on one
day.

## Design for squishiness

"Even at 99 percent accuracy, if it punches the user in the face one time in a
hundred, that is not a viable product. Design assuming the AI will be squishy."
Plan the recovery path for every place the model can be wrong.

## Flywheels beat first-mover advantage

"It is not about being first to have an agent. It is about building the right
flywheels to improve over time." Log human actions and outcomes so the system
compounds.

## A society of models

"Future products will be made of many different models. It is quite a heavy
engineering project." Use specialised models per task rather than one model for
everything.

## Use the right tool per task

"We run chess engines for evaluation; the model translates that into natural
language. Use the right technology for the right task." Do not route an exact
computation through a model.

## People are the bottleneck

"The limiting factor is human typing speed and multitasking on prompts. Build
systems that are default useful without constant prompting." Make the default
path productive, and accept asynchronous interaction where it fits.

## Account for non-determinism

"Most people ignore the non-determinism. You do not know how users will behave
with natural language, and you do not know how the model will respond." Test both
halves of an unpredictable system.

## Agents need autonomy, complexity, natural interaction

"Effective agents have increasing autonomy to handle higher-order tasks, the
ability to handle complex multi-step workflows, and natural, often asynchronous
interaction." Judge an agent design against all three.

## Rebuild your intuitions

"Leaders have to get hands-on, not implementing, but rebuilding intuitions. Be
comfortable that your intuitions might not be right." Keep a habit of using the
technology yourself so the judgement calls stay grounded.
