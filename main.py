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
    "7": "HomemadeApple-Regular.ttf"
}

# Display font options to the user
print("Choose a font:")
print("1. Shadows Into Light")
print("2. Satisfy")
print("3. Caveat")
print("4. Patrick Hand")
print("5. Reenie Beanie")
print("6. Sacramento")
print("7. Homemade Apple")

# Get the user's choice for font
user_choice = input("Enter the number corresponding to your choice: ")

# Check if the user's choice is valid
if user_choice not in font_files:
    print("Invalid choice. Please select a number between 1 and 7.")
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

        # Define border margin (4 cm in pixels)
        border_margin = int(4 * 28.35)  # 1 cm ≈ 28.35 pixels
        text_area_x1 = border_margin + padding
        text_area_y1 = border_margin + padding
        text_area_x2 = max_width - border_margin - padding
        text_area_y2 = max_height - border_margin - padding

        # Create a function to wrap text while preserving paragraphs
        def wrap_text(text, font, max_width):
            lines = []
            paragraphs = text.split('\n\n')
            for paragraph in paragraphs:
                words = paragraph.split()
                current_line = ''
                for word in words:
                    test_line = current_line + ' ' + word if current_line else word
                    width, _ = font.getbbox(test_line)[2:4]
                    if width <= max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word
                lines.append(current_line)
                lines.append('')  # Add a blank line between paragraphs
            return lines

        # Get the color choice from the user
        print("Choose a pen color:")
        print("1. Black")
        print("2. Blue")
        color_choice = input("Enter the number corresponding to your choice: ")

        # Set the pen color based on user choice with more realistic colors
        if color_choice == "1":
            pen_color = (30, 30, 30)  # Dark gray to simulate black ink
        elif color_choice == "2":
            pen_color = (30, 30, 150)  # Muted blue to simulate blue ink
        else:
            print("Invalid color choice. Defaulting to black.")
            pen_color = (30, 30, 30)

        # Get the text input from the user
        print("Enter the text to convert to PDF (End input with a single line containing 'END'):")
        text_lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            text_lines.append(line)
        text_to_convert = "\n".join(text_lines)

        # Wrap the text into multiple lines while preserving paragraphs
        lines = wrap_text(text_to_convert, font, text_area_x2 - text_area_x1)

        # Debugging: Print the wrapped lines
        print("Wrapped lines:", lines)

        # Calculate the number of lines that fit on a single page
        line_height = font.getbbox("A")[3] - font.getbbox("A")[1]
        lines_per_page = (text_area_y2 - text_area_y1) // line_height

        # Initialize a list to store image pages
        images = []

        # Add pages and draw text and border on each page
        for i in range(0, len(lines), lines_per_page):
            # Create an image with a white background
            image = Image.new("RGB", (max_width, max_height), color="white")
            draw = ImageDraw.Draw(image)

            # Draw the pencil-like border
            border_color = (150, 150, 150)  # Light gray to mimic pencil
            border_thickness = 5  # Border thickness
            draw.rectangle(
                [(border_margin, border_margin), (max_width - border_margin, max_height - border_margin)],
                outline=border_color,
                width=border_thickness
            )

            # Add each line of text to the page within the border
            y = text_area_y1
            for line in lines[i:i + lines_per_page]:
                if y + line_height > text_area_y2:
                    break
                draw.text((text_area_x1, y), line, fill=pen_color, font=font)
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
