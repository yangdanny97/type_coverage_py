from typing import Optional, Union, List

def func_with_complex_types(a: Optional[int], b: Union[str, List[str]]) -> Union[bool, None]:
    if isinstance(b, list):
        return bool(a)
    return None