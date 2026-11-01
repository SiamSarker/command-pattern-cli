"""
Unit tests for Command Pattern Calculator
"""

import unittest
from main import (
    Calculator,
    IncrementCommand,
    DecrementCommand,
    DoubleCommand,
    RandAddCommand,
    COMMANDS,
)


class TestCalculatorOperations(unittest.TestCase):
    def test_task_specification_example(self):
        """
        Verifies the exact sequence from the specification:
        Initial value: 1
        Sequence: increment, increment, increment, double, undo, undo
        Expected result values: 2, 3, 4, 8, 4, 3
        """
        calc = Calculator(1)
        self.assertEqual(calc.get_result(), 1)

        # 1. increment -> 2
        res1 = calc.run_command(IncrementCommand())
        self.assertEqual(res1, 2)
        self.assertEqual(calc.get_result(), 2)

        # 2. increment -> 3
        res2 = calc.run_command(IncrementCommand())
        self.assertEqual(res2, 3)
        self.assertEqual(calc.get_result(), 3)

        # 3. increment -> 4
        res3 = calc.run_command(IncrementCommand())
        self.assertEqual(res3, 4)
        self.assertEqual(calc.get_result(), 4)

        # 4. double -> 8
        res4 = calc.run_command(DoubleCommand())
        self.assertEqual(res4, 8)
        self.assertEqual(calc.get_result(), 8)

        # 5. undo -> 4
        res5 = calc.undo()
        self.assertEqual(res5, 4)
        self.assertEqual(calc.get_result(), 4)

        # 6. undo -> 3
        res6 = calc.undo()
        self.assertEqual(res6, 3)
        self.assertEqual(calc.get_result(), 3)

    def test_decrement(self):
        calc = Calculator(5)
        res = calc.run_command(DecrementCommand())
        self.assertEqual(res, 4)
        self.assertEqual(calc.undo(), 5)

    def test_double_fractional(self):
        calc = Calculator(2.5)
        res = calc.run_command(DoubleCommand())
        self.assertEqual(res, 5)
        self.assertEqual(calc.undo(), 2.5)

    def test_randadd_and_undo(self):
        """Ensures randadd creates a non-zero delta and undo restores original value."""
        calc = Calculator(10)
        rand_cmd = RandAddCommand()
        original_value = calc.get_result()

        calc.run_command(rand_cmd)
        self.assertNotEqual(calc.get_result(), original_value)
        self.assertEqual(calc.current_value, original_value + rand_cmd.delta)

        # Undo must restore the exact original value
        restored = calc.undo()
        self.assertEqual(restored, original_value)

    def test_randadd_with_fixed_delta(self):
        calc = Calculator(100)
        cmd = RandAddCommand(delta=42)
        self.assertEqual(calc.run_command(cmd), 142)
        self.assertEqual(calc.undo(), 100)

    def test_empty_undo(self):
        """Calling undo on an empty history should safely return None without throwing."""
        calc = Calculator(10)
        result = calc.undo()
        self.assertIsNone(result)
        self.assertEqual(calc.get_result(), 10)

    def test_commands_dictionary_mapping(self):
        self.assertIs(COMMANDS["increment"], IncrementCommand)
        self.assertIs(COMMANDS["decrement"], DecrementCommand)
        self.assertIs(COMMANDS["double"], DoubleCommand)
        self.assertIs(COMMANDS["randadd"], RandAddCommand)


if __name__ == "__main__":
    unittest.main()
