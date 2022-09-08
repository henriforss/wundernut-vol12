# Solution to Wunderdog wundernut-vol 12.
# https://github.com/wunderdogsw/wundernut-vol12

# Import Python Imaging Library (Pillow) and Numpy
from PIL import Image
import numpy as np
from pytesseract import pytesseract
import string

def reveal_image(image_in, image_out):

  # Open image as Image class object.
  img = Image.open(image_in)

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
  # new_img.show() # Comment out if you don't want to show it

  # Save new image as new file.
  new_img.save(image_out)

def read_image(image_in):

  # Provide path to tesseract and saved image.
  path_to_tesseract = "/usr/local/Cellar/tesseract/5.2.0/bin/tesseract"
  path_to_image = image_in

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

  return text

def decipher_text(text_in):

  # Some googling around suggests the text is a Caesar cipher. Using 5 as shift decodes part of the text, but there are errors.
  alphabet = string.ascii_uppercase
  deciphered_text = ""
  shift = 5
  for i in range(len(text_in)):
    letter = text_in[i]
    index = alphabet.find(letter)
    shift_index = index + shift

    if shift_index > 25:
      shift_index = shift_index % 26

    decoded_letter = alphabet[shift_index]
    deciphered_text += decoded_letter

  print(deciphered_text)

  return deciphered_text

def main():
  reveal_image("parchment.png", "parchment_revealed.png")
  text = read_image("parchment_revealed.png")
  decipher_text(text)

# main()

"""

Running the program returns a decoded text that looks like this:

THISISASECRETLISTOFSPELLSTHATIHATVEINTENTEDMYSELFLANGLNCKGLUESTHETONGUETOTHERNOFONFTHEMNUTHLETICNRPUSLIFTSTHETICPTIMINTONTHEAIRBYTHEIRANKLELIBERACNRPUSISACNOUNTERJINXFNRLETIPNRPUSMUFFLIATOFILLSITSTARGETSEARSWITHUNIDENTIFIABLEBUZZINGSECPTUMSEMPRAISFONRENEMIES

When you divide the text into words it looks like this:

THIS IS A SECRET LIST OF SPELLS THAT I HATVE INTENTED MYSELF LANGLNCK GLUES THE TONGUE TO THE RNOF ONF THE MNUTH LETICNRPUS LIFTS THE TICPTIM INTON THE AIR BY THEIR ANKLE LIBERACNRPUS IS ACNOUNTER JINX FNR LETIPNRPUS MUFFLIATO FILLS ITS TARGETS EARS WITH UNIDENTIFIABLE BUZZING SECPTUMSEMPRA IS FONR ENEMIES

Looking up spell names on the internet gives this:

LANGLNCK / Langlock
LETICNRPUS / Levicorpus
LIBERACNRPUS / Liberacorpus
LETIPNRPUS / Levicorpus
Muffliato
SECPTUMSEMPRA / Sectumsempra

All of the spells listed are invented by Severus Snape.

Applying some manual spellchecking gives this:

This is a secret list of spells that I have invented myself. Langlock glues the tongue to the roof of the mouth, Levicorpus lifts the victim into the air by their ankle, Liberacorpus is a counter jinx for Levicorpus, Muffliato fills its targets ears with unidentifiable buzzing, Sectumsempra is for enemies.

Obviously there is something more in this cipher. Here is a list of the words that are misspellt and which letter the spelling concerns:

HATVE: T
INTENTED: T
LANGLNCK: N
RNOF: N
ONF: N
MNUTH: N
LETICNRPUS: T, N
TICPTIM: T, P
INTON: N
LIBERACNRPUS: N
CNOUNTER: N
FNR: N
LETIPNRPUS: T, P, N
SECPTUMSEMPRA: P, 
FONR: N

The letters that should not be there are:

T, T, N, N, N, N, T, N, T, P, N, N, N, N, T, P, N, P, N

Some are extra letters:

T, N, P, N, N, P, N

Others are misspellt letters:

T, N, N, N, T, N, T, N, N, P, N

Let's see if we can find something there!

"""

def analyze_extra_letters(extra_letters):

  # Do some string manipulation on the extra letters.
  letters = extra_letters
  letters = letters.split(",")
  letters = [letter.strip() for letter in letters]
  letters = "".join(letters)
  print("The letters:", letters)
  print("Number of letters;", len(letters))

  # Try putting the words into a dictionary.
  letters_dict = {}
  for letter in range(len(letters)):
    letter = letters[letter]

    if letter in letters_dict.keys():
      letters_dict[letter] += 1
      continue

    letters_dict[letter] = 1

  # Print the dictionary.
  print(letters_dict)

analyze_extra_letters("T, T, N, N, N, N, T, N, T, P, N, N, N, N, T, P, N, P, N")

""" 

The extra letters are:

T, N, P

They show up like this:

{'T': 5, 'N': 11, 'P': 3}

The frequency 3, 5, 11 are all prime numbers.

To be continued ...

"""