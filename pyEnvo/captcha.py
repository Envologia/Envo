# Envo Userbot - Captcha Generation
# Created by @envologia

import random
import tempfile
import os
from PIL import Image, ImageDraw, ImageFont

def generate_captcha():
    """Generates a captcha image with a simple math problem."""
    # Create a simple math problem
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*'])

    if operator == '+':
        question = f"{num1} + {num2}"
        answer = str(num1 + num2)
    elif operator == '-':
        # Ensure the result is not negative
        if num1 < num2:
            num1, num2 = num2, num1
        question = f"{num1} - {num2}"
        answer = str(num1 - num2)
    else: # operator == '*'
        question = f"{num1} * {num2}"
        answer = str(num1 * num2)

    # Create an image
    width, height = 200, 100
    image = Image.new('RGB', (width, height), color = 'white')
    draw = ImageDraw.Draw(image)

    # Use a font
    try:
        font = ImageFont.truetype("resources/DejaVuSans.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Draw the text
    draw.text((10, 10), question, fill='black', font=font)

    # Add some noise
    for _ in range(1500):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        draw.point((x, y), fill='black')

    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        image.save(temp_file.name)
        return temp_file.name, answer
