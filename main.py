"""
Console Program: Command Pattern Calculator with Undo Support
Candidate: Md Siam Hossain Sarker
Role: Werkstudent:in Technische Informatik (ekvip automation GmbH)

TASK SPECIFICATION & ASSUMPTIONS:
1. Command Line Argument:
   - Accepts exactly one argument as the initial numerical value.
   - Handled as float/int, validating against invalid or missing input.
2. Result Formatting:
   - If a number is an integer (e.g. 4.0), it is displayed as integer (4)
     to match the specification's reference example (2, 3, 4, 8, 4, 3).
3. Random Addition ('randadd'):
   - Generates a non-zero integer between -100 and 100 (excluding 0)
     to guarantee a tangible state change.
   - The generated delta is stored in the command instance so that
     an 'undo' operation reverses the exact same offset.
4. Undo Behavior:
   - Reverts the most recent command on the history stack.
   - Calling 'undo' when the history is empty is treated as a safe no-op
     with an informative message, keeping the current value intact.
5. Command Case & Whitespace:
   - Input is trimmed and converted to lowercase for robust user interaction.
6. Graceful Termination:
   - In addition to running in an infinite loop, the program allows
     clean termination via 'exit', 'quit', or EOF/KeyboardInterrupt.
"""

import sys
import random
from abc import ABC, abstractmethod
from typing import List, Optional, Union


# =====================================================================
# 1. Command Pattern: Abstract Base Class
# =====================================================================
class Command(ABC):
    """
    Abstract base class for all calculator operations.
    Each command encapsulates both execution and inverse (undo) logic.
    """

    @abstractmethod
    def execute(self, current_value: float) -> float:
        """Applies the command operation to current_value and returns the new value."""
        pass

    @abstractmethod
    def undo(self, current_value: float) -> float:
        """Reverts the command operation and returns the previous value."""
        pass


# =====================================================================
# 2. Concrete Command Implementations
# =====================================================================
class IncrementCommand(Command):
    """Increments the current result value by 1."""

    def execute(self, current_value: float) -> float:
        return current_value + 1

    def undo(self, current_value: float) -> float:
        return current_value - 1


class DecrementCommand(Command):
    """Decrements the current result value by 1."""

    def execute(self, current_value: float) -> float:
        return current_value - 1

    def undo(self, current_value: float) -> float:
        return current_value + 1


class DoubleCommand(Command):
    """Doubles the current result value."""

    def execute(self, current_value: float) -> float:
        return current_value * 2

    def undo(self, current_value: float) -> float:
        return current_value / 2


class RandAddCommand(Command):
    """
    Adds a random non-zero integer (between -100 and 100) to the result.
    The generated delta is stored within the instance to guarantee exact undoing.
    """

    def __init__(self, delta: Optional[int] = None):
        # Allow passing delta directly (useful for deterministic unit testing)
        if delta is not None:
            self.delta = delta
        else:
            # Pick a non-zero random integer between -100 and 100
            possible_values = [x for x in range(-100, 101) if x != 0]
            self.delta = random.choice(possible_values)

    def execute(self, current_value: float) -> float:
        return current_value + self.delta

    def undo(self, current_value: float) -> float:
        return current_value - self.delta


# =====================================================================
# 3. Invoker / Calculator Engine
# =====================================================================
class Calculator:
    """
    Maintains the current state of the result and the command history stack.
    Handles command execution and undo mechanics.
    """

    def __init__(self, initial_value: float):
        self._current_value: float = initial_value
        self._history: List[Command] = []

    @property
    def current_value(self) -> float:
        return self._current_value

    def execute_command(self, command: Command) -> float:
        """Executes a command, records it in history, and returns the updated value."""
        self._current_value = command.execute(self._current_value)
        self._history.append(command)
        return self._current_value

    def undo(self) -> Optional[float]:
        """
        Reverts the most recent command that was not yet undone.
        Returns the new value, or None if there is no command to undo.
        """
        if not self._history:
            return None

        last_command = self._history.pop()
        self._current_value = last_command.undo(self._current_value)
        return self._current_value

    def get_formatted_result(self) -> str:
        """
        Formats the current value cleanly:
        Whole numbers are shown as integers (e.g. 4 instead of 4.0).
        Floating-point numbers preserve decimals (rounded to 4 decimal places).
        """
        val_float = float(self._current_value)
        if val_float.is_integer():
            return str(int(val_float))
        return f"{val_float:.4f}".rstrip("0").rstrip(".")


# =====================================================================
# 4. Command Factory & Dispatcher
# =====================================================================
class CommandFactory:
    """Creates command instances corresponding to user input strings."""

    @staticmethod
    def create_command(name: str) -> Optional[Command]:
        normalized = name.strip().lower()
        if normalized == "increment":
            return IncrementCommand()
        elif normalized == "decrement":
            return DecrementCommand()
        elif normalized == "double":
            return DoubleCommand()
        elif normalized == "randadd":
            return RandAddCommand()
        return None


# =====================================================================
# 5. CLI Execution & Interactive Loop
# =====================================================================
def parse_initial_value() -> float:
    """Parses and validates the initial value from command-line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <initial_number>")
        print("Example: python main.py 1")
        sys.exit(1)

    try:
        return float(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid number.")
        sys.exit(1)


def main():
    initial_value = parse_initial_value()
    calculator = Calculator(initial_value)

    print(f"Calculator started with initial value: {calculator.get_formatted_result()}")
    print("Available commands: increment | decrement | double | randadd | undo | exit")

    while True:
        try:
            user_input = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting calculator. Goodbye!")
            break

        if not user_input:
            continue

        normalized_input = user_input.lower()

        # Check for exit command
        if normalized_input in ("exit", "quit"):
            print("Exiting calculator. Goodbye!")
            break

        # Handle undo
        if normalized_input == "undo":
            result = calculator.undo()
            if result is None:
                print(f"Nothing to undo. Current value: {calculator.get_formatted_result()}")
            else:
                print(calculator.get_formatted_result())
            continue

        # Handle operation commands
        command = CommandFactory.create_command(normalized_input)
        if command is None:
            print(f"Unknown command '{user_input}'. Supported commands: increment, decrement, double, randadd, undo, exit")
            continue

        calculator.execute_command(command)
        print(calculator.get_formatted_result())


if __name__ == "__main__":
    main()
