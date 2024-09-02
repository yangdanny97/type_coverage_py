def outer_function(a: int) -> int:
    def inner_function(b: int) -> int:
        return b * 2
    return inner_function(a) + (lambda x: x * 3)(a)