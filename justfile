preview target:
    @echo 'previewing {{target}}...'
    manim render main.py -ql --renderer opengl --write_to_movie {{target}}

build target:
    @echo 'building {{target}}...'
    manim render main.py -qk {{target}} --disable_caching

noise:
    manim render main.py CreateCircle
perlin:
    manim render main.py -ql --renderer opengl --write_to_movie Perlin
fractalperlin:
    manim render main.py -ql --renderer opengl --write_to_movie FractalPerlin