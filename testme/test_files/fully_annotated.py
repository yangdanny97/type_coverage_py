def func_with_annotations(x: int, y: str) -> bool:
    return x > 0

def another_func(z: float, flag: bool) -> str:
    return str(z) if flag else "nope"

class MyClass:
    def method(self, data: dict) -> None:
        self.data = data