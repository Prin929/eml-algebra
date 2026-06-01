# eml-algebra

> *What if one function was enough?*

**eml-algebra** is a recreational mathematics library that bootstraps every algebraic and transcendental operation from a single primitive:

```
eml(x, y) = eˣ − ln(y)
```

Addition, multiplication, powers, roots, trig, calculus — all of it traces back to that one seed.

---

## Installation

```bash
pip install eml-algebra
```

## Quick Start

```python
from eml-algebra import EmlNumber

a = EmlNumber(6)
b = EmlNumber(2)

print(a + b)        # 8
print(a * b)        # 12
print(a ** b)       # 36
print(a.sqrt())     # 2.449...  (√6)

# Works with plain numbers on either side
print(5 + EmlNumber(3))   # 8
print(2 ** EmlNumber(8))  # 256

# Comparisons and sorting
print(EmlNumber(3) > 2)                               # True
print(sorted([EmlNumber(5), EmlNumber(1), EmlNumber(3)]))  # [1, 3, 5]
```

## Trig

```python
import math
angle = EmlNumber(math.pi / 4)

print(angle.sin())   # 0.70710678118655
print(angle.cos())   # 0.70710678118655
print(angle.tan())   # 1.0
```

Both `sin` and `cos` are computed via honest Taylor series — every intermediate multiplication and division routes through `eml`.

## Calculus

```python
# Differentiation — centred difference, h = 1e-30 inside 50-digit Decimal engine
def f(x):
    return x ** 3          # f(x) = x³,  f'(x) = 3x²

print(EmlNumber.diff(f, x=4))   # ≈ 48.0  (3 × 4² = 48)

# Integration — Simpson's rule
def g(x):
    return x * x           # ∫₀¹ x² dx = 1/3

print(EmlNumber.integrate(g, 0, 1))   # ≈ 0.3333333333333
```

## Factorial and Gamma

```python
print(EmlNumber(10).factorial())    # 3628800
print(EmlNumber(20).factorial())    # 2432902008176640000

# Works for non-integers via the Gamma function: n! = Γ(n+1)
print(EmlNumber('0.5').factorial()) # ≈ 0.886226925  (√π / 2)
```

## The Primitive Directly

```python
from eml-algebra import eml, eml_exp, eml_ln
from decimal import Decimal

print(eml(Decimal('1'), Decimal('1')))    # e¹ − ln(1) = e
print(eml_exp(Decimal('0')))              # e⁰ = 1
print(eml_ln(Decimal('1')))              # ln(1) = 0
```

---

## How It Works

The derivation chain:

| Operation | Derivation |
|-----------|-----------|
| `exp(x)` | `eml(x, 1)` |
| `ln(y)` | `1 − eml(0, y)` |
| `a × b` | `exp(ln\|a\| + ln\|b\|) × sign` |
| `a / b` | `exp(ln\|a\| − ln\|b\|) × sign` |
| `aᵇ` | `exp(b · ln a)` |
| `√x` | `x ^ 0.5` |
| `sin(x)` | Taylor series via EML arithmetic |
| `cos(x)` | Taylor series via EML arithmetic |

Full mathematical derivations are in [SIMULATION_PROOF.md](./SIMULATION_PROOF.md).

---

## Precision

All arithmetic runs inside Python's `decimal.Decimal` engine at **50 significant digits**. No intermediate result passes through a `float` — the 15-digit IEEE 754 ceiling never silently caps a computation.

---

## Running Tests

```bash
python test.py
```

52 tests covering the primitive, all four arithmetic operations, reflected operators, comparisons, powers, trig, differentiation, integration, factorial, and sqrt.

---

## License

MIT
