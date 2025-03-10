import requests
import json
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import textwrap
import datetime
from pathlib import Path
from tkinter import *
from tkinter import filedialog
import tkinter.simpledialog as simpledialog

def select_image():
    """Open file dialog to select an image"""
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select Meme Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")],
        initialdir=r"C:\Users\harad\Desktop\meme generator\PO"
    )
    return file_path if file_path else None

def get_user_prompt():
    """Get prompt from user using dialog"""
    root = Tk()
    root.withdraw()  # Hide the main window
    prompt = simpledialog.askstring(
        "Meme Text", 
        "Enter your meme prompt:",
        initialvalue="Trying to stay positive while everything is falling apart."
    )
    return prompt if prompt else None

def generate_meme(image_path, user_prompt, api_key, boxes_data):
    try:
        # Create output directory if it doesn't exist
        output_dir = Path(r"C:\Users\harad\Desktop\meme generator\output")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Validate and open image
        if not os.path.exists(image_path):
            print(f"Error: Image not found at {image_path}")
            return None

        from PIL import Image as PILImage
        img = PILImage.open(image_path).convert("RGBA")
        width, height = img.size

        # Get image filename for JSON lookup
        image_key = str(Path(image_path)).replace('\\', '/')
        if image_key not in boxes_data:
            print(f"Error: No box data found for image: {image_path}")
            return None

        text_boxes = boxes_data[image_key]["boxes"]

        # Construct a more specific prompt for Gemini
        prompt = f"""
        You are a creative meme text generator. Generate witty and engaging text for a meme with {len(text_boxes)} text boxes.

        Context: The user wants a meme about: '{user_prompt}'

        Requirements:
        1. Be creative and humorous while matching the user's intention
        2. Generate plain text only (no special characters or markdown)
        3. Each text box has specific dimensions (in pixels):
        {', '.join([f'Box {i}: width={box["coords"][2]-box["coords"][0]}, height={box["coords"][3]-box["coords"][1]}' for i, box in enumerate(text_boxes)])}
        4. Keep each text segment concise to fit its box
        5. Ensure text flows naturally between boxes if multiple boxes exist
        6. Consider classic meme formats and humor styles

        Return ONLY a JSON object with numbered boxes like this:
        {{"0": "first box text", "1": "second box text"}}

        Make it memorable and funny!
        """

        response = call_gemini_api(prompt, api_key)
        if response is None:
            return None
        log_path = Path(r"C:\Users\harad\Desktop\meme generator\log.txt")
        with open(log_path, "a", encoding='utf-8') as log_file:
            log_file.write(f"\n\nTimestamp: {datetime.datetime.now()}\n")
            log_file.write(f"Image: {Path(image_path).name}\n")
            log_file.write(f"User Prompt: {user_prompt}\n")
            log_file.write(f"Gemini Response: {response}\n")
            log_file.write("-" * 80)

        try:
            text_data = json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"API Response: {response}")
            return None

        draw = ImageDraw.Draw(img)
        font_size = calculate_font_size(img, text_boxes)
        font = ImageFont.truetype("arialbd.ttf", font_size)

        # Draw text in boxes
        for box_index, box in enumerate(text_boxes):
            if str(box_index) in text_data:
                text = text_data[str(box_index)].strip()
                # Calculate max characters per line based on box width
                box_width = box["coords"][2] - box["coords"][0]
                chars_per_line = int(box_width / (font_size * 0.6))  # Approximate character width
                wrapped_text = textwrap.fill(text, width=chars_per_line)

                x1, y1, x2, y2 = box["coords"]
                bbox = draw.textbbox((0, 0), wrapped_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = (x1 + x2 - text_width) / 2
                text_y = (y1 + y2 - text_height) / 2
                
                # Draw text with outline for better visibility
                outline_color = (0, 0, 0, 255)
                for adj in range(-2, 3):
                    for adj2 in range(-2, 3):
                        draw.text((text_x + adj, text_y + adj2), wrapped_text, font=font, fill=outline_color)
                draw.text((text_x, text_y), wrapped_text, font=font, fill=(255, 255, 255, 255))

        # Save with original filename in output directory
        output_filename = f"meme_{Path(image_path).stem}.png"
        output_path = output_dir / output_filename
        img.save(output_path)
        return str(output_path)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def call_gemini_api(prompt, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        full_response = response.json()
        raw_text = full_response['candidates'][0]['content']['parts'][0]['text']
        # remove the ```json and ``` from the response.
        raw_text = raw_text.replace('```json', '')
        raw_text = raw_text.replace('```', '')
        raw_text = raw_text.strip() #remove extra spaces.
        return raw_text

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return None
    except KeyError:
        print("Error: Unexpected API response format.")
        return None
def calculate_font_size(img, text_boxes):
    """Calculate optimal font size based on box dimensions and text length"""
    min_font_size = float('inf')
    
    for box in text_boxes:
        coords = box["coords"]
        box_width = coords[2] - coords[0]
        box_height = coords[3] - coords[1]
        
        # Calculate height-based font size (40% of box height)
        height_based_size = int(box_height * 0.7)
        
        # Calculate width-based font size (considering average character width)
        # Assuming average character takes 60% of font size width
        avg_char_count = 15  # Average characters per line
        width_based_size = int((box_width * 0.95) / (avg_char_count * 0.45))
        
        # Take the smaller of the two sizes to ensure text fits both dimensions
        optimal_size = min(height_based_size, width_based_size)
        
        # Keep track of smallest required font size across all boxes
        min_font_size = min(min_font_size, optimal_size)
    
    # Add a small safety margin (90% of calculated size)
    return int(min_font_size * 0.95)
def list_image_files(directory):
    """List all PNG and JPG files in the specified directory"""
    image_extensions = ('.png', '.jpg', '.jpeg')
    return [f for f in Path(directory).glob('*') if f.suffix.lower() in image_extensions]

# Update the main execution code
if __name__ == "__main__":
    try:
        with open("image_data.json", "r") as f:
            boxes_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        exit(1)

    api_key = "GEMINI_API_KEY"  # Replace with your API key

    # Get image and prompt from user
    image_path = select_image()
    if not image_path:
        print("No image selected. Exiting...")
        exit(1)

    user_prompt = get_user_prompt()
    if not user_prompt:
        print("No prompt provided. Exiting...")
        exit(1)

    print(f"Processing {Path(image_path).name}...")
    generated_meme_path = generate_meme(image_path, user_prompt, api_key, boxes_data)