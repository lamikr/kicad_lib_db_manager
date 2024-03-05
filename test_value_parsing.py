import re

decint = r"(?:[1-9](?:_?\d)*|0+(_?0)*)"
integer = rf"(?:{decint})"

digitpart = r"(?:\d(?:_?\d)*)"
exponent = rf"(?:[eE][-+]?{digitpart})"
fraction = rf"(?:\.{digitpart})"
pointfloat = rf"(?:{digitpart}?{fraction}|{digitpart}\.)"
exponentfloat = rf"(?:(?:{digitpart}|{pointfloat}){exponent})"
floatnumber = rf"(?:{pointfloat}|{exponentfloat})"
floatnumber = rf"(?:{pointfloat})"

regex1 = rf"({integer}|{floatnumber})(F|f|C|c)"
regex2 = r"[-+]?(?:{decint})$"
regex3 = decint
regex4 = floatnumber

number = re.compile(regex1)

test_str = ("asdasdas 33AF asdasdasds\n"
    "sdfasd 333c sadfsdaf\n"
    "asdfasd 33f asdfasd 3.3C 33F 33c ")

res = number.search(test_str)
print(res)

res = re.search(regex1, test_str)
print(res)

degree = res.group(0)
#degree = re.search(r"(?P<degree>[0-9]+F)",a1).group("degree")
print(degree)
