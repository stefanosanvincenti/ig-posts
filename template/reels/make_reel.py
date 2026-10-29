"""Esporta un Reel da una pagina HTML con window.setT(t).

Uso: python3 template/reels/make_reel.py PAGINA.html OUT.mp4 DURATA_SECONDI [fps]
Produce MP4 H.264 1080x1920, 30 fps, con traccia audio silenziosa (Instagram accetta meglio i video con audio;
la musica si sceglie in Metricool/Instagram).
"""
import subprocess
import sys
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright


def main() -> None:
    src, out, dur = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), float(sys.argv[3])
    fps = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    tmp = Path(tempfile.mkdtemp())
    n = int(dur * fps)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        pg.goto(src.as_uri())
        pg.wait_for_timeout(500)
        for i in range(n):
            pg.evaluate(f"window.setT({i / fps})")
            pg.screenshot(path=str(tmp / f"f{i:05d}.png"))
        b.close()
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "f%05d.png"),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20",
        "-preset", "medium", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out),
    ], check=True)
    print(out, f"{n} frame", f"{out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
