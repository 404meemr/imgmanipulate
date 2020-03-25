'''
common.py

Common classes and functions for this project
'''

import enum

def hexToRGB(value):
	value = value.strip("0x");
	lv = len(value)
	
	return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# this text object prevents the functions from becoming too repetitive
# TODO: implement text decoration
class Text(object):
	def __init__(self, content, style, color, size, decoration):
		self.content = content
		self.style = style
		self.color = color
		self.size = size
		self.decoration = decoration

class Position(enum.Enum):
	TOP_LEFT = 0
	TOP_RIGHT = 1
	BOTTOM_LEFT = 2
	BOTTOM_RIGHT = 3
	CENTER = 4
	TOP_CENTER = 5
	BOTTOM_CENTER = 6

class Decoration(enum.Enum):
	NONE = 0
	UNDERLINE = 1
	BOX = 2

class ImageSize(enum.Enum):
	NORESIZE = 0
	EXTRA_SMALL = 1
	SMALL = 2
	MEDIUM = 3
	LARGE = 4
	EXTRA_LARGE = 5

class TextSize(enum.Enum):
	NORMAL = 20
	HEADING2 = 45
	HEADING1 = 50
	SUBTITLE = 80
	TITLE = 100

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
	# TODO: add transparency
	TRANSPARENT = -1

	# TODO: detect colors in the image and use those
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