"""A small HTTP wrapper around the Mandelbrot renderer."""

import io
import os
import pickle

from flask import Flask, request, send_file

from fractals import cache
from fractals.mandelbrot import render

app = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERS_DIR = os.path.join(PROJECT_ROOT, "renders")


def parse_float(name, default):
    """Read a float query parameter, falling back to a default."""
    raw = request.args.get(name)
    if raw is None:
        return default
    return float(raw)


def validate_dimensions(width, height):
    """Return True when the requested image size is sensible."""
    if width < 1 or height < 1:
        return False
    if width > 2000 or height > 2000:
        return False
    return True


@app.route("/render")
def render_endpoint():
    """Render an image from the query parameters and return it as a PNG."""
    width = int(request.args.get("width", 400))
    height = int(request.args.get("height", 300))
    max_iter = int(request.args.get("max_iter", 200))
    centre_x = parse_float("cx", -0.5)
    centre_y = parse_float("cy", 0.0)
    zoom = parse_float("zoom", 1.0)

    if not validate_dimensions(width, height):
        return "that image size is out of range", 400

    params = {
        "width": width,
        "height": height,
        "max_iter": max_iter,
        "cx": centre_x,
        "cy": centre_y,
        "zoom": zoom,
    }
    key = cache.cache_key(params)
    cached_png = cache.load(key)
    if cached_png is not None:
        return send_file(io.BytesIO(cached_png), mimetype="image/png")

    image = render(width, height, max_iter, centre_x, centre_y, zoom)

    save_name = request.args.get("save")
    if save_name:
        os.makedirs(RENDERS_DIR, exist_ok=True)
        image.save(os.path.join(RENDERS_DIR, save_name), format="PNG")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    png_bytes = buffer.getvalue()
    cache.store(key, params, png_bytes)

    return send_file(io.BytesIO(png_bytes), mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
