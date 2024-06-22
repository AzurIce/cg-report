from manim import *

from perlin import *

size = 32
width, height = size, size
depth = 3


def color_func(u, v, get_noise_func):
    z = get_noise_func(v, u)

    if z < -0.5:
        return BLUE
    elif z < 0:
        return interpolate_color(GREEN, YELLOW, np.interp(z, [-0.5, 0], [0, 1]))
    elif z < 0.5:
        return interpolate_color(YELLOW, BROWN, np.interp(z, [0, 0.5], [0, 1]))
    elif z < 0.7:
        return interpolate_color(BROWN, GRAY, np.interp(z, [0.5, 1], [0, 1]))
    else:
        return WHITE


class PerlinNoise(Scene):
    def construct(self):
        noise = generate_perlin_noise(width, height)
        scale = 32.0

        img = ImageMobject(self.noise_to_image(noise))
        img.scale(scale)
        self.add(img)

    def noise_to_image(self, noise):
        from PIL import Image

        noise = (255 * noise).astype(np.uint8)
        return Image.fromarray(noise)


class FractalPerlinNoise(Scene):
    def construct(self):
        noise = generate_fractal_perlin_noise(width, height)
        scale = 32.0

        img = ImageMobject(self.noise_to_image(noise))
        img.scale(scale)
        self.add(img)

    def noise_to_image(self, noise):
        from PIL import Image

        noise = (255 * noise).astype(np.uint8)
        return Image.fromarray(noise)


class FractalWithDerivativePerlinNoise(Scene):
    def construct(self):
        noise = generate_fractal_with_derivative_perlin_noise(width, height)
        scale = 32.0

        img = ImageMobject(self.noise_to_image(noise))
        img.scale(scale)
        self.add(img)

    def noise_to_image(self, noise):
        from PIL import Image

        noise = (255 * noise).astype(np.uint8)
        return Image.fromarray(noise)


from abc import ABC, abstractmethod

class Terrain(ThreeDScene):
    @abstractmethod
    def noise_func(self, x, y, size):
        pass

    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        cut_radius = 16

        mid = (size - 1) // 2
        l = mid - cut_radius + 1
        r = mid + cut_radius - 1
        range = (l, r)
        surface = Surface(
            lambda u, v: axes.c2p(
                u,
                v,
                self.noise_func(v, u, size) * depth
            ),
            resolution=cut_radius * 2 * 16,
            u_range=range,
            v_range=range,
            checkerboard_colors=False,
        )

        surface.shift(size / 2 * (DOWN + LEFT))
        surface.set_style(fill_opacity=1)
        surface.set_fill_by_value(axes=axes, colorscale=[(c, x * depth) for c, x in [(BLUE_E, -1.0), (BLUE_E, -0.9), (BLUE_C, -0.8), (GOLD_E, -0.7), (GRAY_BROWN, -0.1), (GRAY_BROWN, 0.1), (DARK_GRAY, 0.25), (GRAY, 0.6), (WHITE, 0.7), (WHITE, 1.0)]])
        self.add(surface)

        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES, zoom=0.5)

        T = 5
        self.begin_ambient_camera_rotation(rate=1 / T * 2)
        self.wait(T)


class Perlin(Terrain):
    def noise_func(self, x, y, size):
        return get_noise(x, y, size)


class FractalPerlin(Terrain):
    def noise_func(self, x, y, size):
        return get_fractal_noise(x, y, size) * depth


class FractalWithDerivativePerlin(Terrain):
    def noise_func(self, x, y, size):
        return get_fractal_with_derivative_noise(x, y, size) * depth

