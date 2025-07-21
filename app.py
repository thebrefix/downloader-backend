from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Downloader API by Vishal is running!"

@app.route("/api/fetch", methods=["POST"])
def fetch():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required."}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'no_warnings': True,
            'forcejson': True,
            'extract_flat': False,
            'cookiefile': 'cookies.txt',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get("title", "Unknown Title")
        thumbnail = info.get("thumbnail")
        formats = info.get("formats", [])

        downloads = []
        seen_labels = set()

        for fmt in formats:
            file_url = fmt.get("url")
            ext = fmt.get("ext")
            resolution = fmt.get("format_note") or fmt.get("height")
            audio_only = fmt.get("vcodec") == "none"

            if not file_url or ext not in ['mp4', 'm4a', 'mp3', 'webm']:
                continue

            if audio_only:
                label = "MP3" if ext == "mp3" else "M4A"
            else:
                label = str(resolution).upper()

            if label not in seen_labels:
                seen_labels.add(label)
                downloads.append({
                    "label": label,
                    "url": file_url
                })

        return jsonify({
            "title": title,
            "thumbnail": thumbnail,
            "downloads": downloads
        })

    except Exception as e:
        return jsonify({"error": f"Failed to extract info: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
