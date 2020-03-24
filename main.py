
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

import matplotlib.pyplot as plt 
import os.path  
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont 
from PIL import ImageChops
from common import *
import struct

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

def tintImage(directory, tint_color):
  
  # Load all the images
  image_list, file_list = get_images(directory)  

  for n in range(len(image_list)):
    # Parse the filename
    print(n)
    filename, filetype = os.path.splitext(file_list[n])
    
    curr_image = image_list[n]
    curr_image = curr_image.convert("RGBA")
    tintImg = Image.new('RGBA', curr_image.size, tint_color)
    tintedImage = ImageChops.multiply(curr_image, tintImg)

  	# Save the altered image, suing PNG to retain transparency
    new_image_filename = os.path.join("./modified", filename + '.png')
    tintedImage.save(new_image_filename)

# font enum stores an index into this array
fontList = ["Poppins-Regular.ttf", "Poppins-Italic.ttf", "Poppins-SemiBold.ttf", "Poppins-Bold.ttf", "Poppins-Light.ttf", "Poppins-Medium.ttf", "Poppins-Thin.ttf", "Poppins-SemiBoldItalic.ttf", "Poppins-BoldItalic.ttf", "Poppins-LightItalic.ttf", "Poppins-MediumItalic.ttf", "Poppins-ThinItalic.ttf"]

# TODO: implement title positioning
# TODO: implement word wrapping
def addTitle(path, targetPath, text, style=Font.REGULAR, color=Color.BLACK, position=Position.CENTER, size=120):
	global fontList

	"""
	param: path
	type: String
	desc: path to the image

	param: text
	type: String
	desc: title text

	param: style
	type: Font
	desc: specifies the font style. refer to Font class

	param: color
	type: Color or tuple
	desc: color to use for the title

	param: position
	type: Position
	desc: The position of the title on the image

	param: size
	type: int
	desc: text size for the title

	Adds a title with the given text to the specified images
	"""

	# create a new image object with the given path
	img = Image.open(path).convert('RGBA')
	draw = ImageDraw.Draw(img)

	# create a new ImageFont type and load the specified ttf font
	targetFont = ImageFont.truetype("Fonts/" + fontList[style.value], size)

	colorTuple = ()

	if type(color) == tuple:
		colorTuple = color
	else:
		colorTuple = hexToRGB(str(hex(color.value))) # FIX THIS

	# create an rgb tuple out of the derived hex value from the color
	#colorTuple = hexToRGB(str(hex(color.value)))

	# for now, we draw the title on the center of the image
	# until positioning is implemented
	
	# grab the dimensions of the image and the title
	imageWidth, imageHeight = img.size # size is an attribute, not a method for some reason. this lib is pretty inconsistent
	titleWidth, titleHeight = targetFont.getsize(text)

	if position == Position.TOP_LEFT:
		targetX = 30
		targetY = 30

		draw.text((targetX, targetY), text, colorTuple, font=targetFont)

	elif position == Position.TOP_RIGHT:
		targetX = imageWidth - (titleWidth + 30)
		targetY = 30

		draw.text((targetX, targetY), text, colorTuple, font=targetFont)

	elif position == Position.BOTTOM_LEFT:
		targetX = 30
		targetY = imageHeight - (titleHeight + 30)

		draw.text((targetX, targetY), text, colorTuple, font=targetFont)

	elif position == Position.BOTTOM_RIGHT:
		targetX = imageWidth - (titleWidth + 30)
		targetY = imageHeight - (titleHeight + 30)

		draw.text((targetX, targetY), text, colorTuple, font=targetFont)

	elif position == Position.CENTER:
		# calculate the center coordinates of the image
		centerX = imageWidth / 2
		centerY = imageHeight / 2

		# we place the text at centerX - (titleWidth / 2) and centerY - (titleHeight / 2)
		targetX = centerX - (titleWidth / 2)
		targetY = centerY - (titleHeight / 2)

		draw.text((targetX, targetY), text, colorTuple, font=targetFont)

	img.save(targetPath)

round_corners_of_all_images(directory=None)
tintImage("./modified", (230, 190, 138, 225))
addTitle("./modified/lighthouse.png", "./modified/lighthouse.png", "TITLE", style=Font.BOLD, color=(221, 221, 221, 255), position=Position.TOP_LEFT)