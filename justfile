previewall:
    manim render main.py -ql Perlin --disable_caching &
    manim render main.py -ql FractalPerlin --disable_caching &
    manim render main.py -ql FractalWithDerivativePerlin --disable_caching &

render target:
    manim render main.py -ql {{target}} --disable_caching

preview target:
    @echo 'previewing {{target}}...'
    manim render main.py -ql {{target}} --disable_caching

build target:
    @echo 'building {{target}}...'
    manim render main.py -qk {{target}} --disable_caching

noise:
    manim render main.py -qk --disable_caching PerlinNoise FractalPerlinNoise FractalWithDerivativePerlinNoise
terrain:
    manim render main.py -qk --disable_caching Perlin FractalPerlin FractalWithDerivativePerlin
