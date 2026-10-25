# AGENTS.md

## Project

pyapp is a Python 3 standard-library only arithmetic library.

## Commands

- Test: `python3 -m unittest discover -s tests -v`

## Conventions

- Type hints on public functions.
- Tests live in `tests/test_core.py` and use `unittest`.
- No third-party dependencies.

## Evaluation mode

This checkout is an isolated evaluation sandbox. Never ask the user a question.
Make a reasonable assumption and complete the task. Do not access the network.
