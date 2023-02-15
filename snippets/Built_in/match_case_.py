"""
Valid from Python ver. 3.10.0
"""


def http_status(code):
    # Literal Case
    match int(code):
        case 200:
            return "Success"
        case 206:
            return "Partial Content"
        case 400:
            return "Bad request"
        case 401:
            return "Unauthorized"
        case 403:
            return "Forbidden"
        case 404:
            return "Not found"
        case 405:
            return "Method Not Allowed"
        case 500 | 502 | 503:
            return "Something's wrong on the server side"
        case _:  # Wild-card // 왜 else가 아닐까..는 의문
            return f"Something's wrong, Status code: {code}"


# Unpacking Example
point = (640, 480)
# point is an (x, y) tuple
match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"Y={y}")
    case (x, 0):
        print(f"X={x}")
    case (x, y):
        print(f"X={x}, Y={y}")
    case _:
        raise ValueError("Not a point")


# 클래스에도 적용 가능
class Point:
    x: int
    y: int


def where_is(point):
    """"Point(x, 0) 가 Point.__new__를 호출하지도 않고, x라는 변수를 찾는 것도 아닌 ,완전히 새로운 의미"""
    match point:
        case Point(x=0, y=0):
            print("Origin")
        case Point(x=0, y=y):
            print(f"Y={y}")
        case Point(x=x, y=0):
            print(f"X={x}")
        case Point():
            print("Somewhere else")
        case _:
            print("Not a point")


"""points
Point(1, var)
Point(1, y=var)
Point(x=1, y=var)
Point(y=var, x=1)
"""
match points:
    case []:
        print("No points")
    case [Point(0, 0)]:
        print("The origin")
    case [Point(x, y)]:
        print(f"Single point {x}, {y}")
    case [Point(0, y1), Point(0, y2)]:
        print(f"Two on the Y axis at {y1}, {y2}")
    case _:
        print("Something else")


# Guard: 가드가 거짓이면 계속해서 다음 케이스를 시도
match point:
    case Point(x, y) if x == y:
        print(f"Y=X at {x}")
    case Point(x, y):
        print(f"Not on the diagonal")
    # 하위 패턴은 다음 키워드를 사용하여 캡처 가능 (아래 예시는 Point(x2, y2)를 p2로 alias
    # case (Point(x1, y1), Point(x2, y2) as p2): ...


# Enumeration 상수도 사용 가능
from enum import Enum
class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

color = Color(input("Enter your choice of 'red', 'blue' or 'green': "))

match color:
    case Color.RED:
        print("I see red!")
    case Color.GREEN:
        print("Grass is green")
    case Color.BLUE:
        print("I'm feeling the blues :(")
