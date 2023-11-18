from pygame.color import Color
from typing import Tuple, Sequence, Union

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int],
                   RGBAOutput, Sequence[int]]

Pos = Tuple[float, float]
