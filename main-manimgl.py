from manimlib import *
from perlin import *

size = 32
width, height = size, size
depth = 3

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
        pil_img = Image.fromarray(noise)
        return np.array(pil_img)

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
        pil_img = Image.fromarray(noise)
        return np.array(pil_img)

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
        pil_img = Image.fromarray(noise)
        return np.array(pil_img)

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

        colorscale = [
            (BLUE_E, -1.0), (BLUE_E, -0.9), (BLUE_C, -0.8),
            (GOLD_E, -0.7), (GREY_BROWN, -0.1), (GREY_BROWN, 0.1),
            (GREY_D, 0.25), (GREY, 0.6), (WHITE, 0.7), (WHITE, 1.0)
        ]

        def color_func(z):
            t = z / depth
            t = min(max(t, -1.0), 1.0)
            for i in range(len(colorscale)-1):
                c1, x1 = colorscale[i]
                c2, x2 = colorscale[i+1]
                if x1 <= t <= x2:
                    a = (t - x1)/(x2 - x1)
                    return color_to_rgb(interpolate_color(c1, c2, a))
            return color_to_rgb(colorscale[-1][0])

        resolution = cut_radius * 2 * 16
        surface = ParametricSurface(
            lambda u, v: np.array([
                u,
                v,
                self.noise_func(v, u, size) * depth
            ]),
            u_range=(l, r),
            v_range=(l, r),
            resolution=(resolution, resolution),
        )

        # 手动设置面颜色
        points = surface.get_points()
        z_values = points[:, 2]
        surface.set_color_by_rgb_func(lambda p: color_func(p[2]))
        surface.shift(size/2 * (DOWN + LEFT))
        self.add(surface)

        self.camera.frame.set_euler_angles(phi=70 * DEGREES, theta=30 * DEGREES)
        self.camera.frame.set_width(20)

        T = 5
        rate = 0.2
        def update_camera(mob, dt):
            mob.increment_theta(rate * dt)
        self.camera.frame.add_updater(update_camera)
        self.wait(T)
        self.camera.frame.remove_updater(update_camera)

class Perlin(Terrain):
    def noise_func(self, x, y, size):
        return get_noise(x, y, size)

class FractalPerlin(Terrain):
    def noise_func(self, x, y, size):
        return get_fractal_noise(x, y, size) * depth

class FractalWithDerivativePerlin(Terrain):
    def noise_func(self, x, y, size):
        return get_fractal_with_derivative_noise(x, y, size) * depth