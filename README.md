# fractals

A small Mandelbrot renderer with a command line tool and an HTTP endpoint.

Install the dependencies with `pip install -r requirements.txt`, then render a
picture from the command line:

    python -m fractals.cli --width 800 --height 600 --zoom 1.5 --output out.png

Or start the server and ask it for an image in the browser:

    python -m fractals.server
    open http://localhost:5000/render?width=400&height=300&max_iter=200
