"""
primitive.py
============
The single seed of the entire eml-algebra library.

    eml(x, y) = e^x − ln(y)

Every algebraic and transcendental operation in this library is derived
from this one primitive — no other math is imported into the arithmetic
layer.  The Decimal engine is set to 50 significant digits so that the
precision is never silently consumed by floating-point rounding.
"""

from decimal import Decimal, getcontext

# 50-digit guard: keeps exponent/log chains precise through deep compositions
getcontext().prec = 50

# ---------------------------------------------------------------------------
# Decimal-native constants derived without importing math
# ---------------------------------------------------------------------------

def _dec_exp(x: Decimal) -> Decimal:
    """
    Pure-Decimal e^x using Decimal.exp().
    This is the ONLY place where exponentiation is evaluated;
    everything else calls eml(x, 1).
    """
    return x.exp()


def _dec_ln(y: Decimal) -> Decimal:
    """
    Pure-Decimal ln(y) using Decimal.ln().
    Requires y > 0.
    """
    if y <= 0:
        raise ValueError(
            f"Domain Error in ln: argument must be > 0, got {y}."
        )
    return y.ln()


# ---------------------------------------------------------------------------
# The Primitive
# ---------------------------------------------------------------------------

def eml(x: Decimal, y: Decimal) -> Decimal:
    """
    The Absolute Mathematical Primitive:

        eml(x, y) = e^x − ln(y)

    Rules
    -----
    - x  : any Decimal (the exponent argument)
    - y  : strictly positive Decimal (the logarithm argument)
    - All arithmetic stays inside the Decimal 50-digit engine.

    Derivations
    -----------
    eml(x, 1)      = e^x − ln(1) = e^x − 0 = e^x
    eml(0, y)      = 1  − ln(y)
    eml(ln(a), y)  = a  − ln(y)
    """
    if not isinstance(x, Decimal):
        x = Decimal(str(x))
    if not isinstance(y, Decimal):
        y = Decimal(str(y))

    if y <= Decimal('0'):
        raise ValueError(
            f"Domain Error: y must be strictly > 0 for ln(y); got y = {y}."
        )

    try:
        return _dec_exp(x) - _dec_ln(y)
    except OverflowError:
        raise OverflowError(
            f"EML Engine Overflow running eml({x}, {y}). "
            "The arguments exceed the representable range."
        )


# ---------------------------------------------------------------------------
# Derived single-argument helpers (still expressed through eml)
# ---------------------------------------------------------------------------

def eml_exp(x: Decimal) -> Decimal:
    """e^x  ≡  eml(x, 1)"""
    return eml(x, Decimal('1'))


def eml_ln(y: Decimal) -> Decimal:
    """ln(y)  ≡  e^0 − eml(0, y)  =  1 − (1 − ln y)  =  ln y"""
    # eml(0, y) = e^0 − ln(y) = 1 − ln(y)
    # therefore  ln(y) = 1 − eml(0, y)
    return Decimal('1') - eml(Decimal('0'), y)
