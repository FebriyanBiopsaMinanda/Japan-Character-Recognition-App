import os
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import numpy as np

# =========================
# KONFIGURASI
# =========================
FONT_DIR = "Japanese Font"
OUTPUT_DIR = "Dataset/Katakana Images"
IMAGE_SIZE = (256, 256)
BACKGROUND_COLOR = "white"

TARGET_IMAGES_PER_CHAR = 500
BASE_AUGMENT_COUNT = 250
MORPH_AUGMENT_COUNT = 250

BASE_MIN_FONT_SIZE = 105
BASE_MAX_FONT_SIZE = 135

random.seed(42)
np.random.seed(42)

# =========================
# DATA KATAKANA
# =========================
katakana_map = {
    "a": "ア", "i": "イ", "u": "ウ", "e": "エ", "o": "オ",
    "ka": "カ", "ki": "キ", "ku": "ク", "ke": "ケ", "ko": "コ",
    "sa": "サ", "shi": "シ", "su": "ス", "se": "セ", "so": "ソ",
    "ta": "タ", "chi": "チ", "tsu": "ツ", "te": "テ", "to": "ト",
    "na": "ナ", "ni": "ニ", "nu": "ヌ", "ne": "ネ", "no": "ノ",
    "ha": "ハ", "hi": "ヒ", "fu": "フ", "he": "ヘ", "ho": "ホ",
    "ma": "マ", "mi": "ミ", "mu": "ム", "me": "メ", "mo": "モ",
    "ya": "ヤ", "yu": "ユ", "yo": "ヨ",
    "ra": "ラ", "ri": "リ", "ru": "ル", "re": "レ", "ro": "ロ",
    "wa": "ワ", "wo": "ヲ", "n": "ン"
}

# =========================
# FONT
# =========================
def get_font_files(font_dir):
    path = Path(font_dir)

    if not path.exists():
        raise FileNotFoundError(f"Folder font '{font_dir}' tidak ditemukan.")

    font_files = []
    for ext in ("*.ttf", "*.otf", "*.ttc"):
        font_files.extend(path.glob(ext))

    font_files = sorted(font_files)

    if not font_files:
        raise FileNotFoundError(f"Tidak ada file font di folder '{font_dir}'.")

    return font_files


def font_supports_char(font_path, char):
    """
    Cek apakah font bisa merender karakter tertentu.
    Font yang gagal dibuka atau tidak menghasilkan glyph akan di-skip.
    """
    try:
        font = ImageFont.truetype(str(font_path), 96)
        img = Image.new("L", (160, 160), 255)
        draw = ImageDraw.Draw(img)

        bbox = draw.textbbox((0, 0), char, font=font)
        if bbox is None:
            return False

        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w <= 0 or h <= 0:
            return False

        x = (160 - w) // 2 - bbox[0]
        y = (160 - h) // 2 - bbox[1]
        draw.text((x, y), char, font=font, fill=0)

        arr = np.array(img)
        # kalau semuanya putih berarti tidak benar-benar merender
        return np.any(arr < 250)

    except Exception:
        return False


def get_valid_fonts_for_char(font_files, char):
    return [f for f in font_files if font_supports_char(f, char)]

# =========================
# AUGMENTASI
# =========================
def add_noise(img):
    img = img.copy()
    pixels = img.load()
    w, h = img.size

    for _ in range(int(w * h * 0.002)):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        val = 0 if random.random() < 0.5 else 255
        pixels[x, y] = (val, val, val)

    return img


def draw_text_with_thickness(draw, position, text, font, thickness=1):
    x, y = position

    if thickness <= 1:
        draw.text((x, y), text, fill="black", font=font)
        return

    offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in offsets[:min(len(offsets), thickness + 1)]:
        draw.text((x + dx, y + dy), text, fill="black", font=font)


def create_base_image(text, font_path):
    img = Image.new("RGB", IMAGE_SIZE, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    font_size = random.randint(BASE_MIN_FONT_SIZE, BASE_MAX_FONT_SIZE)
    font = ImageFont.truetype(str(font_path), font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    shift_x = random.randint(-12, 12)
    shift_y = random.randint(-12, 12)
    x = (IMAGE_SIZE[0] - w) // 2 - bbox[0] + shift_x
    y = (IMAGE_SIZE[1] - h) // 2 - bbox[1] + shift_y

    thickness = random.randint(1, 2)
    draw_text_with_thickness(draw, (x, y), text, font, thickness=thickness)

    if random.random() < 0.35:
        angle = random.uniform(-10, 10)
        img = img.rotate(
            angle,
            resample=Image.Resampling.BICUBIC,
            expand=False,
            fillcolor="white"
        )

    if random.random() < 0.30:
        img = img.filter(ImageFilter.GaussianBlur(0.5))

    if random.random() < 0.30:
        img = add_noise(img)

    return img


def apply_morph(img):
    """
    Erosi/dilasi dengan background tetap putih dan tulisan tetap hitam.
    """
    gray = np.array(img.convert("L"))
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # invert supaya tulisan jadi foreground putih
    inv = 255 - binary
    kernel_size = random.choice([2, 3])
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    if random.random() < 0.5:
        morphed = cv2.erode(inv, kernel, iterations=random.choice([1, 1, 2]))
    else:
        morphed = cv2.dilate(inv, kernel, iterations=random.choice([1, 1, 2]))

    final = 255 - morphed
    return Image.fromarray(final).convert("RGB")

# =========================
# MAIN
# =========================
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_fonts = get_font_files(FONT_DIR)
    print(f"Jumlah file font ditemukan: {len(all_fonts)}")

    total = 0
    skipped_chars = []

    for romaji, char in katakana_map.items():
        folder = os.path.join(OUTPUT_DIR, romaji)
        os.makedirs(folder, exist_ok=True)

        print(f"Memproses huruf: {romaji}")

        valid_fonts = get_valid_fonts_for_char(all_fonts, char)

        if not valid_fonts:
            print(f"  Tidak ada font valid untuk huruf: {romaji}. Dilewati.")
            skipped_chars.append(romaji)
            continue

        print(f"  Font valid untuk {romaji}: {len(valid_fonts)}")

        # 250 gambar base
        for i in range(1, BASE_AUGMENT_COUNT + 1):
            font = valid_fonts[(i - 1) % len(valid_fonts)]
            save_path = os.path.join(folder, f"{i:03d}.png")

            try:
                img = create_base_image(char, font)
                img.save(save_path)
                total += 1
            except Exception as e:
                print(f"  Gagal render base {romaji} | {font.name} | {e}")

        # 250 gambar morph
        for i in range(BASE_AUGMENT_COUNT + 1, TARGET_IMAGES_PER_CHAR + 1):
            font = valid_fonts[(i - 1) % len(valid_fonts)]
            save_path = os.path.join(folder, f"{i:03d}.png")

            try:
                img = create_base_image(char, font)
                img = apply_morph(img)
                img.save(save_path)
                total += 1
            except Exception as e:
                print(f"  Gagal render morph {romaji} | {font.name} | {e}")

    print(f"Total gambar berhasil dibuat: {total}")
    print(f"Hasil tersimpan di: {OUTPUT_DIR}")

    if skipped_chars:
        print("Huruf yang dilewati karena tidak ada font valid:")
        print(", ".join(skipped_chars))


if __name__ == "__main__":
    main()