from manim import *

from perlin import *

size = 32
width, height = size, size
depth = 5


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


class FractalWithDerivativePerlin(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        cut_radius = 16

        mid = (size - 1) // 2
        l = mid - cut_radius + 1
        r = mid + cut_radius - 1
        range = (l, r)
        surface = Surface(
            lambda u, v: [
                u,
                v,
                get_fractal_with_derivative_noise(v, u, size) * depth
            ],
            resolution=cut_radius * 2 * 4,
            u_range=range,
            v_range=range,
        )

        surface.shift(size / 2 * (DOWN + LEFT))
        self.add(surface)

        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        T = 5
        self.begin_ambient_camera_rotation(rate=1 / T)
        self.wait(T)

class Perlin(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        cut_radius = 16

        mid = (size - 1) // 2
        l = mid - cut_radius + 1
        r = mid + cut_radius - 1
        range = (l, r)
        surface = Surface(
            lambda u, v: [
                u,
                v,
                get_noise(v, u, size) * depth
            ],
            resolution=cut_radius * 2 * 4,
            u_range=range,
            v_range=range,
        )

        surface.shift(size / 2 * (DOWN + LEFT))
        self.add(surface)

        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        T = 5
        self.begin_ambient_camera_rotation(rate=1 / T)
        self.wait(T)


class FractalPerlin(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        cut_radius = 16

        mid = (size - 1) // 2
        l = mid - cut_radius + 1
        r = mid + cut_radius - 1
        range = (l, r)
        surface = Surface(
            lambda u, v: [
                u,
                v,
                get_fractal_noise(v, u, size) * depth
            ],
            resolution=cut_radius * 2 * 8,
            u_range=range,
            v_range=range,
        )

        surface.shift(size / 2 * (DOWN + LEFT))
        self.add(surface)

        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        T = 5
        self.begin_ambient_camera_rotation(rate=1 / T)
        self.wait(T)
