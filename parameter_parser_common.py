#
# Copyright (c) 2024 by Mika Laitio <lamikr@gmail.com>
#
# License: GNU Lesser General Public License (LGPL), version 2.1 or later.
# See the lgpl.txt file in the root directory or <http://www.gnu.org/licenses/lgpl-2.1.html>.
#

from enum import Enum
import os
import re

class ENUM_COMPONENT_WAREHOUSE(Enum):
	UNKNOWN = 0
	DIGIKEY = 1
	MOUSER = 2

class ENUM_COMPONENT_TYPE(Enum):
    UNKNOWN = 0
    RESISTOR = 1
    CAPACITOR = 2
    DIODE = 3
    LED = 4
    INDUCTOR = 5
    IC = 6
    CONNECTOR=7

regex_decint = r"(?:[1-9](?:_?\d)*|0+(_?0)*)"
regex_integer = rf"(?:{regex_decint})"

regex_digitpart = r"(?:\d(?:_?\d)*)"
regex_exponent = rf"(?:[eE][-+]?{regex_digitpart})"
regex_fraction = rf"(?:\.{regex_digitpart})"
regex_pointfloat = rf"(?:{regex_digitpart}?{regex_fraction}|{regex_digitpart}\.)"
regex_exponentfloat = rf"(?:(?:{regex_digitpart}|{regex_pointfloat}){regex_exponent})"
# we dont want to search exponent numbers from the description from now
#regex_floatnumber = rf"(?:{regex_pointfloat}|{regex_exponentfloat})"
regex_floatnumber = rf"(?:{regex_pointfloat})"

regex_any_number = rf"({regex_integer}|{regex_floatnumber})"
regex_any_temperature = rf"{regex_any_number}(F|f|C|c)"
