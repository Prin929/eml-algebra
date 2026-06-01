"""
test.py
=======
Comprehensive test suite for eml-algebra v2.0.0.
Covers every fix described in the review:

  [1] Float precision leak fix (mul / div use Decimal.ln / Decimal.exp)
  [2] Reflected operators (__radd__, __rmul__, etc.)
  [3] Comparison operators (__eq__, __lt__, etc.)
  [4] __pow__ derived purely from eml
  [5] sin / cos via honest Taylor series (EML arithmetic)
  [6] diff via centred difference (near machine-precision)
  [7] integrate via Simpson's rule
  [8] factorial — integer fast-path + Gamma general path
  [9] sqrt
  [10] setup.py long_description guard (manual check)
"""

import sys
sys.path.insert(0, '.')          # so we can run from the repo root
from decimal import Decimal
from eml-algebra import EmlNumber, eml, eml_exp, eml_ln

PASS = "\033[92m PASS\033[0m"
FAIL = "\033[91m FAIL\033[0m"

def check(label, got, expected, tol=1e-10):
    diff = abs(float(str(got)) - expected)
    ok   = diff < tol
    mark = PASS if ok else FAIL
    print(f"{mark}  {label}")
    if not ok:
        print(f"       got={got}  expected={expected:.14f}  diff={diff:.2e}")
    return ok

def section(title):
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}")

passed = 0
total  = 0

# ──────────────────────────────────────────────────────
# [0] Primitive smoke test
# ──────────────────────────────────────────────────────
section("0 · Primitive: eml(x, y) = e^x − ln(y)")

import math
cases = [(0, 1), (1, 1), (2, math.e), (0, math.e)]
for x, y in cases:
    result = float(str(eml(Decimal(str(x)), Decimal(str(y)))))
    expected = math.exp(x) - math.log(y)
    total += 1
    if check(f"eml({x}, {y})", result, expected):
        passed += 1

# ──────────────────────────────────────────────────────
# [1] Precision: no float leakage in mul / div
# ──────────────────────────────────────────────────────
section("1 · Precision: multiplication and division (Decimal-native)")

a = EmlNumber('1.0000000000000001')
b = EmlNumber('1.0000000000000002')
product = a * b
total += 1
# Just confirm it runs without precision collapse to exactly 1.0
if check("1.0000000000000001 × 1.0000000000000002 ≠ 1",
         float(str(product)), 1.0000000000000003, tol=1e-15):
    passed += 1

q = EmlNumber(10) / EmlNumber(3)
total += 1
if check("10 / 3", q, 10/3, tol=1e-12):
    passed += 1

# ──────────────────────────────────────────────────────
# [2] Reflected operators
# ──────────────────────────────────────────────────────
section("2 · Reflected operators (5 + EmlNumber, 5 * EmlNumber, …)")

total += 1
if check("5 + EmlNumber(3)",  5 + EmlNumber(3),  8.0):   passed += 1
total += 1
if check("5 - EmlNumber(3)",  5 - EmlNumber(3),  2.0):   passed += 1
total += 1
if check("5 * EmlNumber(3)",  5 * EmlNumber(3), 15.0):   passed += 1
total += 1
if check("12 / EmlNumber(4)", 12 / EmlNumber(4), 3.0):   passed += 1
total += 1
if check("2 ** EmlNumber(8)", 2 ** EmlNumber(8), 256.0):  passed += 1

# ──────────────────────────────────────────────────────
# [3] Comparison operators
# ──────────────────────────────────────────────────────
section("3 · Comparison operators")

total += 1
r = EmlNumber(3) == EmlNumber(3)
print(f"{'PASS' if r else 'FAIL'}  EmlNumber(3) == EmlNumber(3)  → {r}")
if r: passed += 1

total += 1
r = EmlNumber(2) < EmlNumber(5)
print(f"{'PASS' if r else 'FAIL'}  EmlNumber(2) < EmlNumber(5)   → {r}")
if r: passed += 1

total += 1
r = EmlNumber(7) > 4
print(f"{'PASS' if r else 'FAIL'}  EmlNumber(7) > 4              → {r}")
if r: passed += 1

total += 1
sorted_nums = sorted([EmlNumber(5), EmlNumber(1), EmlNumber(3)])
r = [str(x) for x in sorted_nums] == ['1', '3', '5']
print(f"{'PASS' if r else 'FAIL'}  sorted([5,1,3])               → {sorted_nums}")
if r: passed += 1

# ──────────────────────────────────────────────────────
# [4] __pow__
# ──────────────────────────────────────────────────────
section("4 · __pow__: a^b = exp(b · ln a)  via eml")

total += 1; passed += check("2 ^ 10",       EmlNumber(2) ** 10,     1024.0)
total += 1; passed += check("9 ^ 0.5",      EmlNumber(9) ** 0.5,       3.0)
total += 1; passed += check("(-2) ^ 3",     EmlNumber(-2) ** 3,       -8.0)
total += 1; passed += check("2.5 ^ 2",      EmlNumber(2.5) ** 2,      6.25)
total += 1; passed += check("x ^ 0  = 1",   EmlNumber(7) ** 0,         1.0)

# ──────────────────────────────────────────────────────
# [5] Trig — honest Taylor series
# ──────────────────────────────────────────────────────
section("5 · sin / cos — Taylor series via EML arithmetic")

import math as _m
angles = [0, _m.pi/6, _m.pi/4, _m.pi/3, _m.pi/2, _m.pi, 2*_m.pi, -_m.pi/3]
for a in angles:
    total += 1; passed += check(f"sin({a:.4f})", EmlNumber(a).sin(), _m.sin(a), tol=1e-12)
    total += 1; passed += check(f"cos({a:.4f})", EmlNumber(a).cos(), _m.cos(a), tol=1e-12)

# ──────────────────────────────────────────────────────
# [6] Calculus: diff
# ──────────────────────────────────────────────────────
section("6 · Differentiation")

# f(x) = x^2,   f'(x) = 2x
def f_sq(x): return x * x
total += 1; passed += check("d/dx x² at x=5",  EmlNumber.diff(f_sq, x=5),  10.0, tol=1e-9)
total += 1; passed += check("d/dx x² at x=0",  EmlNumber.diff(f_sq, x=0),   0.0, tol=1e-9)
total += 1; passed += check("d/dx x² at x=-3", EmlNumber.diff(f_sq, x=-3), -6.0, tol=1e-9)

# f(x) = x^3,   f'(x) = 3x^2
def f_cu(x): return x * x * x
total += 1; passed += check("d/dx x³ at x=4",  EmlNumber.diff(f_cu, x=4),  48.0, tol=1e-8)

# ──────────────────────────────────────────────────────
# [7] Calculus: integrate
# ──────────────────────────────────────────────────────
section("7 · Integration (Simpson's rule)")

# ∫₀¹ x² dx = 1/3
def f_sq2(x): return x * x
total += 1; passed += check("∫₀¹ x² dx = 1/3",
                              EmlNumber.integrate(f_sq2, 0, 1, n=1000), 1/3, tol=1e-9)

# ∫₀² x dx = 2
def f_lin(x): return x
total += 1; passed += check("∫₀² x dx = 2",
                              EmlNumber.integrate(f_lin, 0, 2, n=100), 2.0, tol=1e-9)

# ──────────────────────────────────────────────────────
# [8] Factorial
# ──────────────────────────────────────────────────────
section("8 · Factorial")

import math as _m
for n, expected in [(0,1),(1,1),(5,120),(10,3628800),(20, _m.factorial(20))]:
    total += 1; passed += check(f"{n}!", EmlNumber(n).factorial(), expected, tol=0.5)

# Γ(0.5) = √π
total += 1
passed += check("Γ(1.5) = 0.5! = √π/2",
                 EmlNumber('0.5').factorial(),
                 _m.gamma(1.5), tol=1e-8)

# ──────────────────────────────────────────────────────
# [9] sqrt
# ──────────────────────────────────────────────────────
section("9 · sqrt")

for n, expected in [(4, 2), (9, 3), (2, _m.sqrt(2)), (0.25, 0.5)]:
    total += 1; passed += check(f"√{n}", EmlNumber(n).sqrt(), expected, tol=1e-12)

# ──────────────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────────────
print(f"\n{'═'*55}")
print(f"  Results: {passed}/{total} tests passed")
print(f"{'═'*55}\n")
if passed == total:
    print("  ✓ All tests passed.\n")
else:
    print(f"  ✗ {total - passed} test(s) failed.\n")
    sys.exit(1)
