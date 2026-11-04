# AI Agent

A learning project exploring how AI agents work: software that uses AI models to plan and complete tasks.

## Status
Early stage. The repo now has a small working agent loop (plan, act, observe) with a tool registry and tests. The planner is rule-based, not a language model. It is written so a model-backed planner can replace it later.

## Quick start
Requires Python 3.8+. No extra packages.

```
python main.py "what is 6 * 7?"
python main.py "count words in hello big world"
python main.py "reverse: abc"
python main.py            # interactive prompt
```

Run the tests:

```
python -m unittest discover -s tests
```

## Layout
- `agent/core.py` - agent loop and rule-based planner
- `agent/tools.py` - tools: safe calculator, word count, reverse
- `main.py` - command line entry point
- `tests/` - unit tests

## Goals
- Learn how AI agents plan and act
- Build a working agent step by step
- Add a model-backed planner and more tools
