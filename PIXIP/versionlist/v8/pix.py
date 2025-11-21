# This module is made by REI otherwise known as KeiNeroKami in Github
# Codespace helper: gpt-5.1
# ====================<REIME>====================
# v0.8 Efficiency Patch Notes
# Fixed fleep extension retrieval with safe fallback
# Corrected image sizing tiers: 250, 500, 1000, 2500, 3000
# Optimized encode/decode loops using flat index traversal
# Improved byte packing via bit shifting
# Safer padding removal for null-bytes
# Unified error handling and progress logging
# Reduced redundant file checks and simplified logicands
# 
# 
# Made: 11, 21, 25
# ===============================================


from PIL import Image
import math, os, sys, fleep


class pixip:

    @staticmethod
    def num2rgba(n: int) -> tuple[int, int, int, int]:
        return (n >> 8, n & 0xFF, 0, 255)

    @staticmethod
    def rgba2num(px: tuple[int, int, int, int]) -> int:
        r, g, _, _ = px
        return (r << 8) | g

    @staticmethod
    def choose_size(px_needed: int) -> int:
        # Clean sizing tiers
        if px_needed <= 250**2:  return 250
        if px_needed <= 500**2:  return 500
        if px_needed <= 1000**2: return 1000
        if px_needed <= 2500**2: return 2500
        return 3000

    def __init__(self, in_file: str, out_img: str = "pixip_output.png"):
        self.in_file = in_file
        self.out_img = out_img

    
    # ENCODER
    def enc(self) -> bool:
        if not os.path.exists(self.in_file):
            raise FileNotFoundError(f"File {self.in_file} not found")

        try:
            data = open(self.in_file, "rb").read()
            ln = len(data)
            px_needed = math.ceil(ln / 2)

            sz = self.choose_size(px_needed)
            img = Image.new("RGBA", (sz, sz))
            pixels = img.load()

            i = 0
            total_px = sz * sz

            for p in range(total_px):
                if i < ln:
                    # Pack data[i] & data[i+1]
                    b1 = data[i]
                    b2 = data[i + 1] if i + 1 < ln else 0
                    n = (b1 << 8) | b2

                    x = p % sz
                    y = p // sz
                    pixels[x, y] = self.num2rgba(n)

                    i += 2

                    # Dev progress
                    if p % 5000 == 0:
                        print(f"\rEncoding: {round((i / ln) * 100, 2)}%", end="")
                else:
                    break

            img.save(self.out_img)
            print("\nEncode done.")
            return True

        except Exception as e:
            print("ENC ERROR:", e)
            return False

    
    # DECODER
    def denc(self, out_name: str = "pix-decoded") -> bool:
        if not os.path.exists(self.out_img):
            raise FileNotFoundError(f"Image {self.out_img} not found")

        try:
            img = Image.open(self.out_img)
            pixels = img.load()
            w, h = img.size

            data = bytearray()
            total = w * h

            for p in range(total):
                x = p % w
                y = p // w

                r, g, b, a = pixels[x, y]
                if (r, g, b, a) != (0, 0, 0, 0):
                    n = self.rgba2num((r, g, b, a))
                    data.append(n >> 8)
                    data.append(n & 0xFF)

                if p % 5000 == 0:
                    print(f"\rDecoding: {round((p / total) * 100, 2)}%", end="")

            # Remove zero-padding - gptfixes
            while data and data[-1] == 0:
                data.pop()

            # Write temp raw file - gptfixes
            raw_path = out_name
            open(raw_path, "wb").write(data)

            # Detect extension properly - gptfixes
            with open(raw_path, "rb") as f:
                info = fleep.get(f.read(128))

            # Fleep fix: ensure extension list exists - gptfixes
            if info.extension:
                ext = info.extension[0]
            else:
                ext = "bin"

            final_name = f"{raw_path}.{ext}"
            os.rename(raw_path, final_name)

            print(f"\nDecoded → {final_name}")
            return True

        except Exception as e:
            print("DENC ERROR:", e)
            return False
