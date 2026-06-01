"""
pythoneml
=========
A recreational mathematics library that bootstraps every algebraic and
transcendental operation from a single primitive function:

    eml(x, y) = e^x − ln(y)

Public API
----------
EmlNumber  : the main numeric type
eml        : the raw primitive (Decimal → Decimal)
eml_exp    : e^x  via eml(x, 1)
eml_ln     : ln(y) via 1 − eml(0, y)
"""

from .core import EmlNumber
from .primitive import eml, eml_exp, eml_ln

__all__ = ['EmlNumber', 'eml', 'eml_exp', 'eml_ln']
__version__ = '2.0.0'
