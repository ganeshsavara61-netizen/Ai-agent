import unittest

from agent import Agent, TOOLS
from agent.tools import calculate


class ToolTests(unittest.TestCase):
    def test_calculate(self):
        self.assertEqual(calculate("2 * (3 + 4)"), "14")
        self.assertEqual(calculate("7 / 2"), "3.5")
        self.assertEqual(calculate("-3 + 1"), "-2")

    def test_calculate_rejects_unsafe_input(self):
        self.assertTrue(calculate("__import__('os')").startswith("error"))
        self.assertTrue(calculate("2 ** 1000").startswith("error"))

    def test_division_by_zero(self):
        self.assertEqual(calculate("1/0"), "error: division by zero")


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.agent = Agent(TOOLS)

    def test_routes_to_calculator(self):
        self.assertEqual(self.agent.run("what is 6 * 7?"), "42")

    def test_routes_to_word_count(self):
        self.assertEqual(self.agent.run("count words in hello big world"), "3 words, 15 characters")

    def test_routes_to_reverse(self):
        self.assertEqual(self.agent.run("reverse: abc"), "cba")

    def test_unknown_task(self):
        self.assertIn("don't know", self.agent.run("sing a song"))

    def test_history_recorded(self):
        self.agent.run("calc 1 + 1")
        self.assertEqual(self.agent.history[0].tool, "calculate")
        self.assertEqual(self.agent.history[0].observation, "2")

    def test_custom_planner(self):
        agent = Agent(TOOLS, planner=lambda task: ("reverse", task))
        self.assertEqual(agent.run("xyz"), "zyx")


if __name__ == "__main__":
    unittest.main()
