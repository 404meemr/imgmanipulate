'''
Some ideas
----------
- we can do an environmental conservation organization
- finding an existing name is easier than making one up imo
(don't remove these links)
- heres a cool image: https://www.pexels.com/photo/light-house-on-hill-3363331/
- here's another cool image: https://www.pexels.com/photo/calm-body-of-water-1363876/
- here's an even better image: https://www.pexels.com/photo/landscape-photography-of-mountains-covered-in-snow-691668/ (I want to use this)
- we can slightly round the corners
- add some block text in the middle that is the color of the primary color of the image
- we can put translucent, almost transparent long rectangles on the image
'''

'''
Positioning
-----------
	Position:
		- TOP_LEFT
		- TOP_CENTER
		- TOP_RIGHT
		- CENTER
		- BOTTOM_LEFT
		- BOTTOM_CENTER
		- BOTTOM_RIGHT
	As of right now, you are not allowed to choose coordinates.

	Usage: Position.<option>
	Example: Position.TOP_RIGHT

Text API
--------
This program has an incredibly powerful and customizable text generation API.

	Font Styles:
		- REGULAR
		- ITALIC
		- SEMIBOLD
		- BOLD
		- LIGHT
		- MEDIUM
		- THIN
		- SEMIBOLD_ITALIC
		- BOLD_ITALIC
		- LIGHT_ITALIC
		- MEDIUM_ITALIC
		- THIN_ITALIC

	Colors:
		- BLACK
		- WHITE
		- LIGHTRED
		- LIGHTYELLOW
		- ORANGE
		- LIGHTBLUE
		- LIGHTCYAN
		- LIGHTPURPLE
		- MAGENTA
	You can also provide your own colors in an RGBA formatted tuple
	e.x: (255, 255, 255, 255)
	Background colors are not supported.
	
	TextSize:
		- NORMAL
		- HEADING2
		- HEADING1
		- SUBTITLE
		- TITLE

	Decoration:
		- NONE
		- UNDERLINE
		- BOX

	It should be noted that when adding multiple pieces of text aligned to CENTER,
	only the first item will be centered in the image on the y axis, not the entire
	group of texts combined

	Adding text one at a time:
	--------------------------
	First, you will need to create a Text object.
	Text objects can hold the following:
		- content
		- font style
		- color
		- text size
		- decoration
	e.x: myTitle = Text("foo", Font.BOLD, Color.LIGHTRED, 120, Decoration.BOX)

	Then you can put the text on an image by specifying a filepath and a position
	e.x: addText("input file path", myTitle, Position.BOTTOM_CENTER)

	Adding more than one text at a time:
	------------------------------------
	If you choose to add multiple texts at a time, they will share the same position.
	For example, a title and subtitle will both be center aligned.

	myTitle = Text("foo", Font.BOLD, Color.LIGHTRED, 120, Decoration.BOX)
	mySubtitle = Text("bar", Font.MEDIUM, Color.WHITE, 80, Decoration.NONE)
	myFooter = Text("baz", Font.LIGHT, Color. WHITE, 50, Decoration.UNDERLINE)

	addText("input file path", [myTitle, mySubtitle], Position.CENTER)
	addText("input file path", myFooter, Position.BOTTOM_CENTER)

	In this case, both myTitle and mySubtitle will be centered in both the x and y axis, while myFooter
	will be centered at the bottom of the page on the x axis.

	Image API
	---------

		ImageSize:
		- NORESIZE
		- EXTRA_SMALL
		- SMALL
		- MEDIUM
		- LARGE
		- EXTRA_LARGE

		At this point, images can only be composited on top of each other.
		The foreground image can be given a position on the screen.

		ImageSize specifies the amount of *scaling* to perform on the image.
		You can either specify your own scale factor, use ImageSize, or submit your own
		image dimensions in a tuple.

		addImage("background", "foreground", scale, position)

		e.x: addImage("background", "foreground", Image.SMALL, Position.TOP_CENTER)
		e.x: addImage("background", "foreground", 0.5, Position.CENTER)
		e.x: addImage("background", "foreground", (500, 200), Position.TOP_RIGHT)
'''

import matplotlib.pyplot as plt 
import os.path  
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont 
from PIL import ImageChops
from common import *

def round_corners_one_image(original_image, percent_of_side=.3):
  """ Rounds the corner of a PIL.Image
  
  original_image must be a PIL.Image
  Returns a new PIL.Image with rounded corners, where
  0 < percent_of_side < 1
  is the corner radius as a portion of the shorter dimension of original_image
  """
  #set the radius of the rounded corners
  width, height = original_image.size
  radius = int(percent_of_side * min(width, height)) # radius in pixels
  
  ###
  #create a mask
  ###
  
  #start with transparent mask
  rounded_mask = PIL.Image.new('RGBA', (width, height), (127,0,127,0))
  drawing_layer = PIL.ImageDraw.Draw(rounded_mask)
  
  # Overwrite the RGBA values with A=255.
  # The 127 for RGB values was used merely for visualizing the mask
  
  # Draw two rectangles to fill interior with opaqueness
  drawing_layer.polygon([(radius,0),(width-radius,0),
                        (width-radius,height),(radius,height)],
                        fill=(127,0,127,255))
  drawing_layer.polygon([(0,radius),(width,radius),
                        (width,height-radius),(0,height-radius)],
                        fill=(127,0,127,255))

  #Draw four filled circles of opaqueness
  drawing_layer.ellipse((0,0, 2*radius, 2*radius), 
                        fill=(0,127,127,255)) #top left
  drawing_layer.ellipse((width-2*radius, 0, width,2*radius), 
                        fill=(0,127,127,255)) #top right
  drawing_layer.ellipse((0,height-2*radius,  2*radius,height), 
                        fill=(0,127,127,255)) #bottom left
  drawing_layer.ellipse((width-2*radius, height-2*radius, width, height), 
                        fill=(0,127,127,255)) #bottom right
                        
  # Uncomment the following line to show the mask
  # plt.imshow(rounded_mask)
  
  # Make the new image, starting with all transparent
  result = PIL.Image.new('RGBA', original_image.size, (0,0,0,0))
  result.paste(original_image, (0,0), mask=rounded_mask)
  return result
    
def get_images(directory=None):
  """ Returns PIL.Image objects for all the images in directory.
  
  If directory is not specified, uses current directory.
  Returns a 2-tuple containing 
  a list with a  PIL.Image object for each image file in root_directory, and
  a list with a string filename for each image file in root_directory
  """
  
  if directory == None:
    directory = os.getcwd() # Use working directory if unspecified

  image_list = [] # Initialize aggregaotrs
  file_list = []
  
  directory_list = os.listdir(directory) # Get list of files
  for entry in directory_list:
    absolute_filename = os.path.join(directory, entry)
    try:
      image = PIL.Image.open(absolute_filename)
      file_list += [entry]
      image_list += [image]
    except IOError:
      pass # do nothing with errors tying to open non-images
  return image_list, file_list

def round_corners_of_all_images(directory=None):
  """ Saves a modfied version of each image in directory.
  
  Uses current directory if no directory is specified. 
  Places images in subdirectory 'modified', creating it if it does not exist.
  New image files are of type PNG and have transparent rounded corners.
  """
  
  if directory == None:
    directory = os.getcwd() # Use working directory if unspecified
    directory+='/OriginalImages'   
  # Create a new directory 'modified'
  new_directory = os.path.join(directory, '../modified')
  try:
    os.mkdir(new_directory)
  except OSError:
    pass # if the directory already exists, proceed  
  
  # Load all the images
  image_list, file_list = get_images(directory)  

  # Go through the images and save modified versions
  for n in range(len(image_list)):
    # Parse the filename
    print(n)
    filename, filetype = os.path.splitext(file_list[n])
    
    # Round the corners with 5% percent of radius
    curr_image = image_list[n]
    new_image = round_corners_one_image(curr_image, 0.05) 
    
    # Save the altered image, suing PNG to retain transparency
    new_image_filename = os.path.join(new_directory, filename + '.png')
    new_image.save(new_image_filename)    

def tintImage(directory, color):
	"""
	param: directory
	type: String
	desc: Directory that contains the images to be tinted

	param: color
	type: int or Color
	desc: color to tint with

	Tints the images with a specified color in a specified directory
	"""
  
  # Load all the images
	image_list, file_list = get_images(directory)
	colorTuple = ()

	if type(color) == tuple:
		colorTuple = color
	elif type(color) == Color:
		# if the function is called with the Color enum, convert the color enum to an RGBA tuple
		colorTuple = hexToRGB(str(hex(text.color.value)))
		
	for n in range(len(image_list)):
		# Parse the filename
		print(n)
		filename, filetype = os.path.splitext(file_list[n])
		
		curr_image = image_list[n]
		curr_image = curr_image.convert("RGBA")
		tintImg = Image.new('RGBA', curr_image.size, colorTuple)
		tintedImage = ImageChops.multiply(curr_image, tintImg)

  	# Save the altered image, suing PNG to retain transparency
		new_image_filename = os.path.join("./modified", filename + '.png')
		tintedImage.save(new_image_filename)

# font enum stores an index into this array
fontList = ["Poppins-Regular.ttf", "Poppins-Italic.ttf", "Poppins-SemiBold.ttf", "Poppins-Bold.ttf", "Poppins-Light.ttf", "Poppins-Medium.ttf", "Poppins-Thin.ttf", "Poppins-SemiBoldItalic.ttf", "Poppins-BoldItalic.ttf", "Poppins-LightItalic.ttf", "Poppins-MediumItalic.ttf", "Poppins-ThinItalic.ttf"]

# images will be scaled down by a factor of this
# these are arbitrary I have no idea what I'm doing

# these are directly coincide with the ImageSize enum values
imageReductionFactor = [1, 0.05, 0.1, 0.3, 0.7, 2]

# if adding multiple texts, this is to make sure they dont overlap
yOffset = 0

targetX = 0
targetY = 0

# this text refers to an instance of the Text class
def __write__(img, text, position):
	"""
	This is an internal function.
	Its parameters are the same as addText.

	Write text to an image
	"""

	global fontList
	global yOffset
	global targetX
	global targetY

	draw = ImageDraw.Draw(img)

	targetFont = ImageFont.truetype("Fonts/" + fontList[text.style.value], text.size)

	# a tuple of RGBA values that will be used on the text
	colorTuple = ()

	if type(text.color) == tuple:
		# if the function is already called with a tuple, leave it
		colorTuple = text.color
	else:
		# if the function is called with the Color enum, convert the color enum to an RGBA tuple
		colorTuple = hexToRGB(str(hex(text.color.value)))
	
	# grab the dimensions of the image and the content
	imageWidth, imageHeight = img.size # size is an attribute, not a method for some reason. this lib is pretty inconsistent
	contentWidth, contentHeight = targetFont.getsize(text.content)

	# 30 is an arbitrarily chosen offset to place everything at
	# it would look really odd if text was placed directly at (0, 0)
	# so we give it some padding to make it look nice

	# support for custom positioning
	if type(position) == tuple:
		draw.text(position, text.content, colorTuple, font=targetFont)
	elif type(position) == Position:
		if position == Position.TOP_LEFT:
			targetX = 30
			targetY = 30 + yOffset

			draw.text((targetX, targetY), text.content, colorTuple, font=targetFont)

		elif position == Position.TOP_RIGHT:
			targetX = imageWidth - (contentWidth + 30)
			targetY = 30 + yOffset

			draw.text((targetX, targetY), text.content, colorTuple, font=targetFont)

		elif position == Position.BOTTOM_LEFT:
			targetX = 30
			targetY = imageHeight - contentHeight - 30 - yOffset

			draw.text((targetX, targetY), text.content, colorTuple, font=targetFont)

		elif position == Position.BOTTOM_RIGHT:
			targetX = imageWidth - (contentWidth + 30)
			targetY = imageHeight - contentHeight - 30 - yOffset

			draw.text((targetX, targetY), text.content, colorTuple, font=targetFont)

		elif position == Position.CENTER:
			# calculate the center coordinates of the image
			centerX = imageWidth / 2
			centerY = imageHeight / 2

			# we place the text at centerX - (titleWidth / 2) and centerY - (titleHeight / 2)
			targetX = centerX - (contentWidth / 2)
			targetY = centerY - (contentHeight / 2) + yOffset

			draw.text((targetX, targetY), text.content, colorTuple, font=targetFont)
		elif position == Position.TOP_CENTER:
			centerX = imageWidth / 2

			targetX = centerX - (contentWidth / 2)
			targetY = 30 + yOffset

			draw.text((targetX, targetY), text.content, colorTuple, font=targetFont)
		elif position == Position.BOTTOM_CENTER:
			centerX = imageWidth / 2
			
			targetX = centerX - (contentWidth / 2)
			targetY = imageHeight - contentHeight - 30 - yOffset

			draw.text((targetX, targetY), text.content, colorTuple, font=targetFont)

	# check if decoration for the content is enabled
	# decoration means underline
	# the underline color will be the same as the text
	# its thickness will be 1/10 the height of the text

	if text.decoration == Decoration.UNDERLINE:
		targetY += 5 # underline starts 20 pixels below the text

		if "y" in text.content or "g" in text.content:
			targetY -= contentHeight * 0.25

		draw.rectangle((targetX, targetY + contentHeight, targetX + contentWidth, targetY + contentHeight + (contentHeight * 0.1)), fill=colorTuple)

		targetY += contentHeight + (contentHeight * 0.1) # increment targetY by the same amount we calculated the thickness of the underline
	elif text.decoration == Decoration.BOX:
		# the box will just get an underline but on all 4 sides

		lineThickness = contentHeight * 0.1

		# 20 pixel padding and height is 1/10 contentHeight
		# draw the top line
		targetY -= 5 - lineThickness
		draw.rectangle((targetX, targetY, targetX + contentWidth, targetY + lineThickness), fill=colorTuple)

		targetY += 10 + contentHeight # undo what we did before

		# y and g go below the text base line, so move the bottom line up to look consistent
		if "y" in text.content or "g" in text.content:
			targetY -= contentHeight * 0.25

		# draw the bottom line
		draw.rectangle((targetX, targetY, targetX + contentWidth, targetY + lineThickness), fill=colorTuple)

		yOffset += lineThickness * 2

	# return the edited image object so that we can update yOffset in addText
	return img

# TODO: implement word wrapping
# this text refers to an instance of the Text class
def addText(path, text, position=Position.CENTER):
	"""
	param: path
	type: String
	desc: path to the image

	param: text
	type: Text or list
	desc: a Text object or list of Text objects

	param: position
	type: Position or Tuple(int, int)
	desc: The position of the title on the image

	Adds text or gorups of text to a given image
	"""

	global fontList
	global yOffset
	global targetX
	global targetY

	yOffset = 0
	targetX = 0
	targetY = 0

	# split the path with a delimeter
	# the filename is the last item in this list
	splitPath = str.split(path, "/")
	
	img = Image.open(path).convert("RGBA")

	if type(text) == Text:
		# we only have a single item to write, so call it once
		img = __write__(img, text, position)

	# we have a list of items to write, so loop over them and manipulate yOffset
	# so that that content of each item doesn't overlap
	elif type(text) == list:
		for item in text:
			img = __write__(img, item, position)
			
			targetFont = ImageFont.truetype("Fonts/" + fontList[item.style.value], item.size)
			contentWidth, contentHeight = targetFont.getsize(item.content)
			yOffset += contentHeight

	# we remove the file extension and substitute our own
	filename = str.split(splitPath[len(splitPath) - 1], ".")
	newPath = "./modified/" + filename[0] + ".png"
	img.save(newPath)

def addImage(path, maskPath, size, position=Position.CENTER):
	"""
	param: path
	type: String
	desc: path of the background image
	
	param: maskPath
	type: String
	desc: path of the foreground image
	
	param: size
	type: ImageSize, float or Tuple(int, int)
	desc: factor to reduce image by or the new dimensions of the image

	param: position
	type: Position or Tuple(int, int)
	desc: position of the foreground image on the backgorund image

	Composits an image onto another
	"""

	global targetX
	global targetY

	targetX = 0
	targetY = 0

	splitPath = str.split(path, "/")

	img = Image.open(path).convert("RGBA")
	mask = Image.open(maskPath).convert("RGBA")

	imageWidth, imageHeight = img.size
	maskWidth, maskHeight = mask.size

	sizeTuple = ()

	if type(size) == tuple:
		sizeTuple = size
	elif type(size) == float:
		sizeTuple = (int(maskWidth * size), int(maskHeight * size))
	elif type(size) == ImageSize:
		sizeTuple = (int(maskWidth * imageReductionFactor[size.value]), int(maskHeight * imageReductionFactor[size.value]))

	mask = mask.resize(sizeTuple, Image.ANTIALIAS)

	maskWidth, maskHeight = mask.size # update the values with the new size

	# support for custom positioning
	if type(position) == tuple:
		img.paste(mask, position)
	elif position == Position:
		if position == Position.TOP_LEFT:
			targetX = 30
			targetY = 30

			offset = (int(targetX), int(targetY))

			img.paste(mask, offset)
		elif position == Position.TOP_CENTER:
			targetX = (imageWidth / 2) - (maskWidth / 2)
			targetY = 30

			offset = (int(targetX), int(targetY))

			img.paste(mask, offset)
		elif position == Position.TOP_RIGHT:
			targetX = imageWidth - maskWidth - 30
			targetY = 30

			offset = (int(targetX), int(targetY))

			img.paste(mask, offset)
		elif position == Position.CENTER:
			targetX = (imageWidth / 2) - (maskWidth / 2)
			targetY = (imageHeight / 2) - (maskHeight / 2)

			offset = (int(targetX), int(targetY))

			img.paste(mask, offset)
		elif position == Position.BOTTOM_RIGHT:
			targetX = 30
			targetY = maskHeight + 30

			offset = (int(targetX), int(targetY))

			img.paste(mask, offset)
		elif position == Position.BOTTOM_CENTER:
			targetX = (imageWidth / 2) - (maskWidth / 2)
			targetY = maskHeight + 30

			offset = (int(targetX), int(targetY))

			img.paste(mask, offset)
		elif position == Position.BOTTOM_RIGHT:
			targetX = imageWidth - maskWidth - 30
			targetY = maskHeight + 30

			offset = (int(targetX), int(targetY))

			img.paste(mask, offset)

	filename = str.split(splitPath[len(splitPath) - 1], ".")
	newPath = "./modified/" + filename[0] + ".png"
	img.save(newPath)

"""
This is the code used to generate the final images.
It's really simple.
"""

round_corners_of_all_images(directory=None)
tintImage("./modified", (230, 190, 138, 225))

# we dont want the wwf logo to be tinted
round_corners_of_all_images(directory="./assets")

# create new text ob
title = Text("World Wildlife Fund", Font.BOLD, Color.LIGHTRED, 100, Decoration.BOX)
subtitle = Text("Only One Earth", Font.MEDIUM, Color.WHITE, 80, Decoration.NONE)
header = Text("https://wwf.org", Font.LIGHT, Color.WHITE, 50, Decoration.NONE)
footer = Text("Save the Planet", Font.LIGHT, Color.WHITE, 45, Decoration.NONE)

addText("./modified/mountain.png", [title, subtitle], Position.CENTER)
addText("./modified/mountain.png", header, Position.TOP_LEFT)
addText("./modified/mountain.png", footer, Position.BOTTOM_CENTER)

addImage("./modified/mountain.png", "./modified/wwf.png", 0.2, Position.TOP_RIGHT)