# Meme Generator with Gemini AI

A web-based meme generator that uses Google's Gemini AI to create dynamic text for memes based on user prompts.

## Project Structure

```
meme generator/
├── memegenerator/    # Source images for m.py 
├── PO/               # Source images for memes
├── output/           # Generated memes output
├── c.py              # Core meme generation logic
├── m.py              # GUI tool for marking text areas
├── server.py         # Flask web server
├── index2.html       # Web interface
├── image_data.json   # Text box coordinates data
├── requirements.txt  # Project dependencies
└── log.txt           # AI response logs

## Setup Instructions

1. Install Dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API Key:
   - Get an API key from Google Gemini AI
   - Place it in server.py or set as environment variable

3. Prepare Images:
   - Place source images in memegenerator/ directory
   - Use m.py to mark text areas on images
   - images might save in some new folder ensure to copy them in PO/ folder and the json file will be generated in that same folder, ensure to copy paste it in the main folder. like in the above structure
   - Coordinates will be saved in image_data.json

## File Descriptions

### c.py
- Core meme generation functionality
- Handles image processing and text placement
- Integrates with Gemini AI API
- Manages font sizing and text wrapping

### m.py
- GUI tool for marking text areas on images
- Creates and updates image_data.json
- Allows visual selection of text box areas
- Saves coordinates for text placement

### server.py
- Flask web server implementation
- Serves images and handles API requests
- Manages meme generation workflow
- Integrates with web interface

### index2.html
- Web interface for meme generation
- Displays image grid (5 columns)
- Handles user input and meme preview
- Provides download functionality

## Usage

1. Start the Web Server:
```bash
python server.py
```

2. Access the Interface:
- Open browser at http://localhost:5000
- Browse available meme templates
- Click an image to create meme
- Enter prompt and generate

3. Mark New Templates (Optional):
```bash
python m.py
```
- Open image and draw text boxes
- Save coordinates for new templates

## Features

- Web-based interface
- AI-powered text generation
- Dynamic font sizing
- Text outline for readability
- Response logging
- Multiple template support
- Download generated memes

## Dependencies

- Flask: Web framework
- Pillow: Image processing
- Requests: API communication
- TkInter: GUI for template marking
- Google Gemini AI API

## Logging

All AI responses are logged in log.txt with:
- Timestamp
- Image name
- User prompt
- AI response
- Clear separation between entries

## Error Handling

- Image validation
- API response verification
- JSON data validation
- File path checking
- User input validation

## Contributing

1. Use m.py to add new templates
2. Update image_data.json with new coordinates
3. Test text fitting in all boxes
4. Verify API responses

## Notes

- Keep API key secure
- Maintain proper folder structure
- Regular backup of image_data.json
- Monitor log.txt for AI responses
