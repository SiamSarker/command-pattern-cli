# Console Calculator with Command Pattern and Undo Mechanics

A command-line application implemented in Python demonstrating the **Command Pattern (GoF)**, encapsulation of state modifications, inverse execution (undo stack), and clean object-oriented architecture.

**Author:** Md Siam Hossain Sarker  
**Position:** Werkstudent:in Technische Informatik  
**Target Organization:** ekvip automation GmbH  

---

## 1. Architectural Overview

The application follows the classic **Gang of Four (GoF) Command Design Pattern**:

```
           +---------------------+
           |   Command (ABC)     |
           +---------------------+
           | + execute(val): val |
           | + undo(val): val    |
           +----------+----------+
                      |
     +----------------+----------------+----------------+
     |                |                |                |
+----+--------+ +-----+--------+ +-----+--------+ +-----+--------+
|  Increment  | |  Decrement   | |   Double     | |   RandAdd    |
|   Command   | |   Command    | |   Command    | |   Command    |
+-------------+ +--------------+ +--------------+ +--------------+
```

### Components
1. **`Command` (Abstract Base Class):** Declares the unified interface `execute(current_value)` and `undo(current_value)`.
2. **Concrete Commands:**
   - `IncrementCommand`: Increases the value by 1; undo decreases by 1.
   - `DecrementCommand`: Decreases the value by 1; undo increases by 1.
   - `DoubleCommand`: Multiplies the value by 2; undo divides by 2.
   - `RandAddCommand`: Adds a random integer $\Delta \in [-100, 100] \setminus \{0\}$. The generated delta is stored in the command instance so that an `undo` operation subtracts the exact same delta.
3. **`Calculator` (Invoker & State Holder):**
   - Holds the `current_value` state.
   - Maintains an internal history stack (`_history: List[Command]`).
   - Pushes executed commands to the stack and pops them upon `undo()`.
4. **`CommandFactory`:** Isolates string parsing and command instantiation from the business logic.

---

## 2. Assumptions for Under-Specified Requirements

As requested by the task instructions, all assumptions have been explicitly documented:

1. **Random Number Range (`randadd`):**
   - Assumed a uniform random integer between `-100` and `100`, excluding `0`.
   - Excluding `0` ensures that invoking `randadd` always produces an observable change in the result variable.
2. **Empty History Undo:**
   - If `undo` is invoked when no prior reversible operations exist on the stack, the system performs a safe no-op, prints an informative message (`Nothing to undo`), and leaves the current result intact without crashing.
3. **Number Formatting:**
   - Both integers and floating-point values are supported.
   - Result values that represent whole numbers (e.g. `4.0`) are formatted as integers (`4`) to align with the prompt's reference output: `2, 3, 4, 8, 4, 3`.
4. **Command Normalization & Graceful Exit:**
   - Command inputs are stripped of whitespace and evaluated case-insensitively (`increment`, `INCREMENT`, and ` increment ` are all recognized).
   - In addition to running in an infinite loop, users can cleanly exit via `exit`, `quit`, or `Ctrl+C` / `Ctrl+D` (KeyboardInterrupt/EOF).

---

## 3. How to Run

### Requirements
- Python 3.8+ (standard library only; no external dependencies required)

### Execution
Run `main.py` with the initial number as a command-line argument:

```bash
python3 main.py 1
```

### Example Session
```text
Calculator started with initial value: 1
Available commands: increment | decrement | double | randadd | undo | exit
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
Exiting calculator. Goodbye!
```

---

## 4. Running the Unit Tests

An automated test suite using Python's built-in `unittest` framework is included in `test_calculator.py`.

Run the test suite with:

```bash
python3 -m unittest test_calculator.py
```

All 7 test cases verify:
- The exact sequence from the specification (`1 -> increment, increment, increment, double, undo, undo -> 2, 3, 4, 8, 4, 3`).
- Reversibility of all arithmetic operations (`decrement`, `double`).
- Preservation of the random delta during `RandAddCommand.undo()`.
- Safe boundary handling for empty undo stacks.
- Case-insensitive factory instantiation.
