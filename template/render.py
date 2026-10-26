"""Renderizza un layout HTML in JPEG e controlla che nulla esca dalla pagina.

Uso:
  python3 template/render.py LAYOUT.html OUT.jpg [--img posts/AAAA-MM-GG.jpg]

- La dimensione si legge da <meta name="size" content="1080x1350"> (post) o 1080x1920 (story).
- {{POST_IMG}} nell'HTML viene sostituito con l'immagine passata con --img (serve alle story "peek").
- Stampa AVVISO per ogni elemento con testo che esce dai bordi o che va a capo oltre il suo box.
"""
import re
import sys
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright


def main() -> None:
    args = sys.argv[1:]
    img = None
    if "--img" in args:
        i = args.index("--img")
        img = Path(args[i + 1]).resolve()
        del args[i:i + 2]
    src, out = Path(args[0]).resolve(), Path(args[1])
    html = src.read_text(encoding="utf-8")
    m = re.search(r'name="size" content="(\d+)x(\d+)"', html)
    w, h = (int(m.group(1)), int(m.group(2))) if m else (1080, 1350)
    if img:
        html = html.replace("{{POST_IMG}}", img.as_uri())
    tmp = Path(tempfile.mkdtemp()) / "page.html"
    tmp.write_text(html, encoding="utf-8")

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(400)
        problems = pg.evaluate(
            """([W,H]) => {
              const out=[];
              for (const el of document.querySelectorAll('body *')) {
                if (!el.childNodes.length) continue;
                const hasText=[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
                if (!hasText) continue;
                const r=el.getBoundingClientRect();
                if (r.width===0) continue;
                if (r.left<-1||r.top<-1||r.right>W+1||r.bottom>H+1)
                  out.push('fuori pagina: '+el.textContent.trim().slice(0,50));
                else if (r.left<40||r.right>W-40)
                  out.push('troppo vicino al bordo (min 40px, la griglia 3:4 taglia i lati): '+el.textContent.trim().slice(0,50));
                if (el.scrollWidth>el.clientWidth+2 && getComputedStyle(el).overflow!=='visible')
                  out.push('testo tagliato: '+el.textContent.trim().slice(0,50));
              }
              return out;
            }""",
            [w, h],
        )
        png = out.with_suffix(".png")
        pg.screenshot(path=str(png))
        b.close()

    from PIL import Image
    Image.open(png).convert("RGB").save(out, quality=78)
    png.unlink()
    for pr in problems:
        print("AVVISO", pr)
    print(out, f"{w}x{h}", "OK" if not problems else f"{len(problems)} avvisi")


if __name__ == "__main__":
    main()
