# Command Pattern Calculator CLI

A simple Python console calculator built using the Command Pattern with reversible operations (`undo`).

---

## Overview & Structure

Each calculator operation is encapsulated in its own class extending an abstract `Command` base:

- **`Command`**: Base class defining `execute(val)` and `undo(val)`.
- **Commands**:
  - `IncrementCommand`: Adds 1 (undo subtracts 1).
  - `DecrementCommand`: Subtracts 1 (undo adds 1).
  - `DoubleCommand`: Multiplies by 2 (undo divides by 2).
  - `RandAddCommand`: Adds a random integer and saves the generated delta in the instance so `undo()` subtracts the exact same offset.
- **`Calculator`**: Holds the running `current_value` and a `history` list. It runs commands and handles `undo` by popping the last command off the stack.
- **`COMMANDS` map**: A clean dictionary mapping command strings to their classes.

---

## Assumptions & Design Choices

To handle under-specified points from the requirements:

1. **`randadd` behavior:**
   - Generates a non-zero integer between `-100` and `100` (excluding `0`) so every call produces a noticeable change.
   - Stores the generated number in `self.delta` on that command instance so `undo()` reverses the exact number that was added.
2. **Output formatting:**
   - Supports both integers and floating-point inputs.
   - Values are rounded to 4 decimal places to prevent floating-point precision jitter (like `0.1 + 0.2`).
   - If a number is whole (e.g., `4.0` from `8 / 2`), it prints as an integer `4` to match the example output: `2, 3, 4, 8, 4, 3`.
3. **Empty history:**
   - If `undo` is called when history is empty, it prints `"No commands to undo."` without crashing.
4. **Input handling & exit:**
   - Inputs are stripped of whitespace and lowercased (`increment`, `INCREMENT`, etc.).
   - The loop can be exited anytime with `exit`, `quit`, or `Ctrl+C` / `Ctrl+D`.

---

## How to Run

Standard library only (Python 3.8+).

Run `main.py` with an initial number:

```bash
python3 main.py 1
```

### Example Session
```text
> increment
2
> increment
3
> increment
4
> double
8
> undo
4
> undo
3
> exit
```

---

## Running the Unit Tests

Automated tests are in `test_calculator.py`:

```bash
python3 test_calculator.py
```

Tests verify:
- The exact sequence from the task prompt (`1 -> increment, increment, increment, double, undo, undo -> 2, 3, 4, 8, 4, 3`).
- Math reversibility for `decrement` and `double`.
- Preserving and undoing random offsets in `RandAddCommand`.
- Empty undo stack safety.
- Input dictionary mapping.
