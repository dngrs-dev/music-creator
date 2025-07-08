from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import threading
import uuid
from music_generator import generate_music_main
import time

app = Flask(__name__, static_folder=".")
CORS(app)
CLEANUP_INTERVAL = 600
MUSIC_DIR = os.path.join(os.path.dirname(__file__), "music")


def cleanup_old_files():
    while True:
        now = time.time()
        for filename in os.listdir(MUSIC_DIR):
            if filename.startswith("music_output_") and (
                filename.endswith(".wav") or filename.endswith(".json")
            ):
                path = os.path.join(MUSIC_DIR, filename)
                try:
                    if (
                        os.path.isfile(path)
                        and now - os.path.getmtime(path) > CLEANUP_INTERVAL
                    ):
                        os.remove(path)
                except Exception as e:
                    app.logger.error(f"Cleanup error: {e}")
        time.sleep(CLEANUP_INTERVAL)


threading.Thread(target=cleanup_old_files, daemon=True).start()


@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        unique_id = str(uuid.uuid4())
        music_filename = f"music_output_{unique_id}.wav"
        info_filename = f"music_output_info_{unique_id}.json"
        music_path = os.path.join(MUSIC_DIR, music_filename)
        info_path = os.path.join(MUSIC_DIR, info_filename)

        generate_music_main(data, music_path, info_path)
        return jsonify(
            {
                "music_url": f"/download/music/{unique_id}",
                "info_url": f"/download/info/{unique_id}",
                "music_file_url": f"/music/{music_filename}",
                "info_file_url": f"/music/{info_filename}",
            }
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/download/music/<music_id>")
def download_music(music_id):
    path = f"music/music_output_{music_id}.wav"
    if not os.path.exists(path):
        return "File not found", 404
    return send_file(path, as_attachment=True, download_name=f"music_{music_id}.wav")


@app.route("/download/info/<info_id>")
def download_info(info_id):
    path = f"music/music_output_info_{info_id}.json"
    if not os.path.exists(path):
        return "File not found", 404
    return send_file(
        path, as_attachment=True, download_name=f"music_info_{info_id}.json"
    )


@app.route("/music/<path:filename>")
def serve_music(filename):
    return send_from_directory(MUSIC_DIR, filename)


@app.route("/")
def serve_index():
    return send_from_directory("site", "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory("site", filename)


@app.route("/api/cleanup", methods=["POST"])
def cleanup_files():
    data = request.get_json()
    files = data.get("files", [])
    deleted = []
    for file_url in files:
        if not file_url:
            continue
        filename = None
        if "/music/" in file_url:
            filename = file_url.split("/music/")[-1]
        elif "music/" in file_url:
            filename = file_url.split("music/")[-1]
        elif "/download/music/" in file_url:
            music_id = (
                file_url.split("/download/music/")[-1].split("?")[0].split("#")[0]
            )
            filename = f"music_output_{music_id}.wav"
        elif "/download/info/" in file_url:
            info_id = file_url.split("/download/info/")[-1].split("?")[0].split("#")[0]
            filename = f"music_output_info_{info_id}.json"
        if not filename:
            continue
        filename = filename.split("?")[0].split("#")[0]
        abs_path = os.path.abspath(os.path.join(MUSIC_DIR, filename))
        if abs_path.startswith(os.path.abspath(MUSIC_DIR)) and os.path.exists(abs_path):
            try:
                os.remove(abs_path)
                deleted.append(filename)
            except Exception as e:
                app.logger.error(f"Cleanup error: {e}")
    return jsonify({"deleted": deleted})


if __name__ == "__main__":
    app.run(debug=True)
