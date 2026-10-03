"""Decode final exports and verify durations, captions, frame sizes and audio."""
import hashlib
import json
from pathlib import Path
import subprocess
import shutil
import imageio_ffmpeg


def main():
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    probe = shutil.which("ffprobe")
    if not probe:
        candidates = list(Path("remotion/node_modules/@remotion").glob("compositor-*/ffprobe*"))
        if not candidates:
            raise FileNotFoundError("ffprobe is required; install it or the platform Remotion compositor")
        probe = str(candidates[0])
    plan = json.loads(Path("remotion/clips.json").read_text())
    report = []
    for clip in plan:
        path = Path("clips") / (clip["id"] + ".mp4")
        meta = json.loads(subprocess.check_output([str(probe), "-v", "error", "-show_streams",
                                                 "-show_format", "-of", "json", str(path)]))
        video = next(s for s in meta["streams"] if s["codec_type"] == "video")
        audio = next(s for s in meta["streams"] if s["codec_type"] == "audio")
        assert (video["width"], video["height"]) == (1080, 1920)
        assert video["r_frame_rate"] == "30/1"
        assert video["codec_name"] == "h264" and audio["codec_name"] == "aac"
        duration = float(meta["format"]["duration"])
        assert abs(duration - clip["duration"]) < .12
        assert int(video["nb_frames"]) == round(clip["duration"] * 30)
        assert clip["captions"] and all(0 <= c["start"] < c["end"] <= duration + .03 for c in clip["captions"])
        for a, b in zip(clip["captions"], clip["captions"][1:]):
            assert a["end"] <= b["start"] + .001
        check = subprocess.run([ffmpeg, "-hide_banner", "-v", "error", "-xerror", "-i", str(path),
                                "-f", "null", "-"], capture_output=True, text=True)
        assert check.returncode == 0, check.stderr
        metrics = subprocess.run([ffmpeg, "-hide_banner", "-i", str(path), "-vf",
                                  "blackdetect=d=0.15:pix_th=0.1", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                                  "-f", "null", "-"], capture_output=True, text=True, check=True)
        black = [line for line in metrics.stderr.splitlines() if "black_start:" in line]
        assert not black, black
        loudness, _ = json.JSONDecoder().raw_decode(metrics.stderr[metrics.stderr.rfind("{"):])
        assert float(loudness["input_tp"]) <= 0
        assert -22 <= float(loudness["input_i"]) <= -12
        silence = subprocess.run([ffmpeg, "-hide_banner", "-i", str(path), "-af",
                                  "silencedetect=noise=-35dB:d=0.30", "-vn", "-f", "null", "-"],
                                 capture_output=True, text=True, check=True)
        long_pauses = [line for line in silence.stderr.splitlines() if "silence_start:" in line]
        assert not long_pauses, long_pauses
        item = {"id": clip["id"], "source_start": clip["start"], "source_end": clip["end"],
                "duration": duration, "frames": int(video["nb_frames"]), "dimensions": "1080x1920",
                "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "caption_groups": len(clip["captions"]), "decode": "pass", "black_frames": "none detected",
                "silence_over_300ms_at_minus35db": "none detected",
                "integrated_loudness_lufs": loudness["input_i"], "true_peak_dbtp": loudness["input_tp"]}
        report.append(item)
        print(json.dumps(item), flush=True)
    Path("review/verification.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
