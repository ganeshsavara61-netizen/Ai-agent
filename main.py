"""Command line entry point: python main.py "calculate 2 * (3 + 4)" or run with no args for a prompt."""
import sys

from agent import Agent, TOOLS


def main(argv):
    agent = Agent(TOOLS)
    if len(argv) > 1:
        print(agent.run(" ".join(argv[1:])))
        return 0
    print("Agent ready. Type a task, or 'quit'.")
    while True:
        try:
            task = input("> ").strip()
        except EOFError:
            return 0
        if task.lower() in {"quit", "exit"}:
            return 0
        if task:
            print(agent.run(task))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
