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