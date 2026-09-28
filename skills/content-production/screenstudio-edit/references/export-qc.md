# Screen Studio Export And QC

## Delivery Encode

Render a high-quality H.264/AAC master. Measure its pixel range and color metadata, then create a delivery encode with explicit tags. For a measured full-range master intended for SDR BT.709 delivery:

```bash
ffmpeg -y -i master.mp4 \
  -vf 'sidedata=mode=delete:type=ICC_PROFILE,scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p,setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709' \
  -c:v libx264 -preset slow -crf 19 -profile:v high -level:v 4.2 \
  -c:a copy -movflags +write_colr+faststart final.mp4
```

Use the measured input range rather than copying `in_range=full` blindly.

## Mechanical Checks

Full decode:

```bash
ffmpeg -v error -i final.mp4 -map 0:v:0 -map 0:a:0 -f null -
```

Metadata:

```bash
ffprobe -v error \
  -show_entries format=duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,pix_fmt,color_range,color_space,color_transfer,color_primaries,r_frame_rate,sample_rate,channels \
  -of json final.mp4
```

Black frames:

```bash
ffmpeg -hide_banner -i final.mp4 \
  -vf 'blackdetect=d=0.08:pix_th=0.02' -an -f null -
```

Loudness and peak:

```bash
ffmpeg -hide_banner -nostats -i final.mp4 \
  -vn -af 'ebur128=peak=true' -f null -
```

Contact sheet:

```bash
ffmpeg -hide_banner -loglevel error -y -i final.mp4 \
  -vf 'fps=1/10,scale=270:-2,tile=4x3' \
  -frames:v 1 contact.jpg
```

Investigate every detection or metadata mismatch. Then watch the final encoded file at normal speed with headphones and at target playback size. Mechanical scans support playback; they do not replace it.
