"""Transcribe local media with CPU Whisper and preserve word timestamps."""
import argparse
import json
from pathlib import Path


def timestamp(seconds):
    ms = round(seconds * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("media")
    parser.add_argument("--model", default="small")
    parser.add_argument("--language", help="Language code; omit for detection")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--output", default="transcript")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    from faster_whisper import WhisperModel
    model = WhisperModel(args.model, device="cpu", compute_type="int8", cpu_threads=8,
                         local_files_only=args.local_files_only)
    segments, info = model.transcribe(args.media, beam_size=5, word_timestamps=True,
                                     vad_filter=True, language=args.language)
    result = {"model": args.model, "engine": "faster-whisper", "language": info.language,
              "duration": info.duration, "segments": []}
    with (out / "transcript.txt").open("w") as txt, (out / "transcript.srt").open("w") as srt:
        for index, segment in enumerate(segments, 1):
            data = {"start": segment.start, "end": segment.end, "text": segment.text.strip(),
                    "words": [{"start": w.start, "end": w.end, "word": w.word,
                               "probability": w.probability} for w in segment.words or []]}
            result["segments"].append(data)
            txt.write(f"[{timestamp(segment.start)}] {data['text']}\n")
            txt.flush()
            srt.write(f"{index}\n{timestamp(segment.start)} --> {timestamp(segment.end)}\n{data['text']}\n\n")
            srt.flush()
            print(f"{segment.end:.1f}s / {info.duration:.1f}s {data['text']}", flush=True)
            if index % 25 == 0:
                (out / "partial.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    (out / "transcript.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
