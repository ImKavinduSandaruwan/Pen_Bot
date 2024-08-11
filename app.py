from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    data = request.json
    command = data.get('command')

    # Process the command
    if command.startswith("all"):
        response = list_all_commands()
    elif command.startswith("video"):
        url = command.split()[1] if len(command.split()) > 1 else None
        if url:
            response = download_video(url)
        else:
            response = "Please provide a valid YouTube URL."
    elif command.startswith("author"):
        response =  "Hey Kavindu Sandaruwan is my Author"
    else:
        response = "Unknown command. Type all to see available commands."

    return jsonify({"response": response})

def list_all_commands():
    return "Available commands: all, video <YouTube URL>, author"

def download_video(url):
    # Here you can implement the logic to download a YouTube video using something like `youtube-dl` or `yt-dlp`
    try:
        result = subprocess.run(
            ["yt-dlp", url],
            capture_output=True,
            text=True,
            cwd=os.path.join(os.getcwd(), "downloads")
        )
        if result.returncode == 0:
            return f"Video downloaded successfully! Check Download Folder"
        else:
            return f"Failed to download video"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    # Create a directory to store downloaded videos if it doesn't exist
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    app.run(debug=True)
