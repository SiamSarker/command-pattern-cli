"""
Automated Unit Tests for Command Pattern Calculator
Verifies all functional and architectural specifications.
"""

import unittest
from main import (
    Calculator,
    IncrementCommand,
    DecrementCommand,
    DoubleCommand,
    RandAddCommand,
    CommandFactory,
)


class TestCalculatorOperations(unittest.TestCase):
    def test_task_specification_example(self):
        """
        Verifies the exact sequence from the specification:
        Initial value: 1
        Sequence: increment, increment, increment, double, undo, undo
        Expected result sequence: 2, 3, 4, 8, 4, 3
        """
        calc = Calculator(1)
        self.assertEqual(calc.get_formatted_result(), "1")

        # 1. increment -> 2
        calc.execute_command(IncrementCommand())
        self.assertEqual(calc.get_formatted_result(), "2")

        # 2. increment -> 3
        calc.execute_command(IncrementCommand())
        self.assertEqual(calc.get_formatted_result(), "3")

        # 3. increment -> 4
        calc.execute_command(IncrementCommand())
        self.assertEqual(calc.get_formatted_result(), "4")

        # 4. double -> 8
        calc.execute_command(DoubleCommand())
        self.assertEqual(calc.get_formatted_result(), "8")

        # 5. undo -> 4
        calc.undo()
        self.assertEqual(calc.get_formatted_result(), "4")

        # 6. undo -> 3
        calc.undo()
        self.assertEqual(calc.get_formatted_result(), "3")

    def test_decrement(self):
        calc = Calculator(5)
        calc.execute_command(DecrementCommand())
        self.assertEqual(calc.current_value, 4)
        calc.undo()
        self.assertEqual(calc.current_value, 5)

    def test_double_fractional(self):
        calc = Calculator(2.5)
        calc.execute_command(DoubleCommand())
        self.assertEqual(calc.current_value, 5.0)
        self.assertEqual(calc.get_formatted_result(), "5")

    def test_randadd_and_undo(self):
        """Ensures randadd creates a valid delta and undo perfectly restores previous value."""
        calc = Calculator(10)
        rand_cmd = RandAddCommand()
        original_value = calc.current_value

        calc.execute_command(rand_cmd)
        self.assertNotEqual(calc.current_value, original_value)
        self.assertEqual(calc.current_value, original_value + rand_cmd.delta)

        # Undo must restore the exact original value
        calc.undo()
        self.assertEqual(calc.current_value, original_value)

    def test_randadd_with_fixed_delta(self):
        calc = Calculator(100)
        cmd = RandAddCommand(delta=42)
        calc.execute_command(cmd)
        self.assertEqual(calc.current_value, 142)
        calc.undo()
        self.assertEqual(calc.current_value, 100)

    def test_empty_undo(self):
        """Calling undo on an empty history should safely return None without throwing."""
        calc = Calculator(10)
        result = calc.undo()
        self.assertIsNone(result)
        self.assertEqual(calc.current_value, 10)

    def test_factory_command_creation(self):
        self.assertIsInstance(CommandFactory.create_command("increment"), IncrementCommand)
        self.assertIsInstance(CommandFactory.create_command("INCREMENT"), IncrementCommand)
        self.assertIsInstance(CommandFactory.create_command("decrement"), DecrementCommand)
        self.assertIsInstance(CommandFactory.create_command("double"), DoubleCommand)
        self.assertIsInstance(CommandFactory.create_command("randadd"), RandAddCommand)
        self.assertIsNone(CommandFactory.create_command("invalid_cmd"))


if __name__ == "__main__":
    unittest.main()
