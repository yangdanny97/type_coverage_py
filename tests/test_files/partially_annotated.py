def func_partially_annotated(a, b: int) -> int:
    return a + b

def another_partially_annotated(x: float, y) -> None:
    pass

def no_annotations(x, y):
    return x + y