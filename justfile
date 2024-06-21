render target:
    manim render main.py -ql {{target}}

preview target:
    @echo 'previewing {{target}}...'
    manim render main.py -ql --renderer opengl --write_to_movie {{target}}

build target:
    @echo 'building {{target}}...'
    manim render main.py -qk {{target}} --disable_caching

noise:
    manim render main.py -qk PerlinNoise FractalPerlinNoise FractalWithDerivativePerlinNoise
terrain:
    manim render main.py -qk Perlin FractalPerlin FractalWithDerivativePerlin