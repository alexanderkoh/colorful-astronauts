import numpy as np
import random
import cv2
import PIL.ImageFont as ImageFont
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import hashlib

def generate_image(string):
	# Load the template image
	template = cv2.imread("template.png")

	# Encode the string to HEX
	hex_code = string.encode().hex()

	# Generate a unique identifier based on the HEX code
	identifier = int(hashlib.sha256(hex_code.encode()).hexdigest(), 16) % 1000

	# Create a copy of the template image
	image = template.copy()

	# Change the colors of the image based on the identifier
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
			image[i][j] = (image[i][j][0], (image[i][j][1] + identifier) % 255, (image[i][j][2] + 2 * identifier) % 255)

	# Prompt the user to choose a tier
	print("What is the user's tier?")
	print("1. Captain")
	print("2. Navigator")
	print("3. Pathfinder")
	tier = int(input("Enter your choice (1-3): "))

	# Load the "option_3.png" image
	frame = cv2.imread(f"option_{tier}.png")

	# Resize the generated image to 325x325
	image = cv2.resize(image, (325, 325), interpolation=cv2.INTER_AREA)

	# Calculate the position to place the generated image in the middle of the frame
	start_x = int((frame.shape[0] - image.shape[0]) / 2)
	start_y = int((frame.shape[1] - image.shape[1]) / 2)

	# Superimpose the generated image on top of the frame
	frame[start_x:start_x + image.shape[0], start_y:start_y + image.shape[1]] = image

	# Convert the image to PIL Image format
	frame = Image.fromarray(frame)

	# Load the Roboto Mono font
	font = ImageFont.truetype("RobotoMono-Regular.ttf", 36)

	# Create a PIL ImageDraw object
	draw = ImageDraw.Draw(frame)

	# Get the width and height of the input string
	text_width, text_height = draw.textsize(string, font=font)

	# Calculate the position to place the string in the bottom center of the image
	text_x = int((frame.width - text_width) / 2)
	text_y = int(frame.height - text_height - 20)

	# Write the input string into the bottom center of the image
	draw.text((text_x, text_y), string, font=font, fill=(0, 0, 0, 255))

	# Save the final image
	frame.save("astronaut_{}.png".format(hex_code))


# Prompt the user to input a string
string = input("Enter your username: ")

# Generate the image
generate_image(string)
