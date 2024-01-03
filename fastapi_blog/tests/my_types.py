from typing import Callable

from _pytest.fixtures import FixtureFunctionMarker

FixtureFunctionT = Callable[..., FixtureFunctionMarker]

# Определяется тип фикстуры FixtureFunctionT, который используется для типизации фикстур в тестах.
# Он может быть использован для определения типа функции, которая будет использоваться в качестве фикстуры,
# чтобы обеспечить более точную проверку типов и предотвратить ошибки во время выполнения.
