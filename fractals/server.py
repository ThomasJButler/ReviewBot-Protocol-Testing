"""A small HTTP wrapper around the Mandelbrot renderer."""

import io
import json
import os

from flask import Flask, request, send_file

from fractals.mandelbrot import render

app = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERS_DIR = os.path.join(PROJECT_ROOT, "renders")
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")


def parse_float(name, default):
    """Read a float query parameter, falling back to a default."""
    raw = request.args.get(name)
    if raw is None:
        return default
    return float(raw)


@app.route("/render")
def render_endpoint():
    """Render an image from the query parameters and return it as a PNG."""
    width = int(request.args.get("width", 400))
    height = int(request.args.get("height", 300))
    max_iter = int(request.args.get("max_iter", 200))
    centre_x = parse_float("cx", -0.5)
    centre_y = parse_float("cy", 0.0)
    zoom = parse_float("zoom", 1.0)

    image = render(width, height, max_iter, centre_x, centre_y, zoom)

    save_name = request.args.get("save")
    if save_name:
        os.makedirs(RENDERS_DIR, exist_ok=True)
        image.save(os.path.join(RENDERS_DIR, save_name), format="PNG")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png")


@app.route("/")
def gallery_page():
    """Serve the gallery page."""
    return send_file(os.path.join(STATIC_DIR, "gallery.html"))


@app.route("/static/gallery.js")
def gallery_script():
    """Serve the script used by the gallery page."""
    return send_file(os.path.join(STATIC_DIR, "gallery.js"))


@app.route("/api/renders")
def renders_index():
    """Return the list of saved renders described by renders/index.json."""
    index_path = os.path.join(RENDERS_DIR, "index.json")
    if not os.path.exists(index_path):
        return []
    with open(index_path, "r", encoding="utf-8") as handle:
        entries = json.load(handle)
    return entries


@app.route("/renders/<name>")
def saved_render(name):
    """Return one image that was saved by an earlier request."""
    return send_file(os.path.join(RENDERS_DIR, name))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
