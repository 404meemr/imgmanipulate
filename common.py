'''
common.py

Common classes and functions for this project
'''

import enum

def hexToRGB(value):
	value = value.strip("0x");
	lv = len(value)
	return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class Text(object):
	def __init__(self, text, style, color):
		this.text = text
		this.style = style
		this.color = color

# holds a list of text objects
# all text objects get placed at the same position
class Group(object):
	def __init__(self, items):
		this.items = items

# the only reason these exist is to make it easier on the user
# by sacrificing performance
class Position(enum.Enum):
	TOP_LEFT = 0
	TOP_RIGHT = 1
	BOTTOM_LEFT = 2
	BOTTOM_RIGHT = 3
	CENTER = 4

# TODO: support word wrapping
class ALIGN(enum.Enum):
	LEFT = 0
	RIGHT = 1
	CENTER = 3

# we can get the value like so: Font.REGULAR.value
class Font(enum.Enum):
	REGULAR = 0
	ITALIC = 1
	SEMIBOLD = 2
	BOLD = 3
	LIGHT = 4
	MEDIUM = 5
	THIN = 6
	SEMIBOLD_ITALIC = 7
	BOLD_ITALIC = 8
	LIGHT_ITALIC = 9
	MEDIUM_ITALC = 10
	THIN_ITALIC = 11

# this one is a bit crusty
# numbers will be converted to hex and then to rgb
class Color(enum.Enum):
	TRANSPARENT = -1

	# TODO: detect the color in the image and use that
	PRIMARY = -2
	SECONDARY = -3
	TERTIARY = -4

	# TODO: add analagous colors for primary, secondary, and tertiary

	BLACK = 0
	WHITE = 14540253
	RED = 16326688
	LIGHTRED = 16539206
	LIGHTYELLOW = 16562502
	ORANGE = 16740397
	LIGHTBLUE = 7973329
	LIGHTCYAN = 7983564
	LIGHTPURPLE = 7962065
	MAGENTA = 16533129