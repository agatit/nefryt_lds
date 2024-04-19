from dataclasses import dataclass

@dataclass
class A:
    a = "222"
    def __init__(self):
        self.a = 123


a = A()
print(a.a)
print(a.b is None)