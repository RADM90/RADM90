from sympy import Symbol, solve

# Unit 2
## 1)
k = Symbol('k')
equation = k - 2 - 4
print(solve(equation))

## 2)
k = Symbol('k')
equation = 2 * k - 10
print(solve(equation))

## 3)
k = Symbol('k')
equiation = k / 2 - 8
print(solve(equiation))

## p.30
x = Symbol('x')
y = Symbol('y')
eq1 = 3 * x + y - 2
eq2 = x - 2 * y - 3
print(solve((eq1, eq2), dict=True))


# Unit 9
from sympy import factor, expand
x = Symbol('x')
print(factor(x**2 + 6 * x + 5))
print(expand((x + 1) * (x + 5)))