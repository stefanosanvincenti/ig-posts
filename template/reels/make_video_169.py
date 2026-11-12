"""Video orizzontale 1920x1080 (per email/YouTube) da pagina HTML con window.setT(t), musica soft a volume basso.
Uso: python3 template/reels/make_video_169.py PAGINA.html OUT.mp4 DURATA MOOD [fps]"""
import subprocess, sys, tempfile, wave
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import make_story_video as M
from playwright.sync_api import sync_playwright

src, out, dur, mood = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
fps = int(sys.argv[5]) if len(sys.argv) > 5 else 24
tmp = Path(tempfile.mkdtemp())
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(src.as_uri()); pg.wait_for_timeout(500)
    for i in range(int(dur * fps)):
        pg.evaluate(f"window.setT({i / fps})"); pg.screenshot(path=str(tmp / f"f{i:05d}.jpg"), type="jpeg", quality=92)
    b.close()
M.T = dur; M.t = np.arange(int(M.SR * dur)) / M.SR; t = M.t
o = M.MOODS[mood](); o = o * np.clip(t / 1.2, 0, 1) * np.clip((dur - t) / 2, 0, 1); o = o / np.max(np.abs(o)) * 0.3
s = (o * 32767).astype(np.int16)
with wave.open(str(tmp / "a.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(M.SR); w.writeframes(np.column_stack([s, s]).ravel().tobytes())
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "f%05d.jpg"), "-i", str(tmp / "a.wav"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24", "-preset", "medium", "-c:a", "aac", "-b:a", "128k",
                "-shortest", "-movflags", "+faststart", str(out)], check=True)
print(out, f"{out.stat().st_size // 1024} KB")
