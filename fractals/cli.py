"""Command line entry point for rendering a Mandelbrot image to a PNG file."""

import argparse

from fractals.mandelbrot import render


def build_parser():
    """Build the argument parser for the renderer."""
    parser = argparse.ArgumentParser(
        description="Render the Mandelbrot set and write it to a PNG file."
    )
    parser.add_argument("--width", type=int, default=800, help="image width in pixels")
    parser.add_argument("--height", type=int, default=600, help="image height in pixels")
    parser.add_argument("--max-iter", type=int, default=200, help="iteration budget per pixel")
    parser.add_argument("--cx", type=float, default=-0.5, help="centre of the view, real part")
    parser.add_argument("--cy", type=float, default=0.0, help="centre of the view, imaginary part")
    parser.add_argument("--zoom", type=float, default=1.0, help="zoom factor, larger is closer")
    parser.add_argument("--output", default="mandelbrot.png", help="path of the PNG to write")
    return parser


def main(argv=None):
    """Parse arguments, render an image and save it."""
    args = build_parser().parse_args(argv)
    image = render(args.width, args.height, args.max_iter, args.cx, args.cy, args.zoom)
    image.save(args.output, format="PNG")
    print("wrote {0}".format(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
