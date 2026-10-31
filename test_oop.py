class Student:
    def __init__(self, name: str, university: str):
        self.name = name
        self.university = university

    def introduce(self):
        print(f"Hi, I am {self.name} from {self.university}.")


class GraduateStudent(Student):
    def __init__(self, name: str, university: str, degree: str):
        super().__init__(name, university)
        self.degree = degree

    def introduce(self):
        print(f"Hi, I am {self.name} studying {self.degree} at {self.university}.")

s = GraduateStudent("Siam", "TU Chemnitz", "M.Sc. Automotive Software Engineering")
s.introduce()

from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, val:float) -> float:
        pass
    @abstractmethod
    def undo(self, val:float) -> float:
        pass

class IncrementCommand(Command):
    def execute(self, val:float) -> float:
        return val + 1

    def undo(self, val:float) -> float:
        return val - 1

class DecrementCommand(Command):
    def execute(self, val:float) -> float:
        return val - 1

    def undo(self, val:float) -> float:
        return val + 1

class DoubleCommand(Command):
    def execute(self, val:float) -> float:
        return val * 2

    def undo(self, val:float) -> float:
        return val / 2

class SimpleCalculator:
    def __init__(self, initial_value: float):
        self.current_value = initial_value
        self.history = []

    def run_command(self, command: Command):
        self.current_value = command.execute(self.current_value)
        self.history.append(command)
        print(f"Current value: {self.current_value}")

    def undo(self):
        if not self.history:
            print("No commands to undo.")
            return
        last_command = self.history.pop()
        self.current_value = last_command.undo(self.current_value)
        print(f"Undo: Current value: {self.current_value}")


# 5. Test it!
calc = SimpleCalculator(1)
calc.run_command(IncrementCommand())  # 1 + 1 = 2
calc.run_command(IncrementCommand())  # 2 + 1 = 3
calc.run_command(DoubleCommand())     # 3 * 2 = 6
calc.undo()                           # undo double -> 3
calc.undo()                           # undo increment -> 2