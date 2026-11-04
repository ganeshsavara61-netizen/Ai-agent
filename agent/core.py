"""Agent loop: plan -> act -> observe.

The planner here is rule-based (regular expressions), not a language model.
It is written so a model-backed planner can replace `plan` later without
changing the loop or the tools.
"""
import re
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


@dataclass
class Step:
    tool: str
    argument: str
    observation: str


Planner = Callable[[str], Optional[tuple]]

_RULES = [
    (re.compile(r"^(?:calc(?:ulate)?|what is|compute)\s*:?\s*(.+?)\??$", re.I), "calculate"),
    (re.compile(r"^(?:count words(?: in)?|word count)\s*:?\s*(.+)$", re.I), "word_count"),
    (re.compile(r"^reverse\s*:?\s*(.+)$", re.I), "reverse"),
]


def rule_planner(task: str) -> Optional[tuple]:
    """Return (tool_name, argument) for a task, or None if no rule matches."""
    for pattern, tool in _RULES:
        match = pattern.match(task.strip())
        if match:
            return tool, match.group(1).strip()
    return None


class Agent:
    def __init__(self, tools: Dict[str, Callable[[str], str]], planner: Planner = rule_planner):
        self.tools = tools
        self.planner = planner
        self.history: List[Step] = []

    def run(self, task: str) -> str:
        decision = self.planner(task)
        if decision is None:
            return "I don't know how to do that. Tools: " + ", ".join(sorted(self.tools))
        tool, argument = decision
        if tool not in self.tools:
            return f"error: unknown tool '{tool}'"
        observation = self.tools[tool](argument)
        self.history.append(Step(tool, argument, observation))
        return observation
