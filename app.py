from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/api/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestvideo+bestaudio/best',
        'extract_flat': False,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            title = info.get('title')
            thumbnail = info.get('thumbnail')

            downloads = []
            for fmt in info['formats']:
                ext = fmt.get('ext')
                height = fmt.get('height')
                audio = fmt.get('acodec')
                video = fmt.get('vcodec')
                direct_url = fmt.get('url')

                if direct_url:
                    if audio != 'none' and video == 'none':
                        label = f"Audio - {ext.upper()}"
                    elif height:
                        label = f"{height}p - {ext.upper()}"
                    else:
                        label = ext.upper()

                    downloads.append({
                        'format': label,
                        'url': direct_url
                    })

            return jsonify({
                'title': title,
                'thumbnail': thumbnail,
                'downloads': downloads
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
