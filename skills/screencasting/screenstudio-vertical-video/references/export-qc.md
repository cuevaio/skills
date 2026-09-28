# Export And QC Reference

## Delivery Encode

Render a high-quality H.264/AAC master first. Then make color range and tags explicit. A representative finalization command is:

```bash
ffmpeg -y -i master.mp4 \
  -vf 'sidedata=mode=delete:type=ICC_PROFILE,scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p,setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709' \
  -c:v libx264 -preset slow -crf 19 -profile:v high -level:v 4.2 \
  -c:a copy -movflags +write_colr+faststart final.mp4
```

Confirm the master's actual range before using `in_range=full`; use the measured value rather than forcing the example blindly.

## Mechanical Checks

Full decode:

```bash
ffmpeg -v error -i final.mp4 -map 0:v:0 -map 0:a:0 -f null -
```

Stream and color metadata:

```bash
ffprobe -v error \
  -show_entries format=duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,pix_fmt,color_range,color_space,color_transfer,color_primaries,r_frame_rate,sample_rate,channels \
  -of json final.mp4
```

Require 1080×1920, 30 FPS, yuv420p, limited/tv range, and `bt709` for matrix, transfer, and primaries unless the destination spec says otherwise.

Black-frame scan:

```bash
ffmpeg -hide_banner -i final.mp4 \
  -vf 'blackdetect=d=0.08:pix_th=0.02' -an -f null -
```

Investigate every detection; a deliberate black scene is still a decision that should be documented.

Loudness and true peak:

```bash
ffmpeg -hide_banner -nostats -i final.mp4 \
  -vn -af 'ebur128=peak=true' -f null -
```

Judge loudness against the destination and content rather than chasing one universal number. Speech must remain intelligible on a phone without clipping.

Contact sheet:

```bash
ffmpeg -hide_banner -loglevel error -y -i final.mp4 \
  -vf 'fps=1/10,scale=270:480,tile=4x3' \
  -frames:v 1 contact.jpg
```

Choose a denser interval or multiple sheets for longer videos. The sheet is a gap and layout scan, not a substitute for playback.

## Human Playback

Watch the final encoded file, not only the editor timeline:

- once at normal speed with headphones
- once at phone size with simulated platform controls
- around every cut that crosses screen, camera, audio, or caption state

Confirm no status bar, clock, notification, account name, secret, or irrelevant UI is exposed. Confirm screen prompts and results remain readable for long enough to understand.
