from typing import Tuple
import numpy as np

P = [
    151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225,
    140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148,
    247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32,
    57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175,
    74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111, 229, 122,
    60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54,
    65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169,
    200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64,
    52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212,
    207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213,
    119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
    129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104,
    218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241,
    81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157,
    184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205, 93,
    222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180
]


def lerp(t, a, b):
    return a + t * (b - a)

class ImprovedNoise:
    p = P + P

    @staticmethod
    def fractal_with_derivative_noise(x, y, octaves=8, persistence=0.5):
        total = 0.0
        frequency = 1.0
        amplitude = 1.0
        max_value = 0.0

        d = np.zeros(2) # derivatives
        for _ in range(octaves):
            n, dndx, dndy = ImprovedNoise.noise_with_derivative(x * frequency, y * frequency)
            d += (dndx * amplitude, dndy * amplitude)
            factor = n / (1.0 + np.dot(d, d))
            total += amplitude * factor

            max_value += amplitude
            amplitude *= persistence
            frequency *= 2
        # if total > 1:
        #     print(f'-------- {total}, {max_value} --------')

        # Normalize to range [-1, 1]
        total /= max_value
        return total


    @staticmethod
    def fractal_noise(x, y, octaves=8, persistence=0.5):
        total = 0.0
        frequency = 1.0
        amplitude = 1.0
        max_value = 0.0  # Used for normalizing result to [-1, 1]

        for _ in range(octaves):
            total += ImprovedNoise.noise(x * frequency, y * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= 2

        # Normalize to range [-1, 1]
        total /= max_value
        return total


    @staticmethod
    def noise_with_derivative(x, y) -> Tuple[float, float, float]:
        # decimal part
        X = int(np.floor(x)) & 255
        Y = int(np.floor(y)) & 255

        # fractional part
        x -= np.floor(x)
        y -= np.floor(y)

        """
        fade(x) = 6x^5 - 15x^4 + 10x^3
        fade'(x) = 30x^4 - 60x^3 + 30x^2
        lerp(t, a, b) = a + t(b - a)

        u = fade(x)
        v = fade(y)

        so, we have:
        n = lerp(v, lerp(u, p0, p1), lerp(u, p2, p3))
          = lerp(u, p0, p1) + v(lerp(u, p2, p3) - lerp(u, p0, p1))
          = p0 + u(p1 - p0) + v(p2 + u(p3 - p2) - p0 - u(p1 - p0))
          = p0 + (p1 - p0)u + (p2 - p0)v + (p3 - p2 - p1 + p0)uv
        
        so, we have:
        dn/dx = ((p1 - p0) + (p3 - p2 - p1 + p0)v) * u'(x)
        dn/dy = ((p2 - p0) + (p3 - p2 - p1 + p0)u) * v'(y)
        """
        u = ImprovedNoise.fade(x)
        v = ImprovedNoise.fade(y)

        """
            0---01-----1
            |   |      |
            |   p      |
            |   |      |
            2---23-----3
        """
        A = ImprovedNoise.p[X] + Y
        B = ImprovedNoise.p[X + 1] + Y
        p0 = ImprovedNoise.grad(ImprovedNoise.p[A], x, y)
        p1 = ImprovedNoise.grad(ImprovedNoise.p[B], x - 1, y)
        p2 = ImprovedNoise.grad(ImprovedNoise.p[A + 1], x, y - 1)
        p3 = ImprovedNoise.grad(ImprovedNoise.p[B + 1], x - 1, y - 1)

        n = lerp(v, lerp(u, p0, p1), lerp(u, p2, p3))
        dndx = ((p1 - p0) + (p3 - p2 - p1 + p0) * v) * ImprovedNoise.fade_d(x)
        dndy = ((p2 - p0) + (p3 - p2 - p1 + p0) * u) * ImprovedNoise.fade_d(y)

        return (n, dndx, dndy)
        
    

    @staticmethod
    def noise(x, y):
        # decimal part
        X = int(np.floor(x)) & 255
        Y = int(np.floor(y)) & 255

        # fractional part
        x -= np.floor(x)
        y -= np.floor(y)

        u = ImprovedNoise.fade(x)
        v = ImprovedNoise.fade(y)

        """
            0---01-----1
            |   |      |
            |   p      |
            |   |      |
            2---23-----3
        """
        A = ImprovedNoise.p[X] + Y
        B = ImprovedNoise.p[X + 1] + Y
        p0 = ImprovedNoise.grad(ImprovedNoise.p[A], x, y)
        p1 = ImprovedNoise.grad(ImprovedNoise.p[B], x - 1, y)
        p2 = ImprovedNoise.grad(ImprovedNoise.p[A + 1], x, y - 1)
        p3 = ImprovedNoise.grad(ImprovedNoise.p[B + 1], x - 1, y - 1)

        
        return lerp(v, lerp(u, p0, p1), lerp(u, p2, p3))


    @staticmethod
    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    @staticmethod
    def fade_d(t):
        return 30 * t * t * (t * (t - 2) + 1)

    @staticmethod
    def grad(hash, x, y):
        arr = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        h = hash & 0b111
        return (x * arr[h][0] + y * arr[h][1]) / np.sqrt(5)


def map_value(x, original_bound, target_bound):
    return x / original_bound * target_bound


LATTICE_CNT = 8

def get_noise(x, y, size):
    return ImprovedNoise.noise(map_value(x, size, LATTICE_CNT), map_value(y, size, LATTICE_CNT))

def get_fractal_noise(x, y, size):
    return ImprovedNoise.fractal_noise(map_value(x, size, LATTICE_CNT), map_value(y, size, LATTICE_CNT))

def get_fractal_with_derivative_noise(x, y, size):
    return ImprovedNoise.fractal_with_derivative_noise(map_value(x, size, LATTICE_CNT), map_value(y, size, LATTICE_CNT))

def generate_perlin_noise(width, height):
    noise = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            mapped_x = map_value(x, width, LATTICE_CNT)
            mapped_y = map_value(y, height, LATTICE_CNT)
            # print(f'{x}, {y} -> {mapped_x}, {mapped_y}')
            noise[y][x] = ImprovedNoise.noise(mapped_x, mapped_y)
    noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))
    return noise


def generate_fractal_perlin_noise(width, height, octaves=4, persistence=0.5):
    noise = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            mapped_x = map_value(x, width, LATTICE_CNT)
            mapped_y = map_value(y, height, LATTICE_CNT)
            noise[y][x] = ImprovedNoise.fractal_noise(mapped_x, mapped_y, octaves, persistence)
    noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))
    return noise

def generate_fractal_with_derivative_perlin_noise(width, height, octaves=4, persistence=0.5):
    noise = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            mapped_x = map_value(x, width, LATTICE_CNT)
            mapped_y = map_value(y, height, LATTICE_CNT)
            noise[y][x] = ImprovedNoise.fractal_with_derivative_noise(mapped_x, mapped_y, octaves, persistence)
    noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))
    return noise
