from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
import os
import tempfile
import time
from nmap_parser import extract_targets
from seleniumrunner import run_selenium_on_targets
from excel_writer import write_results_to_excel

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)

# Global progress state
progress = {
    "total": 0,
    "completed": 0,
    "start_time": None
}

@app.route("/scan", methods=["POST"])
def scan():
    file = request.files.get("file")
    if not file or not file.filename.endswith(".xml"):
        return jsonify({"error": "Invalid or missing XML file"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
        file.save(temp_file.name)
        targets = extract_targets(temp_file.name)

    all_targets = []

    for target in targets:
        ip = target.get("ip")
        ports = target.get("port")
        if not ip or not ports:
            continue

        port_list = ports.split(",")
        for port in port_list:
            port = port.strip()
            if not port.isdigit():
                continue
            for scheme in ["http", "https"]:
                url = f"{scheme}://{ip}:{port}"
                all_targets.append({
                    "url": url,
                    "ports": port
                })

    # Set progress
    progress["total"] = len(all_targets)
    progress["completed"] = 0
    progress["start_time"] = time.time()

    # Run with progress update
    def update_progress():
        progress["completed"] += 1

    results = run_selenium_on_targets(all_targets, progress_callback=update_progress)
    write_results_to_excel(results, "results.xlsx")

    preview = []
    for item in results:
        preview.append({
            "url": item["url"],
            "ports": item["ports"],
            "screenshot": f"/screenshots/{os.path.basename(item['screenshot'])}" if item["screenshot"] else None
        })

    return jsonify(preview)

@app.route("/progress")
def get_progress():
    completed = progress.get("completed", 0)
    total = progress.get("total", 1)
    start = progress.get("start_time")

    if completed and start:
        elapsed = time.time() - start
        avg_time = elapsed / completed
        remaining = avg_time * (total - completed)
    else:
        remaining = 0

    return jsonify({
        "completed": completed,
        "total": total,
        "remaining_seconds": int(remaining)
    })

@app.route("/download/results.xlsx")
def download_excel():
    return send_file("results.xlsx", as_attachment=True)

@app.route("/screenshots/<path:filename>")
def serve_screenshot(filename):
    return send_file(os.path.join("screenshots", filename), mimetype="image/png")

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    root_dir = os.path.join(os.path.dirname(__file__), "../frontend/build")
    if path != "" and os.path.exists(os.path.join(root_dir, path)):
        return send_from_directory(root_dir, path)
    else:
        return send_from_directory(root_dir, "index.html")

if __name__ == "__main__":
    os.makedirs("screenshots", exist_ok=True)
    app.run(debug=True)
