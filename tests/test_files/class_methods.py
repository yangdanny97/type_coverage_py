class ExampleClass:
    def __init__(self, value: int):
        self.value = value
    
    def compute(self, multiplier: int) -> int:
        return self.value * multiplier
    
    def no_return_annotation(self, x: float) -> None:
        pass