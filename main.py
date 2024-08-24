from PIL import Image, ImageDraw, ImageFont
import os

# Directory containing font files
font_dir = "fonts"

# Map user input to font file names
font_files = {
    "1": "ShadowsIntoLight-Regular.ttf",
    "2": "Satisfy-Regular.ttf",
    "3": "Caveat-Regular.ttf",
    "4": "PatrickHand-Regular.ttf",
    "5": "ReenieBeanie-Regular.ttf",
    "6": "Sacramento-Regular.ttf",
    "7": "HomemadeApple-Regular.ttf",
    "8": "Akhilfont-Regular.ttf"  # Added new font option
}

# Define the text directly in the script
text_to_convert = """
Employee well-being and mental health have become critical components of organizational success and sustainability. As workplaces evolve, the importance of fostering a healthy and supportive environment for employees is increasingly recognized. This study aims to explore the best practices that organizations can implement to enhance employee well-being and mental health.
"""

# Display font options to the user
print("Choose a font:")
print("1. Shadows Into Light")
print("2. Satisfy")
print("3. Caveat")
print("4. Patrick Hand")
print("5. Reenie Beanie")
print("6. Sacramento")
print("7. Homemade Apple")
print("8. Akhil Font")  # New font option

# Get the user's choice
user_choice = input("Enter the number corresponding to your choice: ")

# Check if the user's choice is valid
if user_choice not in font_files:
    print("Invalid choice. Please select a number between 1 and 8.")
else:
    font_name = font_files[user_choice]
    font_path = os.path.join(font_dir, font_name)

    # Check if the font file exists
    if not os.path.exists(font_path):
        print(f"Font file {font_name} not found in the {font_dir} folder.")
    else:
        # Load the chosen font
        font = ImageFont.truetype(font_path, size=50)

        # Define maximum image width, height, and padding
        max_width = 1200
        max_height = 1800
        padding = 50

        # Create a function to wrap text
        def wrap_text(text, font, max_width):
            lines = []
            words = text.split()
            current_line = ''
            for word in words:
                test_line = current_line + ' ' + word if current_line else word
                width, _ = font.getbbox(test_line)[2:4]
                if width <= max_width - 2 * padding:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)
            return lines

        # Wrap the text into multiple lines
        lines = wrap_text(text_to_convert, font, max_width)

        # Calculate the number of lines that fit on a single page
        line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
        lines_per_page = (max_height - 2 * padding) // line_height

        # Initialize a list to store image pages
        images = []

        # Add pages and draw text on each page
        for i in range(0, len(lines), lines_per_page):
            # Create an image with a white background
            image = Image.new("RGB", (max_width, max_height), color="white")
            draw = ImageDraw.Draw(image)

            # Draw the border (4 cm margin)
            border_margin = 4 * 28.35  # 4 cm in pixels (assuming 96 DPI)
            draw.rectangle(
                [(border_margin, border_margin), 
                 (max_width - border_margin, max_height - border_margin)], 
                outline="black", width=2
            )

            # Add each line of text to the page
            y = padding + border_margin
            for line in lines[i:i + lines_per_page]:
                draw.text((padding + border_margin, y), line, fill=(0, 0, 0), font=font)
                y += line_height

            # Append the image to the list of pages
            images.append(image)

        # Check if images list is not empty and save the images as a multi-page PDF
        if images:
            output_filename = "user_text_handwritten.pdf"
            images[0].save(output_filename, save_all=True, append_images=images[1:], resolution=100.0)
            print(f"PDF saved as {output_filename}")
        else:
            print("No images to save.")
