"""
Regular Expressions
"""
import re

input_text = input("Validation Checker: ")

# e-Mail Address Validation (Simple)
pattern_email_simple = r"^\S+@\S+\.\S+$"
pattern_email_simple_extraction = r"\S+@\S+\.\S+"

# e-Mail Address Validation (Short -> MAIN)
pattern_email_short = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

# e-Mail Address Validation (General)
pattern_email = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"

# e-Mail Address Validation (RFC 5322: IETF Internet Message Format)
pattern_email_ietf = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"

# Mobile Contact Validation
pattern_mobile = "^\d{3}-\d{3,4}-\d{4}$"  # 010-1234-5678 형식
pattern_home = "^\d{2,3}-\d{2,4}-\d{4}$"  # 02-0000-0000 형식

# User ID Validation
pattern_id = r"^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$"  # 2 ~ 10자의 영대소문자로 시작하는 영문자, 숫자, 특수문자(_, .)
pattern_pw = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%&*?])[A-Za-z\d!@#$%&*?]{8,20}$"  # 8 ~ 20자의 영문자, 숫자, 특수문자(!@#$%&*?)

r"""
자주 사용하는 문자 클래스

\d	== [0-9]
\D	== [^0-9]
\w	== [a-zA-Z0-9]
\W	== [^a-zA-Z0-9]
\s	== [ \t\n\r\f\v] (공백 문자)
\S	== [^ \t\n\r\f\v] (공백 문자가 아닌 것)
\b	단어 경계 (`\w`와 `\W`의 경계)
\B	비단어 경계
"""


"""
Methods
"""
comp = re.compile(pattern_email)  # 반복적으로 패턴을 활용할 때 유리한 '패턴 컴파일', match(), search() 등에 사용 가능
# 아래 두 사용법은 동일한 결과를 return
print(comp.match(input))
print(re.match(pattern_email, input))

search = re.search(pattern_email, input)  # 패턴과 일치하는 첫 문자열 -> str
match = re.match(pattern_email, input)  # 패턴과 일치하면 -> re.Match 객체, 일치하지 않으면 -> None
fullmatch = re.fullmatch(pattern_email, input)  # 문자열이 패턴에 완전히 일치해야 -> re.Match, 일치하지 않으면 -> None
find_all = re.findall(pattern_email, input)  # 일치하는 모든 부분 문자열을 추출 -> List[str]
find_iter = re.finditer(pattern_email, input)  # 일치하는 모든 부분 문자열을 추출(iter객체라서 인덱스 활용 가능) -> Iter[re.Match]
escape = re.escape(pattern_email)  # 입력 문자의 특수문자를 Escape 처리
split = re.split(pattern_email, input, maxsplit=0)  # 입력 문자열을 입력 패턴으로 split -> List[str]
sub = re.sub(pattern_email, "ALTERNATIVE_STRING", input)  # 입력 문자열 중 패턴과 일치하는 것을 ALTERNATIVE_STRING으로 치환 -> str
subn = re.subn(pattern_email, "ALTERNATIVE_STRING", input)  # sub()와 동일하지만 결과 값이 다름 -> Tuple(str: 바뀐 문자열, int: 몇 번 바꿨나)


"""
Match Object
"""
# Functions
match.start()  # re.Match 객체에서 일치하는 문자열의 시작 인덱스 -> int
match.end()  # re.Match 객체에서 일치하는 문자열의 끝 인덱스 -> int
match.span()  # (start(), end()) -> Tuple(int, int)
match.expand()  #
match.group()  # re.Match 객체에서 일치하는 문자열 -> str
match.groups()  # re.Match 객체에서 '괄호'로 묶인 패턴과 일치하는 문자열 -> Tuple(str, ...)

# Attributes
match.pos
match.endpos
match.lastindex
match.lastgroup
match.re
match.string
