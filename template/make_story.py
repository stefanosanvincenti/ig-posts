"""Crea la versione story 9:16 (1080x1920) di un post 4:5.

Uso: python3 template/make_story.py posts/AAAA-MM-GG.jpg
Output: posts/AAAA-MM-GG-story.jpg (grafica intera centrata, niente tagli).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG = (12, 8, 24)        # #0C0818
VIOLA = (168, 85, 247)  # #A855F7
CIANO = (57, 229, 255)  # #39E5FF
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def main(path: str) -> None:
    src_path = Path(path)
    src = Image.open(src_path).convert("RGB")
    W, H = 1080, 1920
    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)

    tw = 1000
    th = int(src.height * tw / src.width)
    post = src.resize((tw, th), Image.LANCZOS)
    x, y = (W - tw) // 2, (H - th) // 2 + 40

    d.rounded_rectangle([x - 4, y - 4, x + tw + 4, y + th + 4], radius=28, outline=VIOLA, width=4)
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw, th], radius=24, fill=255)
    canvas.paste(post, (x, y), mask)

    font = ImageFont.truetype(FONT, 46)
    label = "NUOVO POST SUL PROFILO"
    d.text(((W - d.textlength(label, font=font)) / 2, y - 110), label, font=font, fill=CIANO)

    out = src_path.with_name(src_path.stem + "-story.jpg")
    canvas.save(out, quality=80)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
