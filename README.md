# Command Pattern Calculator CLI

A command-line program in Python built using the **Command Pattern (GoF)** with reversible operations (undo stack).

Developed for the Werkstudent coding challenge at **ekvip automation GmbH**.

---

## 1. Design & Architecture

The application implements the Command Pattern where each operation is encapsulated in its own class inheriting from an abstract `Command` base:

- **`Command` (Base Interface):** Defines `execute(val)` and `undo(val)`.
- **Concrete Commands:**
  - `IncrementCommand`: Adds 1 (undo subtracts 1).
  - `DecrementCommand`: Subtracts 1 (undo adds 1).
  - `DoubleCommand`: Multiplies by 2 (undo divides by 2).
  - `RandAddCommand`: Adds a random integer and stores the generated delta in the instance so `undo()` subtracts the exact same offset.
- **`Calculator` (Invoker & State Holder):** Holds `current_value` and a `history` stack of executed commands. It pushes commands on execution and pops them on `undo()`.
- **Command Dispatching:** Uses a clean dictionary mapping (`COMMANDS`) to map user input strings to their corresponding command classes.

---

## 2. Assumptions for Under-Specified Requirements

1. **`randadd` Range & Behavior:**
   - Generates a non-zero integer between `-100` and `100` (excluding `0`) so every call produces a noticeable change in state.
   - The generated delta is stored in `self.delta` inside the command instance, ensuring that `undo()` subtracts the exact number that was added.
2. **Result Formatting:**
   - Both integers and floating-point values are supported.
   - Results are rounded to 4 decimal places to prevent binary floating-point precision jitter (e.g., `0.1 + 0.2`).
   - If a result is a whole number (e.g. `4.0` from `8 / 2`), it is displayed as an integer (`4`) to match the prompt's reference output: `2, 3, 4, 8, 4, 3`.
3. **Empty Undo Stack:**
   - If `undo` is called when no previous operations exist on the stack, it outputs `"No commands to undo."` without crashing.
4. **Input Normalization & Graceful Exit:**
   - Inputs are stripped of whitespace and lowercased (`increment`, `INCREMENT`, etc.).
   - The user can exit the infinite loop by typing `exit`, `quit`, or pressing `Ctrl+C` / `Ctrl+D`.

---

## 3. How to Run

Requires Python 3.8+ (standard library only).

Run `main.py` with the initial number as a command-line argument:

```bash
python3 main.py 1
```

### Example Session (matching the prompt sequence):
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

## 4. Running the Tests

An automated test suite using Python's built-in `unittest` is provided in `test_calculator.py`:

```bash
python3 test_calculator.py
```

All 7 test cases verify:
- The exact sequence from the specification (`1 -> increment, increment, increment, double, undo, undo -> 2, 3, 4, 8, 4, 3`).
- Reversibility of arithmetic operations (`decrement`, `double`).
- Preservation and exact undo of random deltas in `RandAddCommand`.
- Boundary handling when calling undo on an empty stack.
- Input command dictionary mapping.
