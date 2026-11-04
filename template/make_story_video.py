"""Trasforma una story statica (JPG 1080x1920) in un video di 12 s con leggero movimento e musica a tema,
composta al volo, a VOLUME BASSO (picco circa -9 dBFS, media circa -22 dB): niente sirene o suoni forti.

Uso: python3 template/make_story_video.py posts/AAAA-MM-GG-story.jpg posts/AAAA-MM-GG-story.mp4 MOOD
MOOD:
  tensione  -> cybersecurity/NIS2: archi morbidi in minore, battito leggero, ticchettio discreto
  positivo  -> SEO/GEO/crescita: accordi maggiori luminosi, arpeggio delicato, ritmo morbido
  tech      -> siti web/e-commerce/tecnico: synth caldo, pulsazione regolare, campanelli leggeri
"""
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

SR = 44100
T = 12.0
t = np.arange(int(SR * T)) / SR


def burst(b, dur, tau, att=0.003):
    e = np.zeros_like(t)
    m = (t >= b) & (t < b + dur)
    x = t[m] - b
    e[m] = np.exp(-x / tau) * np.minimum(1, x / att)
    return e


def soft(f, det=0.0, harm=6, roll=1.6):
    return sum(np.sin(2 * np.pi * f * (1 + det) * k * t) / k ** roll for k in range(1, harm + 1))


def pad(chord, det=0.003):
    return sum(soft(f, det) + soft(f, -det) for f in chord)


def mood_tensione():
    o = 0.10 * pad((146.83, 174.61, 220.0)) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.35 * t))
    o += 0.05 * soft(233.08) * np.clip((t - 6) / 3, 0, 1)
    for b in np.arange(0.4, T - 0.4, 0.75):
        o += 0.22 * np.sin(2 * np.pi * 73.42 * (t - b)) * burst(b, 0.6, 0.18, 0.01)
    for k, b in enumerate(np.arange(0.25, T - 0.3, 0.5)):
        o += 0.05 * np.sin(2 * np.pi * (2600 if k % 2 else 2200) * (t - b)) * burst(b, 0.03, 0.006, 0.001)
    for b, f in [(1.5, 587.33), (3.0, 698.46), (4.5, 659.25), (6.0, 587.33), (7.5, 554.37), (9.0, 587.33)]:
        o += 0.07 * (np.sin(2 * np.pi * f * (t - b)) + 0.3 * np.sin(2 * np.pi * 2 * f * (t - b))) * burst(b, 1.4, 0.45, 0.01)
    return o


def mood_positivo():
    chords = [(261.63, 329.63, 392.0), (220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (196.0, 246.94, 293.66)]
    o = np.zeros_like(t)
    for i, ch in enumerate(chords * 2):
        b = i * 1.5
        w = np.clip((t - b) / 0.3, 0, 1) * np.clip((b + 1.6 - t) / 0.3, 0, 1)
        o += 0.06 * pad(ch, 0.002) * w
    arp = [523.25, 659.25, 783.99, 1046.5, 783.99, 659.25]
    for k, b in enumerate(np.arange(0.5, T - 0.5, 0.375)):
        f = arp[k % len(arp)]
        o += 0.045 * (np.sin(2 * np.pi * f * (t - b)) + 0.25 * np.sin(2 * np.pi * 2 * f * (t - b))) * burst(b, 0.6, 0.18, 0.004)
    for b in np.arange(0.5, T - 0.5, 0.75):
        o += 0.16 * np.sin(2 * np.pi * 65.41 * (t - b)) * burst(b, 0.4, 0.12, 0.008)
    return o


def mood_tech():
    o = 0.07 * pad((110.0, 164.81, 220.0, 277.18), 0.004) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * t))
    for k, b in enumerate(np.arange(0.25, T - 0.4, 0.25)):
        f = 220.0 if k % 4 else 330.0
        o += 0.05 * np.sin(2 * np.pi * f * (t - b)) * burst(b, 0.2, 0.05, 0.003)
    for b in np.arange(0.5, T - 0.5, 1.0):
        o += 0.18 * np.sin(2 * np.pi * 55 * (t - b)) * burst(b, 0.5, 0.15, 0.008)
    for b, f in [(2.0, 1318.5), (5.0, 1174.7), (8.0, 1318.5), (10.0, 1568.0)]:
        o += 0.04 * np.sin(2 * np.pi * f * (t - b)) * burst(b, 1.0, 0.35, 0.005)
    return o


MOODS = {"tensione": mood_tensione, "positivo": mood_positivo, "tech": mood_tech}


def main() -> None:
    img, out, mood = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    o = MOODS[mood]()
    o = o * np.clip(t / 1.2, 0, 1) * np.clip((T - t) / 1.5, 0, 1)
    o = o / np.max(np.abs(o)) * 0.35
    s = (o * 32767).astype(np.int16)
    tmp = Path(tempfile.mkdtemp())
    wav = tmp / "a.wav"
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.column_stack([s, s]).ravel().tobytes())
    vf = ("[0:v]scale=2160:3840,zoompan=z='1.0+0.00018*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          "d=1:s=1080x1920:fps=30,format=yuv420p,fade=t=in:st=0:d=0.4[v]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", str(T), "-i", str(img),
                    "-i", str(wav), "-filter_complex", vf, "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "20",
                    "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)],
                   check=True)
    print(out, mood)


if __name__ == "__main__":
    main()
