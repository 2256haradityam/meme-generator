from flask import Flask, send_from_directory, render_template, request, jsonify
import os
from pathlib import Path
import json
from c import generate_meme  # Import your existing meme generation code

app = Flask(__name__, template_folder='.')
IMAGES_DIR = r"C:\Users\harad\Desktop\meme generator\PO"
OUTPUT_DIR = r"C:\Users\harad\Desktop\meme generator\output"

@app.route('/')
def index():
    # Get all images from PO directory
    images = []
    for ext in ['.png', '.jpg', '.jpeg']:
        images.extend([f.name for f in Path(IMAGES_DIR).glob(f'*{ext}')])
    return render_template('index2.html', images=images)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory(OUTPUT_DIR, filename)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    image_name = data.get('image')
    prompt = data.get('prompt')
    
    if not image_name or not prompt:
        return jsonify({'error': 'Missing image or prompt'}), 400
    
    try:
        # Load boxes data
        with open('image_data.json', 'r') as f:
            boxes_data = json.load(f)
        
        # Generate meme
        image_path = os.path.join(IMAGES_DIR, image_name)
        api_key = "GEMINI_API_KEY"  # Replace with your actual API key
        
        output_path = generate_meme(image_path, prompt, api_key, boxes_data)
        
        if output_path:
            return jsonify({
                'success': True,
                'output': os.path.basename(output_path)
            })
        else:
            return jsonify({'error': 'Failed to generate meme'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)