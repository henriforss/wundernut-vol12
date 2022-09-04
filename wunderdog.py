# Solution to Wunderdog wundernut-vol 12.
# https://github.com/wunderdogsw/wundernut-vol12

# Import Python Imaging Library (Pillow) and Numpy
from PIL import Image
import numpy as np
from pytesseract import pytesseract
import string

# Open image as Image class object.
img = Image.open("parchment.png")

# Check image properties. Size is 4000 x 842 pixels, color mode is RGB.
img_size = img.size
img_mode = img.mode
print("Image size:", img.size)
print("Image mode:", img.mode)

# Get image colors. Find out there are two colors in the image that are almost the same. One is RGB(252, 245, 229) and the other RGB(252, 245, 230).
e = img.getcolors()
print("Number of colors:", len(e))
print("Colors:", e)

# Convert image to Numpy array, and array to list.
img_array = np.asarray(img)
img_list = img_array.tolist()

# Create empty list for new image data.
temp_list = []

# Loop through every pixel in image. img_list is a list with lists for every row of pixels, which have lists for every pixel as RGB-colors. Change one color to black and the other to white to add contrast. Append changed pixels in array as tuples.
for row in img_list:
  for pixel in row:
    red = pixel[0]
    green = pixel[1]
    blue = pixel[2]

    if blue == 230:
      tp = (0, 0, 0)
      temp_list.append(tp)
    else:
      tp = (255, 255, 255)
      temp_list.append(tp)

# Create a new Image class object.
new_img = Image.new(img_mode, img_size)

# Put pixels in temp_list into new_img.
new_img.putdata(temp_list)

# Show new image. Adding contrast to original image reveals writing. The writing does not make sense, it is encoded. According to the instructions it is in English.
new_img.show()

# Save new image as new file.
new_img.save("parchment_revealed.png")

# Provide path to tesseract and saved image.
path_to_tesseract = "/usr/local/Cellar/tesseract/5.2.0/bin/tesseract"
path_to_image = "parchment_revealed.png"

# Point tesseract_cmd to tesseract executable.
pytesseract.tesseract_cmd = path_to_tesseract

# Open saved image as Image class object.
img2 = Image.open(path_to_image)

# Extract text with tesseract.
text = pytesseract.image_to_string(img2)

# Remove newlines.
text = text.replace("\n", "")

# Print text.
print("The text reads:", text)
print("Length of text:", len(text))

# Some googling around suggests the text is a Caesar cipher. Using 5 as shift decodes part of the text, but there are errors.
alphabet = 2 * string.ascii_uppercase
decoded_text = ""
shift = 5
for i in range(len(text)):
  letter = text[i]
  index = alphabet.find(letter)
  shift_index = index + shift
  decoded_letter = alphabet[shift_index]
  decoded_text += decoded_letter

print(decoded_text)

""" 
The decoded text:

THISISASECRETLISTOFSPELLSTHATIHATVEINTENTEDMYSELFLANGLNCKGLUESTHETONGUETOTHERNOFONFTHEMNUTHLETICNRPUSLIFTSTHETICPTIMINTONTHEAIRBYTHEIRANKLELIBERACNRPUSISACNOUNTERJINXFNRLETIPNRPUSMUFFLIATOFILLSITSTARGETSEARSWITHUNIDENTIFIABLEBUZZINGSECPTUMSEMPRAISFONRENEMIES

Divided into words:

THIS IS A SECRET LIST OF SPELLS THAT I HATVE INTENTED MYSELF LANGLNCK GLUES THE TONGUE TO THE RNOF ONF THE MNUTH LETICNRPUS LIFTS THE TICPTIM INTON THE AIR BY THEIR ANKLE LIBERACNRPUS IS ACNOUNTER JINX FNR LETIPNRPUS MUFFLIATO FILLS ITS TARGETS EARS WITH UNIDENTIFIABLE BUZZING SECPTUMSEMPRA IS FONR ENEMIES

With some manual spell checking:

This is a secret list of spells that I have invented myself. LANGLNCK (langlock?)glues the tongue to the roof of the mouth, LETICNRPUS (levicorpus?) lifts the victim into the air by their ankle, LIBERACNRPUS (liberacorpus?) is another jinx for LETIPNRPUS, MUFFLIATO fills its targets ears with unidentifiable buzzing, SECPTUMSEMPRA (septumsempra?) is for enemies.

"""
