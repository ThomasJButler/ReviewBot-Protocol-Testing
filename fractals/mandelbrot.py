"""Escape time rendering of the Mandelbrot set.

The maths here is deliberately plain Python. It is slow for large images,
which is fine for the sizes this project renders.
"""

from PIL import Image


def escape_iterations(real, imaginary, max_iter):
    """Count how many steps a point survives before it escapes the set.

    Returns max_iter when the point never escapes within the budget.
    """
    zr = 0.0
    zi = 0.0
    for step in range(max_iter):
        zr_squared = zr * zr
        zi_squared = zi * zi
        if zr_squared + zi_squared > 4.0:
            return step
        zi = 2.0 * zr * zi + imaginary
        zr = zr_squared - zi_squared + real
    return max_iter


def palette_colour(iterations, max_iter):
    """Turn an iteration count into an RGB tuple.

    Points inside the set are black, points that escape early are blue and
    points that take a long time to escape run through red.
    """
    if iterations >= max_iter:
        return (0, 0, 0)
    fraction = iterations / float(max_iter)
    red = int(255 * fraction)
    green = int(255 * (fraction ** 0.5))
    blue = int(255 * (1.0 - fraction))
    return (red, green, blue)


def render(width, height, max_iter=200, centre_x=-0.5, centre_y=0.0, zoom=1.0):
    """Render the set into a new Pillow image and return it."""
    image = Image.new("RGB", (width, height))
    pixels = image.load()

    span_x = 3.0 / zoom
    span_y = span_x * height / float(width)
    left = centre_x - span_x / 2.0
    top = centre_y - span_y / 2.0

    for row in range(height):
        imaginary = top + row * span_y / height
        for column in range(width):
            real = left + column * span_x / width
            iterations = escape_iterations(real, imaginary, max_iter)
            pixels[column, row] = palette_colour(iterations, max_iter)

    return image
