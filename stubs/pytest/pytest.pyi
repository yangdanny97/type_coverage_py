# pytest.pyi

from typing import Union

class ApproxBase:
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

def approx(
    expected: Union[float, complex, list[float], list[complex]],
    *,
    rel: Union[float, None] = None,
    abs: Union[float, None] = None,
    nan_ok: bool = False
) -> ApproxBase: ...