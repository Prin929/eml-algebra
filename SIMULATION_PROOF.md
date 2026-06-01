# SIMULATION PROOF — pythoneml

## Mathematical Foundations of the EML Algebra

> *Every algebraic and transcendental operation in this library is derived
> from the single primitive:*
>
> **eml(x, y) = eˣ − ln(y)**

---

## 1. The Primitive

Define the **EML primitive** over the domain x ∈ ℝ, y ∈ ℝ⁺:

```
eml : ℝ × ℝ⁺ → ℝ
eml(x, y) = eˣ − ln(y)
```

All library operations are compositions of `eml`. No external arithmetic
function is used in the algebraic layer.

---

## 2. Isolating the Exponential and Logarithm

### 2.1 The Exponential

Set y = 1. Since ln(1) = 0:

```
eml(x, 1) = eˣ − ln(1) = eˣ − 0 = eˣ
```

**Therefore:**  `exp(x) ≡ eml(x, 1)`

### 2.2 The Logarithm

Set x = 0. Since e⁰ = 1:

```
eml(0, y) = 1 − ln(y)
⟹  ln(y) = 1 − eml(0, y)
```

**Therefore:**  `ln(y) ≡ 1 − eml(0, y)`

---

## 3. The Four Arithmetic Operations

### 3.1 Addition and Subtraction

Addition and subtraction are preserved as direct Decimal field operations.
No derivation from `eml` is required because `eml` already performs
subtraction internally: `eml(x, y) = exp(x) − ln(y)`.

### 3.2 Multiplication

For a, b ∈ ℝ, ab ≠ 0:

```
ln|ab| = ln|a| + ln|b|
⟹  |ab| = exp(ln|a| + ln|b|)
⟹  ab   = sign(a) · sign(b) · exp(ln|a| + ln|b|)
```

where `sign(a) · sign(b) = +1` if a,b have the same sign, `−1` otherwise.

**In terms of eml:**

```
ab = sign · eml( ln|a| + ln|b|,  1 )
```

### 3.3 Division

```
ln|a/b| = ln|a| − ln|b|
⟹  a/b = sign · exp(ln|a| − ln|b|)
        = sign · eml( ln|a| − ln|b|,  1 )
```

### 3.4 Exponentiation

For a > 0, b ∈ ℝ:

```
aᵇ = exp(b · ln a) = eml( b · ln(a),  1 )
```

For a < 0, b must be an integer n:

```
aⁿ = (−1)ⁿ · |a|ⁿ = (−1)ⁿ · eml( n · ln|a|,  1 )
```

---

## 4. Transcendental Functions via Taylor Series

### 4.1 Sine

The Maclaurin series:

```
sin(x) = Σₖ₌₀^∞  (−1)ᵏ · x^(2k+1) / (2k+1)!
```

Each term is computed using EML multiplication and division.
The argument is reduced to (−π, π] before summation for rapid convergence.
The series is truncated when |term| < 10⁻⁴⁵.

### 4.2 Cosine

```
cos(x) = Σₖ₌₀^∞  (−1)ᵏ · x^(2k) / (2k)!
```

Same approach as sine; derived from the same Taylor framework.

### 4.3 Tangent

```
tan(x) = sin(x) / cos(x)
```

Reuses the EML division operation defined in §3.3.

---

## 5. Square Root

```
√x = x^(1/2) = exp( (1/2) · ln x ) = eml( (1/2) · ln x,  1 )
```

This is handled by `__pow__(0.5)`, which is in turn derived from §3.4.

---

## 6. Factorial and the Gamma Function

For non-negative integer n ≤ 170:

```
n! = 1 × 2 × 3 × … × n
```

Each multiplication uses the EML multiplication defined in §3.2.

For general real z > 0, the **Lanczos approximation** to Γ(z) is used:

```
Γ(z) ≈ √(2π) · (z + g − 1/2)^(z − 1/2) · e^(−(z+g−1/2)) · A_g(z)
```

where A_g(z) is a rational approximation with g = 7, coefficients from
*Numerical Recipes* (Press et al.). All exponential and power operations
inside the Lanczos formula are computed through `eml_exp` and `eml_ln`.

**Factorial** is then recovered via `n! = Γ(n+1)`.

---

## 7. Numerical Differentiation

### 7.1 Centred Difference (default)

```
f'(x) ≈ [ f(x + h) − f(x − h) ] / (2h)
```

Using h = 10⁻³⁰ inside the 50-digit Decimal engine, this gives
effectively full-precision derivatives for smooth EmlNumber functions.
The centred formula has error O(h²) vs O(h) for the one-sided version,
which matters at small h where floating-point normally collapses.

### 7.2 First-Principles (one-sided, available as `method='first_principles'`)

```
f'(x) ≈ [ f(x + h) − f(x) ] / h
```

---

## 8. Numerical Integration

### 8.1 Simpson's Rule

```
∫ₐᵇ f(x) dx ≈ (h/3) · [ f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + … + f(xₙ) ]
```

where h = (b − a)/n and n is even. All arithmetic over the nodes and
coefficients is performed with EmlNumber (i.e., through `eml`).

Error bound: O(h⁴) per sub-interval, O(h⁴) globally.

---

## 9. Precision Architecture

The library uses Python's `decimal.Decimal` with 50 significant digits
throughout. Critically, **no intermediate result ever passes through a
Python `float`** in the arithmetic layer — the known 15–17 digit ceiling
of IEEE 754 doubles would otherwise silently corrupt high-precision
computations. The Decimal type's native `.exp()` and `.ln()` methods are
used inside `primitive.py` to ensure the 50-digit guard is never broken.

---

## 10. Composition Identity

Every exported operation satisfies the composition identity:

```
op(a, b) = F( eml(·, ·), a, b )
```

for some closed-form function F. The library is therefore a
*bootstrapped algebra*: one transcendental seed, all operations grown
from it.
