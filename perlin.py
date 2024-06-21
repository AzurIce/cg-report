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


class ImprovedNoise:
    p = P + P

    @staticmethod
    def fractal_noise(x, y, octaves=4, persistence=0.5):
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

        return ImprovedNoise.lerp(
            v,
            ImprovedNoise.lerp(
                u,
                ImprovedNoise.grad(ImprovedNoise.p[A], x, y),
                ImprovedNoise.grad(ImprovedNoise.p[B], x - 1, y),
            ),
            ImprovedNoise.lerp(
                u,
                ImprovedNoise.grad(ImprovedNoise.p[A + 1], x, y - 1),
                ImprovedNoise.grad(ImprovedNoise.p[B + 1], x - 1, y - 1),
            ),
        )

    @staticmethod
    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    def lerp(t, a, b):
        return a + t * (b - a)

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
