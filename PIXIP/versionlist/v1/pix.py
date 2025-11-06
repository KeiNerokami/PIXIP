from PIL import Image
import math, os, sys

class pixip:
    # File-to-RGBA pixel encoder/decoder with sizing.

    @staticmethod
    def num2rgba(n: int) -> tuple[int, int, int, int]:
        # Encode a 0->65535 number into an RGBA pixel.
        return (n // 256, n % 256, 0, 255)

    @staticmethod
    def rgba2num(rgba: tuple[int, int, int, int]) -> int:
        # Decode an RGBA pixel back into a number for a hexmap.
        r, g, _, _ = rgba
        return r * 256 + g

    @staticmethod
    def file_dims(file_size: int, bpp: int = 2) -> int:
        # Compute square image side length to store the file (bytes per pixel = bpp).
        total_px = math.ceil(file_size / bpp)
        return math.ceil(math.sqrt(total_px))
    # Initialz
    def __init__(self, in_file: str, out_img: str = "pixip_output.png"):
        self.in_file = in_file
        self.out_img = out_img

    def enc(self) -> bool:
        # Encode file into an RGBA image. Returns True if good, False if bad.
        if os.path.exists(self.in_file) is True:
            try:
                with open(self.in_file, "rb") as f:
                    data = f.read()

                ln = len(data)
                px_needed = math.ceil(ln / 2)

                # Determine image size
                if px_needed <= 250**2:
                    sz = 250
                elif px_needed <= 500**2:
                    sz = 500
                elif px_needed <= 100**2:
                    sz = 1000
                elif px_needed <= 1000**2:
                    sz = 2500
                else:
                    sz = 3000

                img = Image.new("RGBA", (sz, sz))
                pixels = img.load()

                # Pixel encoding
                i = 0
                for y in range(sz):
                    for x in range(sz):
                        if i < ln:
                            n = data[i] * 256 + (data[i+1] if i+1 < ln else 0)
                            pixels[x, y] = self.num2rgba(n)
                            i += 2

                            print(f'\rDev: X: {x}, Y: {y}, PX: {i}, TTX: {round(i / ln,2)}%' , end='')
                            sys.stdout.flush()
                        else:
                            pixels[x, y] = (0, 0, 0, 0)
                            
                img.save(self.out_img)
                return True

            except Exception:
                return False
        else:
            raise FileNotFoundError(f'file {self.in_file} does not exist')


    def denc(self, out_txt: str = "pix-decoded.txt") -> bool:
        # Decode RGBA image back into the original file. Returns True if goodi, False bad.
        if os.path.exists(self.in_file) is True:
            try:
                img = Image.open(self.out_img)
                pixels = img.load()
                w, h = img.size
                data = bytearray()

                for y in range(h):
                    for x in range(w):
                        r, g, b, a = pixels[x, y][:4]
                        if (r, g, b, a) != (0, 0, 0, 0):
                            n = self.rgba2num((r, g, b, a))
                            data.extend([n // 256, n % 256])
                            print(f'\rX: {x}, Y: {y}, RGBa: ({r}, {g}, {b}, {a})', end='')
                            sys.stdout.flush()
                # Remove excess zeros
                while data and data[-1] == 0:
                    data.pop()

                with open(out_txt, "wb") as f:
                    f.write(data)
                return True
            except FileNotFoundError:
                return False

            except Exception:
                return False
        else:
            raise FileNotFoundError(f'file {self.in_file} does not exist')